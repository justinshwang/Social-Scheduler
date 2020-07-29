import csv
import pymysql

class Database(object):

    def _init_(self, host, password, user):
        self.db = pymysql.connect(host='localhost',
            user='root',
            passwd='',
            db='mydb')
    
    def update(self, file):
        cursor = self.db.cursor()
        # csv_data = csv.reader(open('test.csv'))
        csv_data = csv.reader(file('assets/schedules/schedule3.csv'))
        # next(csv_data)
        for row in csv_data:
            cursor.execute('INSERT INTO PM(col1,col2) VALUES(%s, %s)',row)

            # cursor.execute('INSERT INTO testcsv(names, \
            #     classes, mark )' \
            #     'VALUES("%s", "%s", "%s")', 
            #     row)
        #close the connection to the database.
        self.db.commit()
        cursor.close()
        print("Done")