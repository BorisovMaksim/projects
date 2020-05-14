import psycopg2
import csv
import time
from psycopg2 import sql

time1 = time.time()


class SqlUTILS:
    def __init__(self):
        self.url_ActorsDirectorsCodes_IMDB = '/home/maksim/Downloads/ml-latest/ActorsDirectorsCodes_IMDB.tsv'
        self.url_ActorsDirectorsNames_IMDB = '/home/maksim/Downloads/ml-latest/ActorsDirectorsNames_IMDB.csv'
        self.url_links_IMDB_MovieLens = '/home/maksim/Downloads/ml-latest/links_IMDB_MovieLens.csv'
        self.url_MovieCodes_IMDB = '/home/maksim/Downloads/ml-latest/MovieCodes_IMDB.tsv'
        self.url_Ratings_IMDB = '/home/maksim/Downloads/ml-latest/Ratings_IMDB.tsv'
        self.url_TagCodes_MovieLens = '/home/maksim/Downloads/ml-latest/TagCodes_MovieLens.csv'
        self.url_TagScores_MovieLens = '/home/maksim/Downloads/ml-latest/TagScores_MovieLens.csv'
        self.table_MovieCodes_IMDB = ' CREATE TABLE MovieCodes_IMDB (tittleIdIMDB varchar (30),' \
                                     ' ordering varchar (100), title varchar (2048), region varchar(5), "language"  varchar (16),' \
                                     'types varchar(100),attributes varchar(100),isOriginalTitle varchar(5)) '
        self.table_ActorsDirectorsCodes_IMDB = 'CREATE TABLE ActorsDirectorsCodes_IMDB (titleIdIMDB varchar (30),' \
                                               'ordering varchar(10), ActorCodes varchar (50), category varchar (50),' \
                                               ' job varchar (1280), characters varchar (5120))'
        self.table_ActorsDirectorsNames_IMDB = 'CREATE TABLE ActorsDirectorsNames_IMDB (ActorCodes varchar (500),' \
                                               'ActorName varchar (500), birthyear varchar (500), deathyear varchar (50),' \
                                               'Profession varchar (1200), KnownForTitles varchar (1280)) '
        self.table_links_IMDB_MovieLens = 'CREATE TABLE links_IMDB_MovieLens (movieLensId varchar (1208), imdbId varchar (1280),' \
                                          'tmdbId varchar (1280))'
        self.table_links_fix = "UPDATE links_imdb_movielens SET imdbid = ('tt' || imdbid)"

        self.table_Ratings_IMDB = 'CREATE TABLE Ratings_IMDB (titleIdIMDB varchar (500), average_rating varchar (50),' \
                                  ' num_votes varchar (500))'
        self.table_TagCodes_MovieLens = 'CREATE TABLE TagCodes_MovieLens (tagID varchar (1208), tag varchar (10240))'
        self.table_TagScores_MovieLens = 'CREATE TABLE TagScores_MovieLens (movieLensID varchar (1280), tagID varchar(640), ' \
                                         'relevance varchar (640))'
        self.table_new_actors = 'CREATE TABLE table_new_actors (titleimdb varchar (30), actorname varchar(500), category varchar (50) )'
        self.table_new_tags = 'CREATE TABLE table_new_tags (movielensid varchar (13), relevence varchar(40), tagid varchar(50))'

        self.update_new_actors = "insert into table_new_actors ( select actorsdirectorscodes_imdb.titleidimdb, " \
                                 "actorsdirectorsnames_imdb.actorname, category " \
                                 "from actorsdirectorscodes_imdb, actorsdirectorsnames_imdb " \
                                 "where actorsdirectorscodes_imdb.actorcodes = actorsdirectorsnames_imdb.actorcodes " \
                                 "and (category = 'actor' or category = 'actress' or category='director')) "

        self.temp_table = 'create table temp_table ( title varchar (5000) , titleimdb varchar (50),' \
                          ' movielensid varchar (500), tmdbid varchar (30), region varchar (10),' \
                          'average_rating varchar (100), num_votes varchar (100))'
        self.command_drop = 'DROP TABLE ActorsDirectorsNames_IMDB, links_imdb_movielens, moviecodes_imdb,' \
                            'ratings_imdb, tagscores_movielens, tagcodes_movielens,actorsdirectorscodes_imdb,' \
                            ' temp_table, table_new_actors, table_new_tags'
        self.fill_update_new_tags = 'insert into table_new_tags (SELECT movielensid,relevance, tagid from tagscores_movielens' \
                                    ' where  relevance::float > 0.6)'
        self.delete_unneeded_coloumns_1 = 'ALTER TABLE temp_table DROP COLUMN id'
        self.delete_unneeded_coloumns_2 = 'ALTER TABLE temp_table DROP COLUMN region'
        self.delete_unneeded_coloumns_3 = 'ALTER TABLE temp_table DROP COLUMN num_votes'
        self.delete_unneeded_coloumns_4 = 'ALTER TABLE temp_table DROP COLUMN tmdbid'

        self.command_union = "insert into temp_table (select moviecodes_imdb.title, " \
                             "moviecodes_imdb.tittleidimdb, " \
                             "links_imdb_movielens.movielensid, " \
                             "links_imdb_movielens.tmdbid, moviecodes_imdb.region, ratings_imdb.average_rating " \
                             "from moviecodes_imdb, links_imdb_movielens, ratings_imdb " \
                             "where moviecodes_imdb.tittleidimdb = links_imdb_movielens.imdbid " \
                             "and moviecodes_imdb.tittleidimdb = ratings_imdb.titleidimdb " \
                             "and (region = 'RU' or region = 'US') )"
        self.create_seq = 'CREATE SEQUENCE seq ' \
                          'INCREMENT 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1; '

        self.add_colomn = 'ALTER TABLE temp_table ADD COLUMN id integer'
        self.update_seq = "UPDATE temp_table SET id = nextval('seq'); "
        self.delete_duplicates = "DELETE FROM temp_table " \
                                 " WHERE id NOT IN ( SELECT min(id) FROM temp_table GROUP BY titleimdb ) "

    def create_dataset(self, cursor, connection):
        cursor.execute(self.table_ActorsDirectorsCodes_IMDB)
        cursor.execute(self.table_ActorsDirectorsNames_IMDB)
        cursor.execute(self.table_links_IMDB_MovieLens)
        cursor.execute(self.table_MovieCodes_IMDB)
        cursor.execute(self.table_Ratings_IMDB)
        cursor.execute(self.table_TagCodes_MovieLens)
        cursor.execute(self.table_TagScores_MovieLens)
        cursor.execute(self.temp_table)
        cursor.execute(self.table_new_actors)
        cursor.execute(self.table_new_tags)

        connection.commit()

        with open(self.url_MovieCodes_IMDB, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            cursor.copy_from(f, 'MovieCodes_IMDB ', sep='	')

        with open(self.url_ActorsDirectorsCodes_IMDB, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            cursor.copy_from(f, 'ActorsDirectorsCodes_IMDB', sep='	')
        with open(self.url_ActorsDirectorsNames_IMDB, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            cursor.copy_from(f, 'ActorsDirectorsNames_IMDB', sep='	')

        with open(self.url_links_IMDB_MovieLens, 'r') as f:
            reader = csv.reader(f)
            next(reader)

            cursor.copy_from(f, 'links_IMDB_MovieLens', sep=',')

        with open(self.url_Ratings_IMDB, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            cursor.copy_from(f, 'Ratings_IMDB ', sep='	')

        with open(self.url_TagCodes_MovieLens, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            cursor.copy_from(f, 'TagCodes_MovieLens ', sep=',')

        with open(self.url_TagScores_MovieLens, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            cursor.copy_from(f, 'TagScores_MovieLens ', sep=',')
        connection.commit()

    def delete_dataset(self, cursor, connection):
        cursor.execute(self.command_drop)
        connection.commit()

    def update_dataset(self, cursor, connection):
        cursor.execute(self.table_links_fix)
        connection.commit()
        cursor.execute(self.command_union)
        connection.commit()
        # cursor.execute(self.create_seq)
        # connection.commit()
        cursor.execute(self.add_colomn)
        connection.commit()
        cursor.execute(self.update_seq)
        connection.commit()
        cursor.execute(self.delete_duplicates)
        connection.commit()
        cursor.execute(self.delete_unneeded_coloumns_1)
        cursor.execute(self.delete_unneeded_coloumns_2)
        cursor.execute(self.delete_unneeded_coloumns_3)
        cursor.execute(self.delete_unneeded_coloumns_4)
        cursor.execute(self.fill_update_new_tags)
        connection.commit()

    def update_dataset_more(self, cursor, connection):
        cursor.execute(self.update_new_actors)
        connection.commit()


class Movie:
    def __init__(self):
        self.count = 1
        self.interesting_film = str(input())
        print('Название фильма: ' + self.interesting_film)
        self.actors = []
        self.analysys = []
        self.answer = []
        self.state = 'TRUE'
        self.count_1 = 0

    def get_data(self, cursor):
        cursor.execute("SELECT title,titleimdb, movielensid, average_rating "
                       "from temp_table where title = %s ", (self.interesting_film,))
        info = cursor.fetchall()
        if len(info) > 1:
            print("Название неоднозначно, введите код фильма на IMDB")
            new_code = str(input())
            for elem in info:
                if new_code in elem:
                    info = [elem]
                    break

        if len(info) == 0:
            print('Введите корректное название')
            exit()
        print('Рейтинг фильма: ' + info[0][3])
        cursor.execute(("SELECT relevence, table_new_tags.tagid, tag from table_new_tags, tagcodes_movielens "
                        "where table_new_tags.tagid = tagcodes_movielens.tagid and "
                        " movielensid = %s "), (info[0][2],))
        self.tags = cursor.fetchall()
        cursor.execute("SELECT actorname from table_new_actors where titleimdb = %s ", (info[0][1],))

        for i in sorted(cursor.fetchall(), reverse=True):
            if i[0] not in self.actors:
                self.actors.append(i[0])
        print('Съемочная команда: ' + ', '.join(self.actors))
        print('Тэги фильма', end=': ')
        for elem in self.tags:
            if self.count_1 > 5:
                break
            self.count_1 += 1
            print(elem[2], end=', ')
        print()

        cursor.execute('SELECT titleimdb '
                       ' FROM table_new_actors'
                       ' where '
                       'actorname IN %s', (tuple(self.actors),))

        self.imdb_codes = cursor.fetchall()
        cursor.execute(
            "SELECT temp_table.titleimdb, temp_table.title, temp_table.average_rating, temp_table.movielensid "
            "FROM table_new_actors, temp_table, table_new_tags "
            "where table_new_actors.titleimdb = temp_table.titleimdb and "
            "table_new_tags.movielensid = temp_table.movielensid and "
            "temp_table.titleimdb in %s and table_new_tags.tagid in %s", (tuple(self.imdb_codes), tuple(self.tags[1]),))
        self.imdb_info = cursor.fetchall()
        self.imdb_codes = []
        for i in range(len(self.imdb_info)):
            if self.imdb_info[i] not in self.imdb_codes:
                self.imdb_codes.append(self.imdb_info[i])

        for elem in self.imdb_codes:
            self.actors_list = []
            self.full_list = cursor.execute("SELECT actorname from table_new_actors where titleimdb = %s", (elem[0],))
            for actor in cursor.fetchall():
                if actor not in self.actors_list:
                    self.actors_list.append(actor)

            self.similar = (3 * len(list(set(self.actors) & set(self.actors_list))) / (
                    10 * len((list(set(self.actors + self.actors_list)))))
                            + (2 / 10) * float(self.tags[0][0]) / 1024 + (1 / 20) * float(elem[0][3]))
            if elem[1] not in self.analysys and elem[1] != self.interesting_film:
                self.analysys.append((self.similar, elem[1]))
        print("Топ фильмов, похожих на " + self.interesting_film + ":")

        count = 1
        for elem in sorted(list(set(self.analysys)), reverse=True)[:10]:

            print(str(count) + ". " + str(elem[1]))
            count += 1
            self.answer.append(str(elem[1]))
        print(time.time() - time1)


def main():
    Obj = Movie()
    Move_data = SqlUTILS()
    connection = psycopg2.connect(host='localhost', user='postgres', password='likliklik', dbname='postgres')
    cursor = connection.cursor()
    # Move_data.delete_dataset(cursor,connection)
    # Move_data.create_dataset(cursor,connection)
    # Move_data.update_dataset(cursor,connection)
    # Move_data.update_dataset_more(cursor,connection)
    Obj.get_data(cursor)
    cursor.close()
    connection.close()


if __name__ == '__main__':
    main()
