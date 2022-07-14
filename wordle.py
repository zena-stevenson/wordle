#should really oop-ify all this- a "wordle" object is an individual game, with functions that do stuff like select the right answer, connect to the database of all possible, evaluate guesses, update database after a guess, etc. 

import sqlite3

class Wordle:
    def __init__(self):        
        
        self.connection = sqlite3.connect('wordle.db')
        self.cursor = self.connection.cursor()
        
        self.answer=self.set_answer(self.cursor)
        self.table=self.clone_table(self.cursor)

    
    def set_answer(self, cursor):
        '''Eventually this will select a random word from the database to be the answer to the puzzle.
        For now we're just picking a word'''
        ans='SMALL'
        return(ans)
    
    def clone_table(self, cursor):
        '''clones table all_words so we can update the clone/ not alter the original.'''
        
        #connection = sqlite3.connect('wordle.db')
        #cursor = connection.cursor()
        #cursor.execute("DROP TABLE clone;") #clears out clone table from last game
        cursor.execute('''CREATE TABLE clone(
                    l0 char(1),
                    l1 char(1),
                    l2 char(1),
                    l3 char(1),
                    l4 char(1)
                    ); ''')
        
        cursor.execute("INSERT INTO clone SELECT * FROM all_words;")
        connection.commit()
        connection.close()
        return('clone')
    
    def print_table(self):
        '''prints the table of all possible valid guesses'''
        self.cursor.execute("SELECT * FROM clone;")
        ans=self.cursor.fetchall()
        for a in ans:
            print(a)
        
    def gray(self, letter, table, cursor): 
        '''narrows down the word table based on a gray letter (not present in the correct answer)'''
        statement = "SELECT * FROM "+table+" WHERE '"+letter+"' NOT IN (l0, l1, l2, l3, l4)"
        return(statement)
        

    def yellow(self, letter, position, table, cursor):
        '''narrows down the word table based on a yellow letter (letter is present in the correct answer, but not in the position where we guessed it)'''
        statement = "SELECT * FROM "+table+" WHERE "+position+" != '"+letter+"' AND '"+letter+"' IN (l0, l1, l2, l3, l4)"
        return(statement)
        

    def green(self, letter, position, table, cursor):
        '''narrows down the word table based on a green letter (letter is present and in the correct position)'''
        statement = "SELECT * FROM "+table+" WHERE "+position+" == '"+letter+"'"
        return(statement)
    
    def eval_guess(self, guess):
        
        '''compares the guessed word to the answer, and builds a sql statement to narrow down the list of next guesses letter by letter.'''
        statement = ''
        for pos, letter in enumerate(guess):
            
            if letter not in self.answer:
                statement=statement+self.gray(letter, 'all_words', cursor)
            elif letter in self.answer and self.answer.index(letter)!= pos:
                statement=statement+self.yellow(letter, 'l'+str(pos), self.table, cursor)
            elif self.answer.index(letter)== pos:
                statement=statement+self.green(letter, 'l'+str(pos), self.table, cursor)

            if pos != 4:
                statement= statement+ ' INTERSECT '


        #print(statement)
        self.update_table(statement)
        
    def update_table(self, statement):
        '''updates the table of possible guesses. I'm thinking there's definitely a cleaner way to do this... TODO make this suck less'''
        self.cursor.execute("DROP TABLE newclone;")
        self.cursor.execute('''CREATE TABLE newclone(
                    l0 char(1),
                    l1 char(1),
                    l2 char(1),
                    l3 char(1),
                    l4 char(1)
                    ); ''')
        
        statement="INSERT INTO newclone " + statement + ";"
        #print(statement)
        self.cursor.execute(statement)
        
        self.cursor.execute("DROP TABLE clone;")
        self.cursor.execute("ALTER TABLE newclone RENAME TO clone;")
       

    