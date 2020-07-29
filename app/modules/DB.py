import csv
import pymysql
pymysql.install_as_MySQLdb()

class Database(object):
    def _init_(self, host, password, user):
        self.mydb = MySQLdb.connect(host='localhost',
            user='root',
            passwd='',
            db='mydb')
    
    def update(self, file):
        cursor = self.mydb.cursor()
        csv_data = csv.reader(file('students.csv'))
        for row in csv_data:

            cursor.execute('INSERT INTO testcsv(names, \
                classes, mark )' \
                'VALUES("%s", "%s", "%s")', 
                row)
        #close the connection to the database.
        self.mydb.commit()
        cursor.close()
        print("Done")