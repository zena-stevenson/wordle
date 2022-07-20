#builds sqlite3 database from excel file of 5-letter words. Runs automatically when you start a new game and the table of all words is empty.

import sqlite3
import pandas as pd

def build():
    word_list_file='words_5.xlsx'
    words_df=pd.read_excel(word_list_file)
    connection=sqlite3.connect('wordle.db')
    cursor=connection.cursor()
    
    words_df.to_sql('all_words', connection, if_exists='append', index=False)
    
    
    

