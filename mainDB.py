from kivy.app import App
import sqlite3
import os.path
from kivy.uix.boxlayout import BoxLayout

class Database(BoxLayout):
    def __init__(self,**kwargs):
        super(Database,self).__init__(**kwargs)
        self.cols = 2

    def on_release(self):
        try:
            self.conn = sqlite3.connect('test.db')
            print("done")
            self.sql = '''create table if not exists sample(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            PICTURE BLOB,
            TYPE TEXT,
            FILE_NAME TEXT);'''
            try:
                self.conn.execute(self.sql)
                print("created table")
            except:
                print("already there")
        except:
            print("fail")


    def insert_picture(self,conn, picture_file):
        with open(picture_file, 'rb') as input_file:
            ablob = input_file.read()
            base=os.path.basename(picture_file)
            afile, ext = os.path.splitext(base)
            sql = '''INSERT INTO sample
            (PICTURE, TYPE, FILE_NAME)
            VALUES(?, ?, ?);'''
            conn.execute(sql,[sqlite3.Binary(ablob), ext, afile])
            print("added picture")
            self.conn.commit()

    def on_picture_insert(self):
        self.picture_file = './pictures/team.jpg'
        self.insert_picture(self.conn,self.picture_file)

    def extract_picture(self,cursor, picture_id):
        self.sql1 = "SELECT PICTURE, TYPE, FILE_NAME FROM sample WHERE id = :id"
        self.param = {'id': picture_id}
        for r in self.conn.execute(self.sql1,self.param):
            self.filename = r[2]+r[1]
            self.ablob = r[0]
        with open(self.filename, 'wb') as output_file:
            output_file.write(self.ablob)
        return self.filename

    def on_show_picture(self):
        self.cur = self.conn.cursor()
        self.filename = self.extract_picture(self.cur, 1)
        self.lista = []
        self.p = self.conn.execute("select FILE_NAME,TYPE from sample")
        for r in self.p:
            for i in r:
                self.lista.append(str(i))

            self.ids.label_picture.text = str(self.lista)
            print(self.ids.label_picture.text)

class mainApp(App):

    def build(self):
        return Database()

if __name__ == '__main__':
    mainApp().run()