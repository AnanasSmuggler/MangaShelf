import sqlite3

class Database():
    
        def __init__(self, dbPath: str) -> None:
                self.dbPath = dbPath
                self.connection = None
                self.cursor = None
                
                self.connect()
                if self.is_db_empty():
                    self.create_db_structure()
                    
        #Method connects with database       
        def connect(self) -> None:
            try:
                self.connection = sqlite3.connect(self.dbPath)
                self.cursor = self.connection.cursor()
            except sqlite3.Error as e:
                print(e)
        
        #Method disconnects with database  
        def disconnect(self) -> None:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
        
        #Method checks if database has no user made tables        
        def is_db_empty(self) -> bool:
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
            tables = self.cursor.fetchall()
            
            return not bool(tables)
        
        #Method creates basic structure of apps database (four tables: users, series, volumes, collections)
        def create_db_structure(self) -> None:
            try:
                self.cursor.execute('''CREATE TABLE IF NOT EXISTS users
                                (id INT PRIMARY KEY NOT NULL,
                                name TEXT NOT NULL,
                                avatar BLOB,
                                series_amount INTEGER NOT NULL,
                                volumes_amount INTEGER NOT NULL
                );''')
                self.cursor.execute('''CREATE TABLE IF NOT EXISTS series
                                (id INT PRIMARY KEY NOT NULL,
                                title TEXT NOT NULL,
                                art TEXT NOT NULL,
                                story TEXT NOT NULL,
                                publisher TEXT NOT NULL,
                                volumes_published INTEGER NOT NULL,
                                is_finished INTEGER NOT NULL,
                                logo BLOB not null
                );''')
                self.cursor.execute('''CREATE TABLE IF NOT EXISTS volumes
                                (id INT PRIMARY KEY NOT NULL,
                                title TEXT NOT NULL,
                                series_id INT NOT NULL,
                                front_page BLOB NOT NULL,
                                FOREIGN KEY (series_id) REFERENCES series(id)
                );''')
                self.cursor.execute('''CREATE TABLE IF NOT EXISTS collections
                                (id INT PRIMARY KEY NOT NULL,
                                series_id INT NOT NULL,
                                volume_id INT NOT NULL,
                                user_id INT NOT NULL,
                                read INT NOT NULL,
                                borrowed INT NOT NULL,
                                borrower INT,
                                FOREIGN KEY (series_id) REFERENCES series(id),
                                FOREIGN KEY (volume_id) REFERENCES volumes(id),
                                FOREIGN KEY (user_id) REFERENCES user(id),
                                FOREIGN KEY (borrower) REFERENCES user(id)
                );''')
            except sqlite3.Error as e:
                print(e)
        
        #Method returns True if there are no users in users table        
        def no_users(self) -> bool:
            try:
                usersCountSelect = self.cursor.execute('''SELECT * FROM users LIMIT 1;''')
                usersCount = usersCountSelect.fetchall()
                return True if len(usersCount) == 0 else False
            except sqlite3.Error as e:
                print(e)
                
            return True