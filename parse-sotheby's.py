import csv
import time
from difflib import SequenceMatcher
from selenium import webdriver

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()



def main():
    with open("parsed-sotheby's-arts.csv", 'w+', newline='', encoding="utf-8") as write_file:
        with open(r"arts.csv", newline='', encoding="utf-8") as read_file:
            headers = ["Author", "Art", "Sale date", "Price", "Side_info", "Main_info"]
            writer = csv.DictWriter(write_file, fieldnames=headers,
                                    extrasaction='ignore', delimiter=',')
            writer.writeheader()
            reader = csv.reader(read_file, delimiter=',')
            read_file.readline()
            # read_file.readline()
            driver = webdriver.Chrome(r'C:\Users\Maks\Downloads\chromedriver_win32\chromedriver')
            num = 0
            for row in reader:
                num += 1
                author = row[0]
                art = row[1]
                driver.implicitly_wait(3)
                driver.get("https://www.sothebys.com/en")
                driver.find_elements_by_xpath("//input[@type='search']")[0].send_keys(author + " " + art)
                driver.find_elements_by_xpath('//button[@class="HeaderSearch-magnifier"]')[0].click()
                driver.implicitly_wait(3)

                # author_request = driver.find_elements_by_class_name('ais-Highlight')
                art_request = driver.find_elements_by_class_name('Card-artistWorkTitle')
                url_request = driver.find_elements_by_class_name('Card-info-container')

                for i in range(len(art_request)):
                    driver.implicitly_wait(3)
                    s_art = "-" if art_request[i] is None else art_request[i].text
                    s_url = "-" if url_request is None else url_request[i].get_attribute('href')

                    print(num, art, s_art, similar(art.lower(), s_art.lower()))
                    if similar(art.lower(), s_art.lower()) > 0.7:
                        driver.get(s_url)
                        text_request = driver.find_elements_by_class_name("lotdetail-description-text")
                        text = "-" if len(text_request) < 1 else text_request[0].text
                        side_info_request = driver.find_elements_by_class_name("readmore-content")
                        side_info = ""
                        for piece in side_info_request:
                            side_info += piece.text + "\n"
                        writer.writerow({"Author": row[0], "Art": row[1], "Sale date": row[2], "Price": row[3],
                                         "Side_info": side_info, "Main_info": text})
                        print({"Author": row[0], "Art": row[1], "Sale date": row[2], "Price": row[3],
                                         "Side_info": side_info, "Main_info": text})
                        break


        read_file.close()
    write_file.close()


if __name__ == '__main__':
    main()
