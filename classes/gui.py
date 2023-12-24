import customtkinter as ctk
import os
from PIL import Image
from classes.database_handler import Database

class Gui(ctk.CTk):
    def __init__(self, imgPth: str, dbPth: str) -> None:
        super().__init__()
        
        self.database = Database(dbPth)
        
        self.title("Manga Shelf")
        self.geometry("1280x720")
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.imagePath = imgPth
        
        self.homeImage = ctk.CTkImage(light_image = Image.open(os.path.join(self.imagePath, "home_dark.png")),
                                                 dark_image = Image.open(os.path.join(self.imagePath, "home_light.png")))
        self.listImage = ctk.CTkImage(light_image = Image.open(os.path.join(self.imagePath, "list_dark.png")),
                                                 dark_image = Image.open(os.path.join(self.imagePath, "list_light.png")))
        self.addImage = ctk.CTkImage(light_image = Image.open(os.path.join(self.imagePath, "add_dark.png")),
                                                 dark_image = Image.open(os.path.join(self.imagePath, "add_light.png")))
        self.settingsImage = ctk.CTkImage(light_image = Image.open(os.path.join(self.imagePath, "settings_dark.png")),
                                                 dark_image = Image.open(os.path.join(self.imagePath, "settings_light.png"))) 
        self.create_navigationFrame()
        self.create_homeFrame()
        self.create_listFrame()
        self.create_addFrame()
        self.create_settingsFrame()
        self.select_frame_by_name("home")
        
    # Creates navigation frame with buttons linked to other frames in the app    
    def create_navigationFrame(self) -> None:
        self.navigationFrame = ctk.CTkFrame(self, corner_radius = 0)
        self.navigationFrame.grid(row = 0, column = 0, sticky = "nsew")
        self.navigationFrame.grid_rowconfigure(5, weight=1)
        
        self.navigationFrameLabel = ctk.CTkLabel(self.navigationFrame, text="Manga Shelf", compound="left", font=ctk.CTkFont(size=25, weight="bold"))
        self.navigationFrameLabel.grid(row=0, column=0, padx=20, pady=20)
        
        
        # Creating navigation buttons - home, list, add/edit, settings
        self.homeButton = ctk.CTkButton(self.navigationFrame, corner_radius=0, height=50, border_spacing=20, text="Home", fg_color="transparent",
                                         text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), image=self.homeImage, anchor="w", command=self.home_nav_button_event)
        self.homeButton.grid(row=1, column=0, sticky="ew")
        
        self.listButton = ctk.CTkButton(self.navigationFrame, corner_radius=0, height=50, border_spacing=20, text="Your Shelf", fg_color="transparent",
                                         text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), image=self.listImage, anchor="w", command=self.list_nav_button_event)
        self.listButton.grid(row=2, column=0, sticky="ew")
        
        self.addButton = ctk.CTkButton(self.navigationFrame, corner_radius=0, height=50, border_spacing=20, text="Add/Edit", fg_color="transparent",
                                         text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), image=self.addImage, anchor="w", command=self.add_nav_button_event)
        self.addButton.grid(row=3, column=0, sticky="ew")
        
        self.settingsButton = ctk.CTkButton(self.navigationFrame, corner_radius=0, height=50, border_spacing=20, text="Settings", fg_color="transparent",
                                         text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), image=self.settingsImage, anchor="w", command=self.settings_nav_button_event)
        self.settingsButton.grid(row=4, column=0, sticky="ew")
    
    def create_homeFrame(self) -> None:
        self.homeFrame = ctk.CTkFrame(self, corner_radius = 0, fg_color="transparent")
        self.homeFrame.grid_columnconfigure(0, weight=1)
        
    def create_listFrame(self) -> None:
        self.listFrame = ctk.CTkFrame(self, corner_radius = 0, fg_color="transparent")
        self.listFrame.grid_columnconfigure(0, weight=1)
        
    def create_addFrame(self) -> None:
        self.addFrame = ctk.CTkFrame(self, corner_radius = 0, fg_color="transparent")
        self.addFrame.grid_columnconfigure(0, weight=1)      
        
    def create_settingsFrame(self) -> None:
        self.settingsFrame = ctk.CTkFrame(self, corner_radius = 0, fg_color="transparent")
        self.settingsFrame.grid_columnconfigure(0, weight=1)              

    #Navigational button events    
    def home_nav_button_event(self) -> None:
        self.select_frame_by_name("home")
        
    def list_nav_button_event(self) -> None:
        self.select_frame_by_name("list")
        
    def add_nav_button_event(self) -> None:
        self.select_frame_by_name("add")
        
    def settings_nav_button_event(self) -> None:
        self.select_frame_by_name("settings")
    
    #Sets button color and shows selected frame    
    def select_frame_by_name(self, name: str) -> None:
        
        self.homeButton.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.listButton.configure(fg_color=("gray75", "gray25") if name == "list" else "transparent")
        self.addButton.configure(fg_color=("gray75", "gray25") if name == "add" else "transparent")
        self.settingsButton.configure(fg_color=("gray75", "gray25") if name == "settings" else "transparent")
        
        self.homeFrame.grid(row=0, column=1, sticky="nsew") if name == "home" else self.homeFrame.grid_forget()
        self.listFrame.grid(row=0, column=1, sticky="nsew") if name == "list" else self.listFrame.grid_forget()
        self.addFrame.grid(row=0, column=1, sticky="nsew") if name == "add" else self.addFrame.grid_forget()
        self.settingsFrame.grid(row=0, column=1, sticky="nsew") if name == "settings" else self.settingsFrame.grid_forget()
        