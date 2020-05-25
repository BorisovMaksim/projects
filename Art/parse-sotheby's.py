import csv
from difflib import SequenceMatcher
from selenium import webdriver
import dateparser
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def main():
    with open("parsed-sotheby's.csv", 'w+', newline='', encoding="utf-8") as write_file:
        with open(r"arts.csv", newline='', encoding="utf-8") as read_file:
            headers = ["Author", "Art", "Sale date", "Price","Provenance", "Sign", "Technique and performance material",
                       "Size", "Image", "Estimate", "Report", "Description",
                       "Tried url"]
            writer = csv.DictWriter(write_file, fieldnames=headers,
                                    extrasaction='ignore', delimiter=',')
            writer.writeheader()
            reader = csv.reader(read_file, delimiter=',')
            read_file.readline()
            driver = webdriver.Chrome(r'/home/maksim/Apps/chromedriver')
            driver.maximize_window()
            for row in reader:
                found = 0
                print(row)
                author = row[0]
                pos = row[1].find('REPEAT SALE')
                art = row[1] if pos == -1 else row[1][:pos]
                url_to_art = "https://www.sothebys.com/en/search-results.html?" \
                             "query={} {}&refinementList%5Btype%5D%5B0%5D=Lot&timeframe=past".format(author, art)
                driver.get(url_to_art)

                try:  # Ждем пока на страничке появятся элементы
                    WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "Card-artistWorkTitle")))
                    WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "Card-info-container")))
                    WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "Card-details")))
                    WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "Card-media")))
                except Exception:
                    writer.writerow({"Author": row[0], "Art": row[1], "Sale date": row[2], "Price": row[3],
                                     "Report": "Not Found", "Tried url": url_to_art})
                    continue

                urls_request = driver.find_elements_by_class_name('Card-info-container')
                images_request = driver.find_elements_by_class_name('Card-media')
                for i in range(len(urls_request)):
                    url = urls_request[i]
                    try:  # Пытаемся найти изображение
                        image = images_request[i].find_element_by_tag_name('img').get_attribute('src')
                    except Exception:
                        continue

                    try:  # Пытаемся найти дату
                        date = url.find_element_by_class_name('Card-details')
                        pos = date.text.find('|')
                        date = date.text[: pos] if pos != -1 else row[2]
                    except Exception:  # Если дата не указана, то считаем ее за правильную
                        date = row[2]
                    try:  # Пробуем найти текст способом 1
                        art_request = url.find_element_by_class_name('Card-artistWorkTitle')
                        s_art = "-" if art_request is None else art_request.text
                    except Exception:  # Если не получилось, находим текст способом 2
                        s_art = ""
                        for elem in url.find_elements_by_class_name("ais-Highlight-highlighted"):
                            s_art += elem.text
                    pos = s_art.find("(")
                    s_art = s_art[:pos]
                    if dateparser.parse(date) == dateparser.parse(row[2]) and similar(s_art.lower(), art.lower()) > 0.6:

                        driver.get(url.get_attribute('href'))
                        try:  # Если не нашли описание лота, то переходим к следующему
                            WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.CLASS_NAME, "lotdetail-description")))
                        except Exception:
                            continue
                        text_request = driver.find_elements_by_class_name("lotdetail-description-text")
                        text = "-" if len(text_request) < 1 else text_request[0].text
                        side_info_request = driver.find_elements_by_class_name("readmore-content")
                        side_info = ""
                        for piece in side_info_request:
                            side_info += piece.text + "\n"
                        try:
                            estimate_request = driver.find_element_by_class_name('range-from')
                        except Exception:
                            estimate_request = None
                        s_estimate = "-" if estimate_request is None else estimate_request.text
                        found = 1
                        break
                if found: # Начинаем обработку данных
                    sign_list = ["sign", " titled", r"\ntitled", "dated", "stamped"]
                    method_list = ["oil", "canvas", "ink(s)?", "casein", "limestone", "patina", " graph",
                                   "pigment", "acrylic",
                                   "steel", "bronze", "pastel", "gouache", "charcoal", "engraving", "metal",
                                   "rod", "wire",
                                   "colour", "board", "Kautschuk", "baked", "enamel", "paper", "plaster",
                                   "chalk", "iron",
                                   "tempera"]
                    re_col = re.compile(r'(\n)?[^\n]*collection[^\n]*(\n)?', flags=re.IGNORECASE)
                    re_sign = re.compile(
                        r'(\n)?[^\n]*' + r'[^\n]*(\n)?|(\n)?[^\n]*'.join(sign_list) + r'[^\n]*(\n)?',
                        flags=re.IGNORECASE)
                    re_met = re.compile(
                        r'\n[^\n]*' + r'[^\n]*\n|\n[^\n]*'.join(method_list) + r'[^\n]*\n',
                        flags=re.IGNORECASE)
                    re_size = re.compile(r'\d(\d)*(.)?(\d)* x \d(\d)*(.)?(\d)*( )?cm|'
                                            r'\d(\d)*(.)?(\d)* x \d(\d)*(.)?(\d)*( )?mm|'
                                            r'\d(\d)*(.)(\d)?( )?cm|'
                                            r'\d(\d)*(.)?(\d)* by \d(\d)*(.)?(\d)*( )?cm')
                    re_date = re.compile(
                        r'Painted[^"]*\d{4}|Executed [^"]* \d{4}|Conceived [^"]* \d{4}|Drawn[^"]* \d{4}')
                    sign = "-" if re_sign.search(text) is None else re_sign.search(text).group()
                    collection = "-" if re_col.search(side_info) is None else re_col.search(side_info).group()
                    method = "-" if re_met.search(text) is None else re_met.search(text).group()[1:-1]
                    size = "-" if re_size.search(text) is None else re_size.search(text).group()
                    date = "-" if re_date.search(text) is None else re.search(r'\d{4}', re_date.search(text).group()).group()
                    writer.writerow({"Author": author, "Art": art, "Sale date": row[2], "Price": row[3],
                                     "Painted": date, "Technique and performance material": method,
                                     "Size": size, "Provenance": side_info, "Description": text, "Sign": sign,
                                     "Collection": collection, "Image": image, "Estimate": s_estimate, "Report": "Found"})

                else:
                    writer.writerow({"Author": row[0], "Art": row[1], "Sale date": row[2], "Price": row[3],
                                     "Report": "Not Found", "Tried url": url_to_art})

            read_file.close()
            write_file.close()


if __name__ == '__main__':
    main()
