import csv

def main():
    with open("parsed-christies.csv", 'r', newline='', encoding="utf-8") as read_file_1:
        with open(r"parsed-sotheby's.csv", 'r', newline='', encoding="utf-8") as read_file_2:
            with open(r"parsed-wiki-arts.csv", 'r', newline='', encoding="utf-8") as read_file_3:
                with open(r"data_set.csv", 'w+', newline='', encoding="utf-8") as write_file_1:
                    with open(r"data_set_not_found.csv", 'w+', newline='', encoding="utf-8") as write_file_2:
                        headers = ["Author", "Art", "Sale date", "Price", "Size",
                                   "Style", "Estimate", "Description", "Signed", "dated", "Collection",
                                   "Material", "Technique", "Painted",
                                   "Image", "Genre", "Square", "Nazi", "Length description", "Evening sale", "Museum",
                                   "Provenance", "Sothbys", "ProvenanceNum", "Exhibitions"]
                        writer_1 = csv.DictWriter(write_file_1, fieldnames=headers,
                                                  extrasaction='ignore', delimiter=',')
                        writer_2 = csv.DictWriter(write_file_2, fieldnames=["Author", "Art", "Sale date", "Price", "Url", "Report"],
                                                  extrasaction='ignore', delimiter=',')
                        writer_1.writeheader()
                        writer_2.writeheader()
                        reader_1 = csv.reader(read_file_1, delimiter=',')
                        reader_2 = csv.reader(read_file_2, delimiter=',')
                        reader_3 = csv.reader(read_file_3, delimiter=',')
                        read_file_1.readline()
                        read_file_2.readline()
                        read_file_3.readline()
                        for i in range(1000):
                            if i == 0:
                                c = next(reader_1)
                                s = [0]*20
                                w = [0]*20
                            else:
                                c = next(reader_1)
                                s = next(reader_2)
                                w = next(reader_3)



                            # print(w)
                            found_c = c[15]
                            found_s = s[10]
                            if found_c == "1" and found_s == "Found":
                                writer_2.writerow({"Author": c[0], "Art": c[1], "Sale date": c[2], "Price": c[3],
                                                   "Url": c[14] + " and " + s[11],
                                                   "Report": "Found in both Sothby's and Christie's"})
                            elif found_c == "1":
                                currency = c[6][:3] if c[6] is not "-" else ""

                                money = float(c[6][4:c[6].find("-")].replace(",", "", 4)) if currency is not "" else "-"
                                if type(money) is float:
                                    if currency == "GBP":
                                        money = money * 1.22
                                    elif currency == "HKD":
                                        money = money * 0.13
                                    elif currency == "EUR":
                                        money = money * 1.08

                                signed = 1 if c[9].lower().find("sign") != -1 else 0
                                dated = 1 if c[9].lower().find("dated") != -1 else 0
                                if c[10].lower().find("private") != -1 or c[10] == "" or c[10] == None:
                                    collection = 0
                                else:
                                    collection = 1
                                size = c[4].replace(",", ".", 4).replace("by", "x", 2)
                                pos_x = size.find("x")
                                square = round(float(size[:pos_x - 1]) * float(size[pos_x + 1:-3]) / 10000,
                                               4) if pos_x != -1 else 0
                                materials_and_methods = c[11].lower()
                                materials_list = ["canvas", "bronze", "patina", "wood", "cotton", "paper", "board",
                                                  "linen", "lamina",
                                                  "panel", "transparent colour coating", "plexiglas", "metal", "toile"]
                                materials = ""
                                for elem in materials_list:
                                    if elem in materials_and_methods:
                                       materials += elem + ", "
                                materials = materials[:-2]

                                if materials == "":
                                    materials = 'other'
                                if "oil and" in materials_and_methods or "oil, " in materials_and_methods:
                                    methods = "oil and others"
                                elif "oil" in materials_and_methods:
                                    methods = "oil only"
                                else:
                                    methods = "other techniques"
                                genre = "-"
                                style = c[5]
                                image = c[13]
                                if w[10] == "1":
                                    if style == "-":
                                        style = w[5]
                                    if w[4] is not None:
                                        genre = w[4]
                                    if image == "-":
                                        image = w[6]
                                    if size == "-":
                                        size = w[7].replace(",", ".", 4).replace("by", "x", 2)
                                        pos_x = size.find("x")
                                        square = round(float(size[:pos_x - 1]) * float(size[pos_x + 1:-3]) / 10000,
                                                       4) if pos_x != -1 else 0
                                    if collection == "-":
                                        if w[9].lower().find("private") != -1 or w[9] == "" or w[9] == None:
                                            collection = 0
                                        else:
                                            collection = 1
                                nazi = 1 if c[7].lower().count("nazi") != 0 else 0
                                if nazi == 0:
                                    nazi = 1 if c[8].lower().count("nazi") != 0 else 0

                                pos = style.lower().find("evening")
                                evening_sale = 0 if pos == -1 else 1
                                style = style if pos == -1 else style[:pos - 1]
                                museum = 1 if c[7].lower().find("museum") != -1 else 0
                                art = c[1]
                                art = art if art.find("REPEAT") == -1 else art[:art.find("REPEAT") - 1]
                                exhibitions = c[7].lower().count("museum") + c[7].lower().count("hall") + c[7].lower().count("gallery")
                                writer_1.writerow({"Author": c[0] , "Art": art, "Sale date": c[2], "Price": c[3].replace(",", "", 4), "Size": size,
                                   "Style": style, "Estimate": money, "Signed": signed, "dated": dated, "Collection": collection,
                                   "Material": materials , "Technique": methods, "Painted": c[12],
                                   "Image": image, "Genre": genre, "Square": square, "Nazi": nazi, "Length description": len(c[8]),
                                                   "Evening sale": evening_sale, "Description": c[8], "Museum": museum,
                                                   "Provenance": c[7], "Sothbys": 0, "ProvenanceNum": len(c[7]), "Exhibitions": exhibitions })
                            elif s[10] == "Found":
                                money_str = s[9].replace(",", "", 4)
                                money = float(money_str) if money_str is not "-" else "-"

                                signed = 1 if s[5].lower().find("sign") != -1 else 0
                                dated = 1 if s[5].lower().find("dated") != -1 else 0
                                collection = 0

                                size = s[7].replace(",", ".", 4).replace("by", "x", 2)
                                pos_x = size.find("x")
                                square = round(float(size[:pos_x - 1]) * float(size[pos_x + 1:-3]) / 10000,
                                               4) if pos_x != -1 else 0
                                materials_and_methods = s[6].lower()
                                materials_list = ["canvas", "bronze", "patina", "wood", "cotton", "paper", "board",
                                                  "linen", "lamina",
                                                  "panel", "transparent colour coating", "plexiglas", "metal", "toile"]
                                materials = ""
                                for elem in materials_list:
                                    if elem in materials_and_methods:
                                        materials += elem + ", "
                                materials = materials[:-2]

                                if materials == "":
                                    materials = 'other'
                                if "oil and" in materials_and_methods or "oil, " in materials_and_methods:
                                    methods = "oil and others"
                                elif "oil" in materials_and_methods:
                                    methods = "oil only"
                                else:
                                    methods = "other techniques"
                                genre = "-"
                                style = "-"
                                image = s[8]
                                if w[10] == "1":
                                    if style == "-":
                                        style = w[5]
                                    if w[4] is not None:
                                        genre = w[4]
                                    if image == "-":
                                        image = w[6]
                                    if size == "-":
                                        size = w[7].replace(",", ".", 4).replace("by", "x", 2)
                                        pos_x = size.find("x")
                                        square = round(float(size[:pos_x - 1]) * float(size[pos_x + 1:-3]) / 10000,
                                                       4) if pos_x != -1 else 0
                                    if collection == "-":
                                        if w[9].lower().find("private") != -1 or w[9] == "" or w[9] == None:
                                            collection = 0
                                        else:
                                            collection = 1
                                nazi = 1 if s[4].lower().count("nazi") != 0 else 0
                                if nazi == 0:
                                    nazi = 1 if s[11].lower().count("nazi") != 0 else 0
                                pos = style.lower().find("evening")
                                evening_sale = 0 if pos == -1 else 1
                                style = style if pos == -1 else style[:pos - 1]
                                museum = 1 if s[4].lower().find("museum") != -1 else 0
                                art = s[1]
                                art = art if art.find("REPEAT") == -1 else art[:art.find("REPEAT") - 1]
                                exhibitions = s[4].lower().count("museum")

                                writer_1.writerow(
                                    {"Author": s[0], "Art": art, "Sale date": s[2], "Price": s[3].replace(",", "", 4),
                                     "Size": size,
                                     "Style": style, "Estimate": money, "Signed": signed, "dated": dated,
                                     "Collection": collection,
                                     "Material": materials, "Technique": methods, "Painted": "-",
                                     "Image": image, "Genre": genre, "Square": square,
                                     "Nazi": nazi, "Length description": len(s[11]), "Evening sale": evening_sale, "Description": s[11],
                                     "Museum": museum, "Provenance": s[4], "Sothbys": 1, "ProvenanceNum": len(s[4]), "Exhibitions": exhibitions})
                            else:
                                # print(c)
                                # print(s)
                                writer_2.writerow({"Author": c[0], "Art": c[1], "Sale date": c[2], "Price": c[3],
                                                   "Url": c[14] + " and " + s[11],
                                                   "Report": "Not Found in both Sothby's and Christie's"})

                        read_file_1.close()
                        read_file_2.close()
                        read_file_3.close()
                        write_file_1.close()
                        write_file_2.close()


if __name__ == '__main__':
    main()
