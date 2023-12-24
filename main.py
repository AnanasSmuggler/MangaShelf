from classes.gui import Gui
import os
    
def close_app(app: Gui) -> None:
    app.database.disconnect()
    app.destroy()
    
def main() -> None:
    imagePath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
    databasePath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "database.db")
    app = Gui(imagePath, databasePath)
    app.protocol("WM_DELETE_WINDOW", lambda: close_app(app))
    app.mainloop()
    
if __name__ == "__main__":
    main()