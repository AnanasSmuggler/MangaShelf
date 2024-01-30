import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import os
from PIL import Image
from classes.database_handler import Database

class Gui(ctk.CTk):
    def __init__(self, imgPth: str, dbPth: str) -> None:
        super().__init__()
        
        self.database = Database(dbPth, imgPth)
        
        self.title("Manga Shelf")
        self.geometry("1280x720")
        self.resizable(width=False, height=False)
        
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

        self.homeFrameLabel = ctk.CTkLabel(self.homeFrame, text="Home Page", compound="left", font=ctk.CTkFont(size=55, weight="bold"))
        self.homeFrameLabel.grid(row=0, column=0, padx=20, pady=20)
        
        if self.database.no_users():
            self.homeFrameLabel = ctk.CTkLabel(self.homeFrame, text="There are currently no users in this MangaShelf. Let's change it:", compound="left", font=ctk.CTkFont(size=25, weight="bold"))
            self.homeFrameLabel.grid(row=1, column=0, padx=20, pady=20)

            self.addUserHomeButton = ctk.CTkButton(self.homeFrame, text="Add User", command=self.add_user_menu)
            self.addUserHomeButton.grid(row=2, column=0, padx=20, pady=20) 
        else:
            userData = self.database.get_from_users()
            self.ppImgPath = os.path.join(self.imagePath, f"{userData[0]}PP.png")
            if not os.path.exists(self.ppImgPath):
                self.database.write_to_file(userData[1], self.ppImgPath)
            self.currUserProfilePicture = ctk.CTkImage(light_image=Image.open(self.ppImgPath), size=(250,250))
            self.currUserProfilePictureLabel = ctk.CTkLabel(self.homeFrame, image=self.currUserProfilePicture, text="", compound="left")
            self.currUserProfilePictureLabel.grid(row=1, column=0, padx=20, pady=5, sticky="w")
            
            self.userNameLabel = ctk.CTkLabel(self.homeFrame, text=userData[0], compound="left", font=ctk.CTkFont(size=25, weight="bold"))
            self.userNameLabel.grid(row=2, column=0, sticky="w", padx=20, pady=5)
            
            self.seriesAmountLabel = ctk.CTkLabel(self.homeFrame, text=f"Series on shelf: {userData[2]}", compound="left", font=ctk.CTkFont(size=20, weight="bold"))
            self.seriesAmountLabel.grid(row=3, column=0, sticky="w", padx=20, pady=10)
            
            self.volumesAmountLabel = ctk.CTkLabel(self.homeFrame, text=f"Volumes on shelf: {userData[3]}", compound="left", font=ctk.CTkFont(size=20, weight="bold"))
            self.volumesAmountLabel.grid(row=4, column=0, sticky="w", padx=20, pady=10)
            
            self.homeOptionMenuLabel = ctk.CTkLabel(self.homeFrame, text=f"Change user: ", compound="left", font=ctk.CTkFont(size=20, weight="bold"))
            self.homeOptionMenuLabel.grid(row=5, column=0, sticky="w", padx=20, pady=10)
            
            self.homeOptionMenu = ctk.CTkOptionMenu(self.homeFrame, width=150, values=self.database.get_all_user_names(), command=self.homeMenu_callback)      
            self.homeOptionMenu.grid(row=6, column=0, sticky="w", padx=20)
            
            
        
    def create_listFrame(self) -> None:
        self.listFrame = ctk.CTkFrame(self, corner_radius = 0, fg_color="transparent")
        self.listFrame.grid_columnconfigure(0, weight=1)

        self.listFrameLabel = ctk.CTkLabel(self.listFrame, text="Your Shelf", compound="left", font=ctk.CTkFont(size=55, weight="bold"))
        self.listFrameLabel.grid(row=0, column=0, padx=20, pady=20)
        
        if self.database.currentUserId == -1:
            self.listFrameNoUserLabel = ctk.CTkLabel(self.listFrame, text="No user selected", compound="left", font=ctk.CTkFont(size=25, weight="bold"))
            self.listFrameNoUserLabel.grid(row=1, column=0, padx=20, pady=20)
        
    def create_addFrame(self) -> None:
        self.addFrame = ctk.CTkFrame(self, corner_radius = 0, fg_color="transparent")
        self.addFrame.grid_columnconfigure(0, weight=1) 

        self.addFrameLabel = ctk.CTkLabel(self.addFrame, text="Add/Edit", compound="left", font=ctk.CTkFont(size=55, weight="bold"))
        self.addFrameLabel.grid(row=0, column=0, padx=20, pady=20)

        if self.database.no_users():
            self.addFrameNoUserLabel = ctk.CTkLabel(self.addFrame, text="Let's add first user to MangaShelf: ", compound="left", font=ctk.CTkFont(size=25, weight="bold"))
            self.addFrameNoUserLabel.grid(row=1, column=0, padx=20, pady=20)

            self.addUserButton = ctk.CTkButton(self.addFrame, text="Add User", command=self.add_user_menu)
            self.addUserButton.grid(row=2, column=0, padx=20, pady=20)
        else:  
            self.addSeriesButton = ctk.CTkButton(self.addFrame, text="Add Series", command=self.editProfileButton_handler)
            self.addSeriesButton.grid(row=1, column=0, sticky="w", padx=330, pady=20)

            self.editSeriesButton = ctk.CTkButton(self.addFrame, text="Edit Series", command=self.resetDbButton_handler)
            self.editSeriesButton.grid(row=1, column=0, sticky="e", padx=330, pady=20)     
            
            self.addVolumeButton = ctk.CTkButton(self.addFrame, text="Add Volume", command=self.editProfileButton_handler)
            self.addVolumeButton.grid(row=2, column=0, sticky="w", padx=330, pady=20)

            self.editVolumeButton = ctk.CTkButton(self.addFrame, text="Edit Series", command=self.resetDbButton_handler)
            self.editVolumeButton.grid(row=2, column=0, sticky="e", padx=330, pady=20)     
            
    def create_settingsFrame(self) -> None:
        self.settingsFrame = ctk.CTkFrame(self, corner_radius = 0, fg_color="transparent")
        self.settingsFrame.grid_columnconfigure(0, weight=1) 

        self.settingsFrameLabel = ctk.CTkLabel(self.settingsFrame, text="Settings", font=ctk.CTkFont(size=55, weight="bold"))
        self.settingsFrameLabel.grid(row=0, column=0, padx=20, pady=20) 

        self.settingsFrameComboboxLabel = ctk.CTkLabel(self.settingsFrame, text="Set appearance mode:", compound="left", font=ctk.CTkFont(size=20, weight="bold"))
        self.settingsFrameComboboxLabel.grid(row=1, column=0, sticky="w", padx=20, pady=20)

        self.displayOptionMenu = ctk.CTkOptionMenu(self.settingsFrame, values=["Light", "Dark", "System"], command=self.displayOptionMenu_callback)      
        self.displayOptionMenu.grid(row=1, column=0, sticky="w", padx=260, pady=20)

        self.displayOptionMenu.set("System")

        self.settingsAddProfileButton = ctk.CTkButton(self.settingsFrame, text="Add Profile", command=self.add_user_menu)
        self.settingsAddProfileButton.grid(row=3, column=0, sticky="w", padx=20, pady=20)

        self.editProfileButton = ctk.CTkButton(self.settingsFrame, text="Edit Profiles", command=self.editProfileButton_handler)
        self.editProfileButton.grid(row=3, column=0, sticky="w", padx=180, pady=20)

        self.resetDbButton = ctk.CTkButton(self.settingsFrame, text="Reset Database", command=self.resetDbButton_handler)
        self.resetDbButton.grid(row=4, column=0, sticky="w", padx=20, pady=20)

    def homeMenu_callback(self, choice) -> None:
        self.database.currentUserId = self.database.get_user_id_by_user_name(choice)
        self.refresh_home_frame()
        self.homeOptionMenu.set(choice)
        

    def displayOptionMenu_callback(self, choice) -> None:
        ctk.set_appearance_mode(choice.lower())

    def editProfileButton_handler(self) -> None:
        print("editProfileButton_handler")

    def resetDbButton_handler(self) -> None:
        print("resetDbButton_handler")

    def refresh_home_frame(self) -> None:
        self.homeFrame.destroy()
        self.create_homeFrame()
        self.select_frame_by_name("home")
        
    def refresh_add_frame(self) -> None:
        self.addFrame.destroy()
        self.create_addFrame()

    def is_square_image(self, file_path: str) -> bool:
        try:
            with Image.open(file_path) as img:
                width, height = img.size
                return width == height
        except Exception as e:
            print(f"Error: {e}")
            return False

    def browse_image(self)-> None:
        filename = ctk.filedialog.askopenfilename(initialdir="/", title="Select Image", filetypes=(("Image files", "*.png;*.jpg;*.jpeg;*.gif"), ("all files", "*.*")))
        if filename:
            if self.is_square_image(filename):
                self.userImageEntryVar.set(filename)
            else:
                CTkMessagebox(title="Error", message="Please provide squared image!", icon="cancel")


    def add_user_menu(self) -> None:
        self.addUserWindow = ctk.CTkToplevel(self)
        self.addUserWindow.title("Add User")
        self.addUserWindow.geometry("600x400")
        self.addUserWindow.grab_set()

        self.addUserWindowLabel = ctk.CTkLabel(self.addUserWindow, text="Add User:", font=ctk.CTkFont(size=35, weight="bold"))
        self.addUserWindowLabel.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        self.addUserWindowNameLabel = ctk.CTkLabel(self.addUserWindow, text="User name:", font=ctk.CTkFont(size=25))
        self.addUserWindowNameLabel.grid(row=1, column=0, padx=20, pady=20)

        userNamePrompt = ctk.CTkEntry(self.addUserWindow, corner_radius=3.5)
        userNamePrompt.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)

        self.addUserWindowImageLabel = ctk.CTkLabel(self.addUserWindow, text="Profile image:", font=ctk.CTkFont(size=25))
        self.addUserWindowImageLabel.grid(row=2, column=0, padx=20, pady=20)

        self.userImageEntryVar = ctk.StringVar()
        self.addUserWindowImageEntry = ctk.CTkEntry(self.addUserWindow, textvariable=self.userImageEntryVar, state="readonly", corner_radius=3.5)
        self.addUserWindowImageEntry.grid(row=2, column=1, sticky="nsew", padx=20, pady=20)

        addUserImageBrowseButton = ctk.CTkButton(self.addUserWindow, text="Browse Image", command=self.browse_image)
        addUserImageBrowseButton.grid(row=2, column=2, sticky="nsew", padx=20, pady=20)

        addUserSubmitButton = ctk.CTkButton(self.addUserWindow, text="Submit", command=lambda: self.add_user_to_database(userNamePrompt.get(), self.userImageEntryVar.get()))
        addUserSubmitButton.grid(row=3, column=0, sticky="nsew", padx=20, pady=20)
        
        addUserExitButton = ctk.CTkButton(self.addUserWindow, text="Cancel", command=lambda: self.addUserWindow.destroy())
        addUserExitButton.grid(row=3, column=1, sticky="nsew", padx=20, pady=20)

    def add_user_to_database(self, userName: str, profilePicture: str) -> None:
        self.addUserWindow.destroy()
        userNames = self.database.get_all_user_names()
        if userName in userNames:
            CTkMessagebox(title="Error", message=f"Error: There is user with this username in database!", icon="cancel")
        else:
            databaseResponse = self.database.add_user(userName, profilePicture)
            if databaseResponse == "ok":
                CTkMessagebox(title="Success", message="User has been added to MangaShelf", icon="check", option_1="Ok")
                self.refresh_home_frame()
                self.refresh_add_frame()
                self.select_frame_by_name("home")
            else:
                CTkMessagebox(title="Error", message=f"Error: {databaseResponse}", icon="cancel")
            
            
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
        