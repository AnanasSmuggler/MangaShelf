import sqlite3
import os

class Database():
    
        def __init__(self, dbPth: str, imgPth: str) -> None:
                self.dbPath = dbPth
                self.imgPath = imgPth
                self.connection = None
                self.cursor = None
                self.currentUserId = 1
                
                self.connect()
                
                if self.is_db_empty():
                    self.create_db_structure()
                    
                if self.no_users():
                    self.currentUserId = -1
                else:
                    self.currentUserId = 1
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
            
            try:
                self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
                tables = self.cursor.fetchall()
                
                return not bool(tables)
            except sqlite3.Error as e:
                print(e)
            
            return 0
        
        #Method creates basic structure of apps database (four tables: users, series, volumes, collections)
        def create_db_structure(self) -> None:
            
            try:
                self.cursor.execute('''CREATE TABLE IF NOT EXISTS users
                                (id INTEGER PRIMARY KEY NOT NULL,
                                name TEXT NOT NULL,
                                avatar BLOB,
                                series_amount INTEGER NOT NULL,
                                volumes_amount INTEGER NOT NULL
                );''')
                self.cursor.execute('''CREATE TABLE IF NOT EXISTS series
                                (id INTEGER PRIMARY KEY NOT NULL,
                                title TEXT NOT NULL,
                                art TEXT NOT NULL,
                                story TEXT NOT NULL,
                                publisher TEXT NOT NULL,
                                volumes_published INTEGER NOT NULL,
                                is_finished INTEGER NOT NULL,
                                logo BLOB not null
                );''')
                self.cursor.execute('''CREATE TABLE IF NOT EXISTS volumes
                                (id INTEGER PRIMARY KEY NOT NULL,
                                title TEXT NOT NULL,
                                series_id INT NOT NULL,
                                front_page BLOB NOT NULL,
                                FOREIGN KEY (series_id) REFERENCES series(id)
                );''')
                self.cursor.execute('''CREATE TABLE IF NOT EXISTS collections
                                (id INTEGER PRIMARY KEY NOT NULL,
                                series_id INT NOT NULL,
                                volume_id INT NOT NULL,
                                user_id INT NOT NULL,
                                read INT NOT NULL,
                                borrowed INT NOT NULL,
                                borrower INT,
                                FOREIGN KEY (series_id) REFERENCES series(id),
                                FOREIGN KEY (volume_id) REFERENCES volumes(id),
                                FOREIGN KEY (user_id) REFERENCES users(id),
                                FOREIGN KEY (borrower) REFERENCES users(id)
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
        
        #Method converts digital data to binary format
        def convert_to_binary_data(self, filename: str) -> bytes:
            with open(filename, 'rb') as file:
                blobData = file.read()
                
            return blobData
        
        #Method converts binary data to proper format and write it on Hard Disk
        def write_to_file(self, data: bytes, filename: str) -> None:
            with open(filename, 'wb') as file:
                file.write(data)
            print(f"Stored blob data into: {filename}")
        
        #Adds user to database
        def add_user(self, userName: str, profilePicture: str) -> str:
            try:
                insertQuery = """INSERT INTO users (name, avatar, series_amount, volumes_amount) VALUES (?, ?, ?, ?);"""
                binaryData = self.convert_to_binary_data(profilePicture)
                dataTuple = (userName, binaryData, 0, 0)
                self.cursor.execute(insertQuery, dataTuple)
                self.write_to_file(binaryData, os.path.join(self.imgPath, f"{userName}PP.png"))
                self.connection.commit()
                self.currentUserId = self.get_user_id_by_user_name(userName)
                return "ok"
            except sqlite3.Error as e:
                
                return e
        
        def get_from_users(self) -> list:
            try:
                user = self.cursor.execute(f'''SELECT * FROM users WHERE id = {self.currentUserId};''')
                record = user.fetchone()
                return [record[1], record[2], record[3], record[4]]
            except sqlite3.Error as e:
                print(e)
                
            return []
        
        def get_all_user_names(self) -> list[str]:
            try:
                users = self.cursor.execute('''SELECT name FROM users;''')
                records = users.fetchall()
                return [records[i][0] for i in range(len(records))]
            except sqlite3.Error as e:
                print(e)
            return []
        
        def get_user_id_by_user_name(self, userName: str) -> int:
            try:
                user = self.cursor.execute(f'''SELECT id FROM users WHERE name = ?;''', (userName,))
                record = user.fetchone()
                return record[0]
            except sqlite3.Error as e:
                print(e)
                
            return -1
                
