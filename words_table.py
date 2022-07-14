#builds sqlite3 database from excel file of 5-letter words. Runs automatically when you start a new game and the table of all words is empty.

import sqlite3

def build():
    word_list_file='Downloads\\words_5.xlsx'
    
    connection=sqlite3.connect('wordle.db')
    cursor=connection.cursor()
    
    

