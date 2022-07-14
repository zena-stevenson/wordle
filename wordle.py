#should really oop-ify all this- a "wordle" object is an individual game, with functions that do stuff like select the right answer, connect to the database of all possible, evaluate guesses, update database after a guess, etc. 

class Wordle:
    def __init__(self):        
        
        self.answer=self.set_answer()
        self.table=self.clone_table()
        
        self.connection = sqlite3.connect('wordle.db')
        self.cursor = self.connection.cursor()

    
    def set_answer(self):
        #eventually this will select a random word from the database. for now, just
        ans='SMALL'
        return(ans)
    
    def clone_table(self):
        #clone all_words so we can update the clone/ not alter the original
        connection = sqlite3.connect('wordle.db')
        cursor = connection.cursor()
        cursor.execute("DROP TABLE clone;") #clears out clone table from last game
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
        self.cursor.execute("SELECT * FROM clone;")
        ans=self.cursor.fetchall()
        for a in ans:
            print(a)
        
    def gray(self, letter, table, cursor): 
        statement = "SELECT * FROM "+table+" WHERE '"+letter+"' NOT IN (l0, l1, l2, l3, l4)"
        return(statement)
        

    def yellow(self, letter, position, table, cursor):
        statement = "SELECT * FROM "+table+" WHERE "+position+" != '"+letter+"' AND '"+letter+"' IN (l0, l1, l2, l3, l4)"
        return(statement)
        

    def green(self, letter, position, table, cursor):
        statement = "SELECT * FROM "+table+" WHERE "+position+" == '"+letter+"'"
        return(statement)
    
    def eval_guess(self, guess):
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
       

    