import csv
from difflib import SequenceMatcher
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()



def main():
    with open("parsed-wiki-arts_3.csv", 'w+', newline='', encoding="utf-8") as write_file:
        with open(r"arts.csv", newline='', encoding="utf-8") as read_file:
            headers = ["Author", "Art", "Sale date", "Price", "Genre", "Style", "Image", "Dimensions", "Media",
                       "Location",
                       "Found", "Url"]
            writer = csv.DictWriter(write_file, fieldnames=headers,
                                    extrasaction='ignore', delimiter=',')
            writer.writeheader()
            reader = csv.reader(read_file, delimiter=',')
            read_file.readline()
            driver = webdriver.Chrome(r'/home/maksim/Apps/chromedriver')
            driver.maximize_window()
            for row in reader:
                author = row[0]
                pos = row[1].find('REPEAT SALE')
                art = row[1] if pos == -1 else row[1][:pos]
                url_search = "https://www.wikiart.org/en/Search/{} {}".format(author, art)
                driver.get(url_search)
                d = dict.fromkeys(headers)
                d["Author"] = author
                d["Art"] = art
                d["Sale date"] = row[2]
                d["Price"] = row[3]
                d["Found"] = 0
                d["Url"] = url_search
                try:
                    WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//*[@class='artwork-name ng-binding']")))
                    pictures = driver.find_elements_by_xpath("//*[@class='artwork-name ng-binding']")
                    names = driver.find_elements_by_xpath("//*[@class='artist-name ng-binding']")
                    for i in range(len(pictures)):
                        if similar(pictures[i].text, row[1]) > 0.8 and \
                                similar(names[i].text[:names[i].text.find("•") - 1], author) > 0.8:
                            url = pictures[i].get_attribute('href')
                            driver.get(url)
                            WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH, "//*[@class='wiki-top-menu-logo en']")))
                            info = driver.find_elements_by_xpath("/html/body/div[2]/div["
                                                                 "1]/section[1]/main/div[2]/article/ul/li")
                            image = driver.find_element_by_xpath("//*[@class='wiki-layout-artist-image-wrapper "
                                                                 "btn-overlay-wrapper-artwork ng-scope']").\
                                find_element_by_tag_name('img').get_attribute('src')
                            d["Image"] = image
                            d["Found"] = 1
                            for elem in info:
                                pos = elem.text.find(":")
                                d[elem.text[:pos]] = elem.text[pos + 2:]
                            break
                    writer.writerow(d)
                    print(d)
                except Exception:
                    writer.writerow(d)
                    print(d)
                    continue
            read_file.close()
            write_file.close()


if __name__ == '__main__':
    main()
