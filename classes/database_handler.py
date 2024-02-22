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
                                is_active INT NOT NULL,
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
                self.write_to_file(binaryData, os.path.join(self.imgPath, f"profile_pictures\\{userName}PP.png"))
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
        
        def update_user(self, newUserName: str, oldUserName: str, profilePicture: str) -> str:
            try:
                updateQuery = """UPDATE users SET name = ?, avatar = ? WHERE id = ?;"""
                binaryData = self.convert_to_binary_data(profilePicture)
                dataTuple = (newUserName, binaryData, self.get_user_id_by_user_name(oldUserName))
                self.cursor.execute(updateQuery, dataTuple)
                self.write_to_file(binaryData, os.path.join(self.imgPath, f"profile_pictures\\{newUserName}PP.png"))
                self.connection.commit()
                self.currentUserId = self.get_user_id_by_user_name(newUserName)
                return "ok"
            except sqlite3.Error as e:
                return e
            
        def reset_db(self) -> str:
            try:
                tables = self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
                
                for table in tables:
                    tableName = table[0]
                    self.cursor.execute(f"DELETE FROM {tableName};")
                    
                self.connection.commit()
                return "ok"
            except sqlite3.Error as e:
                return e
            
        def add_series(self, title: str, art: str, story: str, publisher: str, volumes: int, finished: int, logo: str) -> str:
            try:
                insertQuery = """INSERT INTO series (title, art, story, publisher, volumes_published, is_finished, logo) VALUES (?, ?, ?, ?, ?, ?, ?);"""
                binaryData = self.convert_to_binary_data(logo)
                dataTuple = (title, art, story, publisher, volumes, finished, binaryData)
                self.cursor.execute(insertQuery, dataTuple)
                self.write_to_file(binaryData, os.path.join(self.imgPath, f"series_logos\\{title.lower().replace(' ', '_')}SL.png"))
                self.connection.commit()
                return "ok"
            except sqlite3.Error as e:
                return e
        
        def get_all_series(self) -> list[list[str]]:
            try:
                series = self.cursor.execute('''SELECT * FROM series ORDER BY title;''')
                records = series.fetchall()
                return [[record[1], record[2], record[3], record[4], record[5], record[6], record[7]] for record in records]
            except sqlite3.Error as e:
                print(e)
            
            return []
            
        def get_all_series_names(self) -> list[str]:
            try:
                users = self.cursor.execute('''SELECT title FROM series ORDER BY title ASC;''')
                records = users.fetchall()
                return [records[i][0] for i in range(len(records))]
            except sqlite3.Error as e:
                print(e)
            return []
        
        def get_series_with_volumes(self) -> list[str]:
            try:
                series = self.cursor.execute('''SELECT title FROM series WHERE id IN (SELECT DISTINCT series_id FROM volumes) ORDER BY title ASC;''')
                records = series.fetchall()
                return [record[0] for record in records]
            except sqlite3.Error as e:
                print(e)
            return []
        
        def get_series_volumes(self, seriesName: str) -> list[list]:
            try:
                volumes = self.cursor.execute('''SELECT title, id FROM volumes WHERE series_id = ?;''', (str(self.get_series_id_by_series_title(seriesName))))
                records = volumes.fetchall()
                return [[record[0], record[1]] for record in records]
            except sqlite3.Error as e:
                print(e)
            return []

        def get_current_user_series(self) -> list[str]:
            try:
                userSeries = self.cursor.execute('''SELECT * FROM series WHERE id IN (SELECT DISTINCT series_id FROM collections WHERE user_id = ?);''', (self.currentUserId,))
                records = userSeries.fetchall()
                return [[record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7]] for record in records]
            except sqlite3.Error as e:
                print(e)
            return []

        def get_series_id_by_series_title(self, title: str) -> int:
            try:
                user = self.cursor.execute(f'''SELECT id FROM series WHERE title = ?;''', (title,))
                record = user.fetchone()
                return record[0]
            except sqlite3.Error as e:
                print(e)
                
            return -1
        
        def check_collection_active(self, id: int) -> bool:
            try:
                query = self.cursor.execute('''SELECT is_active FROM collections WHERE id = ?;''', (id,))
                return query.fetchone()[0]
            except sqlite3.Error as e:
                print(e)
            return False

        def switch_volume_active(self, vol_id: int, active: int) -> str:
            try:
                query = '''UPDATE collections SET is_active = ? WHERE id = ?;'''
                dataTuple = (active, vol_id)
                self.cursor.execute(query, dataTuple)
                self.connection.commit()
                return "ok"
            except sqlite3.Error as e:
                return e


        def check_collection_record(self, seriesName: str, volumeId: int, userName: str) -> list:
            seriesId = self.get_series_id_by_series_title(seriesName)
            userId = self.get_user_id_by_user_name(userName)
            try:
                query = self.cursor.execute('''SELECT id FROM collections WHERE series_id = ? AND volume_id = ? AND user_id = ?;''', (seriesId, volumeId, userId))
                record = query.fetchone()
                
                return [True, record[0]] if record != None else [False, []]
            except sqlite3.Error as e:
                print(e)
            return []

        def get_user_volumes_of_series(self, seriesId: int) -> list[list[str]]:
            try:
                volumes = self.cursor.execute('''SELECT * FROM volumes WHERE id IN (SELECT volume_id FROM collections WHERE series_id = ? AND user_id = ? AND is_active = 1);''', (seriesId, self.currentUserId))
                records = volumes.fetchall()
                finalList = [[records[i][0], records[i][1], records[i][3]] for i in range(len(records))]
                read_borrow = '''SELECT read, borrowed, borrower FROM collections WHERE series_id = ? AND user_id = ? AND volume_id = ?;'''
                for i in finalList:
                    dataTuple = (seriesId, self.currentUserId, i[0])
                    new_records = self.cursor.execute(read_borrow, dataTuple).fetchall()
                    for j in new_records:
                        i.append(j[0])
                        i.append(j[1])
                        i.append(j[2])
                return finalList
            except sqlite3.Error as e:
                print(e)
            return []

        def get_from_series(self, id: int) -> list:
            try:
                series = self.cursor.execute(f'''SELECT * FROM series WHERE id = {id};''')
                record = series.fetchone()
                return [record[1], record[2], record[3], record[4], record[5], record[6], record[7]]
            except sqlite3.Error as e:
                print(e)
                
            return []
        
        def update_series(self, newTitle: str, oldTitle: str, art: str, story: str, publisher: str, volumes: int, finished: int, logo: str) -> str:
            try:
                updateQuery = """UPDATE series SET title = ?, art = ?, story = ?, publisher = ?, volumes_published = ?, is_finished = ?, logo = ?  WHERE id = ?;"""
                binaryData = self.convert_to_binary_data(logo)
                dataTuple = (newTitle, art, story, publisher, volumes, finished, binaryData, self.get_series_id_by_series_title(oldTitle))
                self.cursor.execute(updateQuery, dataTuple)
                if newTitle != oldTitle:
                    self.change_series_dir_name(os.path.join(self.imgPath, f"series_logos\\{oldTitle.lower().replace(' ', '_')}SL.png"), os.path.join(self.imgPath, f"series_logos\\{newTitle.lower().replace(' ', '_')}SL.png"))
                    if os.path.exists(os.path.join(self.imgPath, f"volumes_covers\\{oldTitle.lower().replace(' ', '_')}")):
                        self.change_series_dir_name(os.path.join(self.imgPath, f"volumes_covers\\{oldTitle.lower().replace(' ', '_')}"), os.path.join(self.imgPath, f"volumes_covers\\{newTitle.lower().replace(' ', '_')}"))
                self.connection.commit()
                return "ok"
            except sqlite3.Error as e:
                return e
            
        def get_volumes_from_series(self, seriesId: int) -> list[str]:
            try:
                users = self.cursor.execute('''SELECT title FROM volumes WHERE series_id = ?;''', (seriesId,))
                records = users.fetchall()
                return [records[i][0] for i in range(len(records))]
            except sqlite3.Error as e:
                print(e)
            return []
        
        def add_volume(self, seriesId: int, seriesName: str, title: str, cover: str) -> str:
            try:
                insertQuery = """INSERT INTO volumes (title, series_id, front_page) VALUES (?, ?, ?);"""
                binaryData = self.convert_to_binary_data(cover)
                dataTuple = (title, seriesId, binaryData)
                self.cursor.execute(insertQuery, dataTuple)
                if not os.path.exists(os.path.join(self.imgPath, f"volumes_covers\\{seriesName.lower().replace(' ', '_')}")):
                    os.makedirs(os.path.join(self.imgPath, f"volumes_covers\\{seriesName.lower().replace(' ', '_')}"))
                self.write_to_file(binaryData, os.path.join(self.imgPath, f"volumes_covers\\{seriesName.lower().replace(' ', '_')}\\{title.lower().replace(' ', '_')}.png"))
                self.connection.commit()
                return "ok"
            except sqlite3.Error as e:
                return e
            
        def add_volume_to_collection(self, seriesName: str, volumeId: int, userName: str) -> str:
            seriesId = self.get_series_id_by_series_title(seriesName)
            userId = self.get_user_id_by_user_name(userName)
            try:
                insertQuery = '''INSERT INTO collections (series_id, volume_id, user_id, read, borrowed, borrower, is_active) VALUES (?, ?, ?, ?, ?, ?, ?);'''
                dataTuple = (seriesId, volumeId, userId, 0, 0, None, 1)
                self.cursor.execute(insertQuery, dataTuple)
                self.connection.commit()
                return "ok"
            except sqlite3.Error as e:
                return e
        
        def get_volume_id_by_title(self, seriesId: int, volumeName: str) -> int:
            try:
                volId = self.cursor.execute('''SELECT Id FROM volumes WHERE series_id = ? AND title = ?;''', (seriesId, volumeName))
                record = volId.fetchone()
                return record[0]
            except sqlite3.Error as e:
                print(e)
            return -1

        def update_volume(self, seriesId: int, seriesName: str, newTitle: str, oldTitle: str, cover: str) -> str:
            try:
                id = self.cursor.execute("""SELECT id FROM volumes WHERE title = ? AND series_id = ?;""", (oldTitle, seriesId,)).fetchall()[0][0]
                updateQuery = """UPDATE volumes SET title = ?, series_id = ?, front_page = ? WHERE id = ?;"""
                binaryData = self.convert_to_binary_data(cover)
                dataTuple = (newTitle, self.get_series_id_by_series_title(seriesName), binaryData, id)
                self.cursor.execute(updateQuery, dataTuple)
                self.write_to_file(binaryData, os.path.join(self.imgPath, f"volumes_covers\\{seriesName.lower().replace(' ', '_')}\\{newTitle.lower().replace(' ', '_')}.png"))
                self.connection.commit()
                return "ok"
            except sqlite3.Error as e:
                return e

        def change_series_dir_name(self, old: str, new: str):
            try:
                os.rename(old, new)
                print(f"Directory '{old}' has been renamed to '{new}' successfully.")
            except FileNotFoundError:
                print(f"Directory '{old}' not found.")
            except FileExistsError:
                print(f"Directory '{new}' already exists.")
