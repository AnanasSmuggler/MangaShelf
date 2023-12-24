import sqlite3

class Database():
    
        def __init__(self, dbPath: str) -> None:
                self.dbPath = dbPath
                self.connection = None
                self.cursor = None
                
                self.connect()
                
        def connect(self) -> None:
            try:
                self.connection = sqlite3.connect(self.dbPath)
                self.cursor = self.connection.cursor()
            except sqlite3.Error as e:
                print(e)
                
        def disconnect(self) -> None:
            if self.connection:
                self.connection.close()