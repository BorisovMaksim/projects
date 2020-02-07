import csv
import sys
csv.field_size_limit(sys.maxsize)
sys.setrecursionlimit(10000)



dictionary_NameOfFilm_ImdbCode = dict()
dictionary_ImdbCode_Rating = dict()
dictionary_ImdbCode_CodeOfManAndProfession = dict()
dictionary_ImdbCode_MovieLensCode = dict()
dictionary_TagID_Tag = dict()
dictionary_MovieLensCode_TagID = dict()
dictionary_MovieLensCode_TagRating = dict()
dictionary_NameOfFilm_ObjectMovie = dict()
dictionary_MovieLensCode_Name = dict()



with open("/home/maksim/Downloads/ml-latest/MovieCodes_IMDB.tsv") as tsvfile:
    tsvreader = csv.reader(tsvfile, delimiter="\t")
    for line in tsvreader:
        k = line[4]
        c = line[3]
        if 'ru' == k  or 'en' == k or 'us' == k or 'US' == c or 'RU' == c or 'EN' == c:
            if line[2] not in dictionary_NameOfFilm_ImdbCode:
                 dictionary_NameOfFilm_ImdbCode[line[2]]=line[0]

with open("/home/maksim/Downloads/ml-latest/Ratings_IMDB.tsv") as tsvfile:
    tsvreader = csv.reader(tsvfile, delimiter="\t")
    for line in tsvfile:
        dictionary_ImdbCode_Rating[line[0:9]] = line[10:13]

with open("/home/maksim/Downloads/ml-latest/ActorsDirectorsCodes_IMDB.tsv") as tsvfile:
    tsvreader = csv.reader(tsvfile, delimiter="\t")
    for line in tsvreader:
        if line[3]=='director' or line[3]=='actress' or line[3]=='actor':
            if line[0] in dictionary_ImdbCode_CodeOfManAndProfession:
                dictionary_ImdbCode_CodeOfManAndProfession[line[0]]=((line[2],line[3]),dictionary_ImdbCode_CodeOfManAndProfession[line[0]])
            else:
                dictionary_ImdbCode_CodeOfManAndProfession[line[0]]=(line[2],line[3])
#
with open("/home/maksim/Downloads/ml-latest/ActorsDirectorsNames_IMDB.txt") as tsvfile:
   tsvreader = csv.reader(tsvfile, delimiter="\t")
   for line in tsvreader:
       if line[0] not in dictionary_MovieLensCode_Name:
           dictionary_MovieLensCode_Name[line[0]]=line[1]



with open("/home/maksim/Downloads/ml-latest/links_IMDB_MovieLens.csv") as tsvfile:
    tsvreader = csv.reader(tsvfile, delimiter="\t")
    for line in tsvreader:
        line = line[0].split(',')
        dictionary_ImdbCode_MovieLensCode[line[1]] = line[2]

with open("/home/maksim/Downloads/ml-latest/TagCodes_MovieLens.csv") as tsvfile:
    tsvreader = csv.reader(tsvfile, delimiter="\t")
    for line in tsvreader:
        line = line[0].split(',')
        dictionary_TagID_Tag[line[0]] = line[1]

with open("/home/maksim/Downloads/ml-latest/TagScores_MovieLens.csv") as tsvfile:
    tsvreader = csv.reader(tsvfile, delimiter="\t")
    for line in tsvreader:
        line = line[0].split(',')
        if line[0] in dictionary_MovieLensCode_TagID:
            dictionary_MovieLensCode_TagRating[line[0]] = (line[2],dictionary_MovieLensCode_TagRating[line[0]])
            dictionary_MovieLensCode_TagID[line[0]]=(line[1],dictionary_MovieLensCode_TagID[line[0]])
        else:
            dictionary_MovieLensCode_TagRating[line[0]]=(line[2])
            dictionary_MovieLensCode_TagID[line[0]]=(line[1])
#
#
#



class Movie:
    def __init__(self, rating, group, name_of_film, tags):
        self.rating = rating
        self.group = group
        self.name_of_film = name_of_film
        self.tags = tags

    def print_information(self):
        print('Название фильма: '+self.name_of_film)
        print('Участвовали: '+self.group)
        print('Рейтинг фильма: '+self.rating)
        print('Тэги фильма: '+self.tags)




for elem in dictionary_NameOfFilm_ImdbCode.items():
    rating = dictionary_ImdbCode_Rating[elem[1]]
    group_with_codes = dictionary_ImdbCode_CodeOfManAndProfession[elem[1]]
    for member in group_with_codes:
        member[0] = dictionary_MovieLensCode_Name[member[0]]
    name_of_film = elem[0]
    tags = dictionary_MovieLensCode_TagID[dictionary_ImdbCode_MovieLensCode[elem[1]]]

    dictionary_NameOfFilm_ObjectMovie[elem[0]] = Movie(rating, group_with_codes, name_of_film, tags).print_information()

print(dictionary_NameOfFilm_ObjectMovie['Партия в карты'])