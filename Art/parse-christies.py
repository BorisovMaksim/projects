import csv
from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import dateparser
import re

from multiprocessing import Pool

session = requests.Session()
session.mount('https://', HTTPAdapter(max_retries=Retry(connect=5, backoff_factor=0.5)))


def get_links():
    with open(r"arts.csv", newline='', encoding="utf-8") as read_file:
        d = {"Author": [], "Art": [], "Sale date": [], "Price": [], "Urls": [], "Found": []}
        reader = csv.reader(read_file, delimiter=',')
        for row in reader:
            try:
                pos_repeat_sale = row[1].find("REPEAT SALE")
                art = row[1] if pos_repeat_sale is -1 else row[1][:pos_repeat_sale]
                url = 'https://www.christies.com/lotfinder/' \
                      'searchresults.aspx?sc_lang=en&lid=1&searchFrom=searchresults&entry=' \
                      '{} {}&searchtype=p&action=search'.format(row[0], art)
                with session.get(url, stream=True) as response:
                    soup = BeautifulSoup(response.text, "lxml")
                    url_ok = "-"
                    for link in soup.find_all('a'):
                        url_to_lot = link.get('href')
                        if url_to_lot is not None and url_to_lot.startswith('https'):
                            with session.get(url_to_lot, stream=True) as response_to_lot:
                                soup = BeautifulSoup(response_to_lot.text, "lxml")
                                sale_date_soup = soup.find(id="main_center_0_lblSaleDate")
                                sale_date = "-" if sale_date_soup is None else dateparser.parse(sale_date_soup.text)
                                if sale_date == dateparser.parse(row[2]):
                                    url_ok = url_to_lot
                                break
                d["Author"].append(row[0])
                d["Art"].append(row[1])
                d["Sale date"].append(row[2])
                d["Price"].append(row[3])
                d["Urls"].append(url_ok)
                if url_ok == "-":
                    d["Found"].append(0)
                else:
                    d["Found"].append(1)

            except Exception:
                print("Exception")
                d["Author"].append(row[0])
                d["Art"].append(row[1])
                d["Sale date"].append(row[2])
                d["Price"].append(row[3])
                d["Urls"].append("-")
                d["Found"].append(0)

                continue



        read_file.close()
        return d


def parse_link(url):
    if url == "-":
        return {"Painted": "-", "Technique and performance material": "-", "Estimate": "-",
                "Size": "-", "Style": "-", "Provenance": "-", "Sign": "-",
                "Collection": "-", "Image": "-", "Description": "-"}
    response = session.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    description_soap = soup.find(id="main_center_0_lblLotDescription")
    estimate_soap = soup.find(id="main_center_0_lblPriceEstimatedPrimary")
    style_soap = soup.find(id="main_center_0_lblSaleTitle")
    provenance_soup = soup.find(id="main_center_0_lblLotProvenance")
    img_soup = soup.find("a", class_="panzoom--link")

    description = "-" if description_soap is None else description_soap.text
    estimate = "-" if estimate_soap is None else estimate_soap.text
    style = "-" if style_soap is None else style_soap.text
    provenance = "-" if provenance_soup is None else provenance_soup.text
    img = "-" if img_soup is None else img_soup.get('data-large-url')

    sign_list = ["sign", " titled", r"\ntitled", "dated", "stamped"]
    method_list = ["oil", "canvas", "ink(s)?", "casein", "limestone", "patina", " graph",
                   "pigment", "acrylic",
                   "steel", "bronze", "pastel", "gouache", "charcoal", "engraving", "metal",
                   "rod", "wire",
                   "colour", "board", "Kautschuk", "baked", "enamel", "paper", "plaster",
                   "chalk", "iron",
                   "tempera"]
    regex_collection = re.compile(r'(\n)?[^\n]*collection[^\n]*(\n)?', flags=re.IGNORECASE)
    regex_sign = re.compile(
        r'(\n)?[^\n]*' + r'[^\n]*(\n)?|(\n)?[^\n]*'.join(sign_list) + r'[^\n]*(\n)?',
        flags=re.IGNORECASE)
    regex_method = re.compile(
        r'\n[^\n]*' + r'[^\n]*\n|\n[^\n]*'.join(method_list) + r'[^\n]*\n',
        flags=re.IGNORECASE)
    regex_size = re.compile(r'\d(\d)*(.)?(\d)* x \d(\d)*(.)?(\d)*( )?cm|'
                            r'\d(\d)*(.)?(\d)* x \d(\d)*(.)?(\d)*( )?mm|'
                            r'\d(\d)*(.)(\d)?( )?cm')
    regex_date = re.compile(
        r'Painted[^"]*\d{4}|Executed [^"]* \d{4}|Conceived [^"]* \d{4}|Drawn[^"]* \d{4}')
    ans_sign = regex_sign.search(description)
    ans_method = regex_method.search(description)
    ans_size = regex_size.search(description)
    ans_date = regex_date.search(description)
    ans_collection = regex_collection.search(provenance)
    sign = "-" if ans_sign is None else ans_sign.group()
    collection = "-" if ans_collection is None else ans_collection.group()
    method = "-" if ans_method is None else ans_method.group()[1:-2]
    size = "-" if ans_size is None else ans_size.group()
    date = "-" if ans_date is None else re.search(r'\d{4}', ans_date.group()).group()

    return {"Painted": date, "Technique and performance material": method, "Estimate": estimate,
            "Size": size, "Style": style, "Provenance": provenance, "Sign": sign,
            "Collection": collection, "Image": img, "Description": description}


def main():
    with open("parsed-christies.csv", 'w+', newline='', encoding="utf-8") as write_file:
        writer = csv.DictWriter(write_file, fieldnames=["Author", "Art", "Sale date", "Price", "Size",
                                                        "Style", "Estimate", "Provenance", "Description", "Sign", "Collection",
                                                        "Technique and performance material", "Painted",
                                                        "Image", "Urls", "Found"],
                                extrasaction='ignore', delimiter=',')
        writer.writeheader()
        for num in range(len(records)):
            writer.writerow(
                {"Author": info["Author"][num], "Art": info["Art"][num], "Painted": records[num]["Painted"],
                 "Sale date": info["Sale date"][num],
                 "Price": info["Price"][num], "Urls": info["Urls"][num], "Found": info["Found"][num],
                 "Technique and performance material": records[num]["Technique and performance material"],
                 "Estimate": records[num]["Estimate"], "Size": records[num]["Size"],
                 "Style": records[num]["Style"], "Provenance": records[num]["Provenance"],
                 "Sign": records[num]["Sign"], "Description": records[num]["Description"],
                 "Collection": records[num]["Collection"], "Image": records[num]["Image"]})
    write_file.close()


if __name__ == '__main__':
    info = get_links()
    p = Pool(10)
    records = p.map(parse_link, info["Urls"])
    p.terminate()
    p.join()
    main()
