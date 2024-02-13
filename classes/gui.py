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
        
        self.homeImage = ctk.CTkImage(light_image = Image.open(os.path.join(self.imagePath, "func_images\\home_dark.png")),
                                                 dark_image = Image.open(os.path.join(self.imagePath, "func_images\\home_light.png")))
        self.listImage = ctk.CTkImage(light_image = Image.open(os.path.join(self.imagePath, "func_images\\list_dark.png")),
                                                 dark_image = Image.open(os.path.join(self.imagePath, "func_images\\list_light.png")))
        self.addImage = ctk.CTkImage(light_image = Image.open(os.path.join(self.imagePath, "func_images\\add_dark.png")),
                                                 dark_image = Image.open(os.path.join(self.imagePath, "func_images\\add_light.png")))
        self.settingsImage = ctk.CTkImage(light_image = Image.open(os.path.join(self.imagePath, "func_images\\settings_dark.png")),
                                                 dark_image = Image.open(os.path.join(self.imagePath, "func_images\\settings_light.png"))) 
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
            self.ppImgPath = os.path.join(self.imagePath, f"profile_pictures\\{userData[0]}PP.png")
            if not os.path.exists(self.ppImgPath):
                self.database.write_to_file(userData[1], self.ppImgPath)
            self.currUserProfilePicture = ctk.CTkImage(light_image=Image.open(self.ppImgPath), size=(200,200))
            self.currUserProfilePictureLabel = ctk.CTkLabel(self.homeFrame, image=self.currUserProfilePicture, text="", compound="left")
            self.currUserProfilePictureLabel.grid(row=1, column=0, padx=20, pady=5, sticky="w")
            
            self.collectionProggresLabel = ctk.CTkLabel(self.homeFrame, text="Collection progress:", font=ctk.CTkFont(size=35, weight="bold"))
            self.collectionProggresLabel.grid(row=2, column=1, sticky="nsew", padx=20)
            
            self.placeholderHome = ctk.CTkLabel(self.homeFrame, text="", font=ctk.CTkFont(size=25, weight="bold"))
            self.placeholderHome.grid(row=2, column=2, sticky="nsew", padx=70)
            
            if userData[2] == 0:
                self.collectionProggresLabel = ctk.CTkLabel(self.homeFrame, text="Currently you have no volumes on shelf", font=ctk.CTkFont(size=25, weight="bold"))
                self.collectionProggresLabel.grid(row=3, column=1, sticky="w", padx=20)
            
            self.readingProggresLabel = ctk.CTkLabel(self.homeFrame, text="Reading progress:", font=ctk.CTkFont(size=35, weight="bold"))
            self.readingProggresLabel.grid(row=4, column=1, sticky="nsew", padx=20)
            
            self.placeholderHome2 = ctk.CTkLabel(self.homeFrame, text="", font=ctk.CTkFont(size=25, weight="bold"))
            self.placeholderHome2.grid(row=4, column=2, sticky="nsew", padx=70)
            
            if userData[3] == 0:
                self.collectionProggresLabel = ctk.CTkLabel(self.homeFrame, text="Currently you have no volumes on shelf", font=ctk.CTkFont(size=25, weight="bold"))
                self.collectionProggresLabel.grid(row=5, column=1, sticky="w", padx=20)
            
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
        self.listFrameLabel.grid(row=0, column=0, sticky="nsew", pady=20)
        
        if self.database.currentUserId == -1:
            self.listFrameNoUserLabel = ctk.CTkLabel(self.listFrame, text="No user selected", compound="left", font=ctk.CTkFont(size=25, weight="bold"))
            self.listFrameNoUserLabel.grid(row=1, column=0, padx=20, pady=20)
        else:
            self.allSeries = self.database.get_all_series()           
            for i in range(len(self.allSeries)):
                buttonImage = ctk.CTkImage(light_image = Image.open(os.path.join(self.imagePath, f"series_logos\\{self.allSeries[i][0].lower().replace(' ', '_')}SL.png")), size=(100,100))
                if self.allSeries[i][1] == self.allSeries[i][2]:
                    buttonText = f"{self.allSeries[i][0]} | {self.allSeries[i][1]}"
                else:
                    buttonText = f"{self.allSeries[i][0]} | {self.allSeries[i][1]}, {self.allSeries[i][2]}"
                seriesButton = ctk.CTkButton(self.listFrame, corner_radius=0, height=120, border_spacing=20, text=buttonText, fg_color="transparent",
                                            text_color=("gray10", "gray90"), font=ctk.CTkFont(size=25, weight="bold"), hover_color=("gray70", "gray30"), image=buttonImage, anchor="w", command=self.listButton)
                seriesButton.grid(row=i+1, column=0, sticky="ew")
                

                #title = ctk.CTkLabel(self.listFrame, text=self.allSeries[i][0], compound="left", font=ctk.CTkFont(size=12, weight="bold"))
                #title.grid(row=3+i, column=1, padx=20, pady=20)
        
    def listButton(self) -> None:
        print("listButton")
        
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
            self.addSeriesButton = ctk.CTkButton(self.addFrame, text="Add Series", command=self.add_series_menu)
            self.addSeriesButton.grid(row=1, column=0, sticky="w", padx=330, pady=20)

            self.editSeriesButton = ctk.CTkButton(self.addFrame, text="Edit Series", command=self.edit_series_menu)
            self.editSeriesButton.grid(row=1, column=0, sticky="e", padx=330, pady=20)     
            
            self.addVolumeButton = ctk.CTkButton(self.addFrame, text="Add Volume", command=self.add_volume_menu)
            self.addVolumeButton.grid(row=2, column=0, sticky="w", padx=330, pady=20)

            self.editVolumeButton = ctk.CTkButton(self.addFrame, text="Edit Volume", command=self.edit_volume_menu)
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

        self.editProfileButton = ctk.CTkButton(self.settingsFrame, text="Edit Profiles", command=self.editProfileButton_menu)
        self.editProfileButton.grid(row=3, column=0, sticky="w", padx=180, pady=20)

        self.resetDbButton = ctk.CTkButton(self.settingsFrame, text="Reset Database", command=self.resetDbButton_handler)
        self.resetDbButton.grid(row=4, column=0, sticky="w", padx=20, pady=20)

    def homeMenu_callback(self, choice) -> None:
        self.database.currentUserId = self.database.get_user_id_by_user_name(choice)
        self.refresh_home_frame()
        self.homeOptionMenu.set(choice)
        

    def displayOptionMenu_callback(self, choice) -> None:
        ctk.set_appearance_mode(choice.lower())

    def add_series_menu(self) -> None:
        self.addSeriesWindow = ctk.CTkToplevel(self)
        self.addSeriesWindow.title("Add Series")
        self.addSeriesWindow.geometry("700x700")
        self.addSeriesWindow.grab_set()

        self.addSeriesWindowLabel = ctk.CTkLabel(self.addSeriesWindow, text="Add Series", font=ctk.CTkFont(size=35, weight="bold"))
        self.addSeriesWindowLabel.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        self.addSeriesTitleLabel = ctk.CTkLabel(self.addSeriesWindow, text="Title: ", font=ctk.CTkFont(size=25))
        self.addSeriesTitleLabel.grid(row=1, column=0, padx=20, pady=20)
        
        self.addSeriesTitlePrompt = ctk.CTkEntry(self.addSeriesWindow, corner_radius=3.5)
        self.addSeriesTitlePrompt.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)
        
        self.addSeriesArtLabel = ctk.CTkLabel(self.addSeriesWindow, text="Art: ", font=ctk.CTkFont(size=25))
        self.addSeriesArtLabel.grid(row=2, column=0, padx=20, pady=20)
        
        self.addSeriesArtPrompt = ctk.CTkEntry(self.addSeriesWindow, corner_radius=3.5)
        self.addSeriesArtPrompt.grid(row=2, column=1, sticky="nsew", padx=20, pady=20)
        
        self.addSeriesStoryLabel = ctk.CTkLabel(self.addSeriesWindow, text="Story: ", font=ctk.CTkFont(size=25))
        self.addSeriesStoryLabel.grid(row=3, column=0, padx=20, pady=20)
        
        self.addSeriesStoryPrompt = ctk.CTkEntry(self.addSeriesWindow, corner_radius=3.5)
        self.addSeriesStoryPrompt.grid(row=3, column=1, sticky="nsew", padx=20, pady=20)
        
        self.addSeriesPublisherLabel = ctk.CTkLabel(self.addSeriesWindow, text="Publisher: ", font=ctk.CTkFont(size=25))
        self.addSeriesPublisherLabel.grid(row=4, column=0, padx=20, pady=20)
        
        self.addSeriesPublisherPrompt = ctk.CTkEntry(self.addSeriesWindow, corner_radius=3.5)
        self.addSeriesPublisherPrompt.grid(row=4, column=1, sticky="nsew", padx=20, pady=20)
        
        self.addSeriesVolumesPublishedLabel = ctk.CTkLabel(self.addSeriesWindow, text="Volumes published: ", font=ctk.CTkFont(size=25))
        self.addSeriesVolumesPublishedLabel.grid(row=5, column=0, padx=20, pady=20)
        
        self.addSeriesVolumesPublishedPrompt = ctk.CTkEntry(self.addSeriesWindow, corner_radius=3.5)
        self.addSeriesVolumesPublishedPrompt.grid(row=5, column=1, sticky="nsew", padx=20, pady=20)
        
        self.addSeriesOnGoingLabel = ctk.CTkLabel(self.addSeriesWindow, text="On Going", font=ctk.CTkFont(size=25))
        self.addSeriesOnGoingLabel.grid(row=6, column=0, padx=20, pady=20)
        
        switch_var = ctk.StringVar(value="0")
        
        self.addSeriesSwitch = ctk.CTkSwitch(self.addSeriesWindow, text="", variable=switch_var, onvalue="1", offvalue="0")
        self.addSeriesSwitch.grid(row=6, column=1, sticky="nsew", padx=20, pady=20)
            
        self.addSeriesFinishedLabel = ctk.CTkLabel(self.addSeriesWindow, text="Finished", font=ctk.CTkFont(size=25))
        self.addSeriesFinishedLabel.grid(row=6, column=2, padx=20, pady=20)
        
        self.addSeriesLogoLabel = ctk.CTkLabel(self.addSeriesWindow, text="Logo: ", font=ctk.CTkFont(size=25))
        self.addSeriesLogoLabel.grid(row=7, column=0, padx=20, pady=20)
        
        self.seriesImageEntryVar = ctk.StringVar()
        self.addSeriesWindowImageEntry = ctk.CTkEntry(self.addSeriesWindow, textvariable=self.seriesImageEntryVar, state="readonly", corner_radius=3.5)
        self.addSeriesWindowImageEntry.grid(row=7, column=1, sticky="nsew", padx=20, pady=20)
        
        self.addSeriesImageBrowseButton = ctk.CTkButton(self.addSeriesWindow, text="Browse Image", command=lambda: self.browse_square_image(self.seriesImageEntryVar))
        self.addSeriesImageBrowseButton.grid(row=7, column=2, sticky="nsew", padx=20, pady=20)
        
        self.addSeriesSubmitButton = ctk.CTkButton(self.addSeriesWindow, text="Submit", command=lambda: self.submit_series(self.addSeriesTitlePrompt.get(), self.addSeriesArtPrompt.get(), self.addSeriesStoryPrompt.get(), self.addSeriesPublisherPrompt.get(), self.addSeriesVolumesPublishedPrompt.get(), switch_var.get(), self.seriesImageEntryVar.get()))
        self.addSeriesSubmitButton.grid(row=8, column=1, sticky="nsew", padx=20, pady=20)
        
        self.addSeriesExitButton = ctk.CTkButton(self.addSeriesWindow, text="Cancel", command=lambda: self.addSeriesWindow.destroy())
        self.addSeriesExitButton.grid(row=8, column=2, sticky="nsew", padx=20, pady=20)

    def edit_series_menu(self) -> None:
        self.editSeriesWindow = ctk.CTkToplevel(self)
        self.editSeriesWindow.title("Edit Series")
        self.editSeriesWindow.geometry("900x800")
        self.editSeriesWindow.grab_set()

        self.editSeriesWindowLabel = ctk.CTkLabel(self.editSeriesWindow, text="Edit Series", font=ctk.CTkFont(size=35, weight="bold"))
        self.editSeriesWindowLabel.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        self.editSeriesWindowOptionLabel = ctk.CTkLabel(self.editSeriesWindow, text="Choose Series: ", font=ctk.CTkFont(size=35, weight="bold"))
        self.editSeriesWindowOptionLabel.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        
        self.editSeriesOptionMenu = ctk.CTkOptionMenu(self.editSeriesWindow, values=self.database.get_all_series_names(), command=self.editSeriesMenu_callback)
        self.editSeriesOptionMenu.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)

        self.chosenSeries = self.database.get_from_series(self.database.get_series_id_by_series_title(self.editSeriesOptionMenu.get()))

        self.editSeriesTitleLabel = ctk.CTkLabel(self.editSeriesWindow, text="Title: ", font=ctk.CTkFont(size=25))
        self.editSeriesTitleLabel.grid(row=2, column=0, padx=20, pady=20)

        self.editSeriesTitleEntryVar = ctk.StringVar()
        self.editSeriesTitleEntryVar.set(f"{self.chosenSeries[0]}")        
        self.editSeriesTitlePrompt = ctk.CTkEntry(self.editSeriesWindow, textvariable=self.editSeriesTitleEntryVar, corner_radius=3.5)
        self.editSeriesTitlePrompt.grid(row=2, column=1, sticky="nsew", padx=20, pady=20)
        
        self.editSeriesArtLabel = ctk.CTkLabel(self.editSeriesWindow, text="Art: ", font=ctk.CTkFont(size=25))
        self.editSeriesArtLabel.grid(row=3, column=0, padx=20, pady=20)
        
        self.editSeriesArtEntryVar = ctk.StringVar()
        self.editSeriesArtEntryVar.set(f"{self.chosenSeries[1]}")
        self.editSeriesArtPrompt = ctk.CTkEntry(self.editSeriesWindow, textvariable=self.editSeriesArtEntryVar, corner_radius=3.5)
        self.editSeriesArtPrompt.grid(row=3, column=1, sticky="nsew", padx=20, pady=20)
        
        self.editSeriesStoryLabel = ctk.CTkLabel(self.editSeriesWindow, text="Story: ", font=ctk.CTkFont(size=25))
        self.editSeriesStoryLabel.grid(row=4, column=0, padx=20, pady=20)
        
        self.editSeriesStoryEntryVar = ctk.StringVar()
        self.editSeriesStoryEntryVar.set(f"{self.chosenSeries[2]}")
        self.editSeriesStoryPrompt = ctk.CTkEntry(self.editSeriesWindow, textvariable=self.editSeriesStoryEntryVar, corner_radius=3.5)
        self.editSeriesStoryPrompt.grid(row=4, column=1, sticky="nsew", padx=20, pady=20)
        
        self.editSeriesPublisherLabel = ctk.CTkLabel(self.editSeriesWindow, text="Publisher: ", font=ctk.CTkFont(size=25))
        self.editSeriesPublisherLabel.grid(row=5, column=0, padx=20, pady=20)
        
        self.editSeriesPublisherEntryVar = ctk.StringVar()
        self.editSeriesPublisherEntryVar.set(f"{self.chosenSeries[3]}")
        self.editSeriesPublisherPrompt = ctk.CTkEntry(self.editSeriesWindow, textvariable=self.editSeriesPublisherEntryVar, corner_radius=3.5)
        self.editSeriesPublisherPrompt.grid(row=5, column=1, sticky="nsew", padx=20, pady=20)
        
        self.editSeriesVolumesPublishedLabel = ctk.CTkLabel(self.editSeriesWindow, text="Volumes published: ", font=ctk.CTkFont(size=25))
        self.editSeriesVolumesPublishedLabel.grid(row=6, column=0, padx=20, pady=20)
        
        self.editSeriesVolumesPublishedEntryVar = ctk.StringVar()
        self.editSeriesVolumesPublishedEntryVar.set(f"{self.chosenSeries[4]}")
        self.editSeriesVolumesPublishedPrompt = ctk.CTkEntry(self.editSeriesWindow, textvariable=self.editSeriesVolumesPublishedEntryVar, corner_radius=3.5)
        self.editSeriesVolumesPublishedPrompt.grid(row=6, column=1, sticky="nsew", padx=20, pady=20)
        
        self.editSeriesOnGoingLabel = ctk.CTkLabel(self.editSeriesWindow, text="On Going", font=ctk.CTkFont(size=25))
        self.editSeriesOnGoingLabel.grid(row=7, column=0, padx=20, pady=20)
        
        self.editSeriesSwitchVar = ctk.StringVar()
        self.editSeriesSwitch = ctk.CTkSwitch(self.editSeriesWindow, text="", variable=self.editSeriesSwitchVar, onvalue="1", offvalue="0")
        self.editSeriesSwitch.grid(row=7, column=1, sticky="nsew", padx=20, pady=20)
        
        if self.chosenSeries[5] == 1:
            self.editSeriesSwitch.toggle()
            
        self.editSeriesFinishedLabel = ctk.CTkLabel(self.editSeriesWindow, text="Finished", font=ctk.CTkFont(size=25))
        self.editSeriesFinishedLabel.grid(row=7, column=2, padx=20, pady=20)
        
        self.editSeriesLogoLabel = ctk.CTkLabel(self.editSeriesWindow, text="Logo: ", font=ctk.CTkFont(size=25))
        self.editSeriesLogoLabel.grid(row=8, column=0, padx=20, pady=20)
        
        self.seriesImageEntryVar = ctk.StringVar()
        self.seriesImageEntryVar.set(f"{self.imagePath}\\series_logos\\{self.chosenSeries[0].lower().replace(' ', '_')}SL.png")
        self.editSeriesWindowImageEntry = ctk.CTkEntry(self.editSeriesWindow, textvariable=self.seriesImageEntryVar, state="readonly", corner_radius=3.5)
        self.editSeriesWindowImageEntry.grid(row=8, column=1, sticky="nsew", padx=20, pady=20)
        
        self.editSeriesImageBrowseButton = ctk.CTkButton(self.editSeriesWindow, text="Browse Image", command=lambda: self.browse_square_image(self.seriesImageEntryVar))
        self.editSeriesImageBrowseButton.grid(row=8, column=2, sticky="nsew", padx=20, pady=20)
        
        self.editSeriesSubmitButton = ctk.CTkButton(self.editSeriesWindow, text="Submit", command=lambda: self.submit_update_series(self.editSeriesTitlePrompt.get(), self.editSeriesArtPrompt.get(), self.editSeriesStoryPrompt.get(), self.editSeriesPublisherPrompt.get(), self.editSeriesVolumesPublishedPrompt.get(), self.editSeriesSwitch.get(), self.seriesImageEntryVar.get()))
        self.editSeriesSubmitButton.grid(row=9, column=1, sticky="nsew", padx=20, pady=20)
        
        self.editSeriesExitButton = ctk.CTkButton(self.editSeriesWindow, text="Cancel", command=lambda: self.editSeriesWindow.destroy())
        self.editSeriesExitButton.grid(row=9, column=2, sticky="nsew", padx=20, pady=20)

    def add_volume_menu(self) -> None:
        self.addVolumeWindow = ctk.CTkToplevel(self)
        self.addVolumeWindow.title("Add Volume")
        self.addVolumeWindow.geometry("800x400")
        self.addVolumeWindow.grab_set()
        
        self.addVolumeWindowLabel = ctk.CTkLabel(self.addVolumeWindow, text="Add Volume", font=ctk.CTkFont(size=35, weight="bold"))
        self.addVolumeWindowLabel.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        self.addVolumeWindowOptionLabel = ctk.CTkLabel(self.addVolumeWindow, text="Choose Series: ", font=ctk.CTkFont(size=25, weight="bold"))
        self.addVolumeWindowOptionLabel.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        
        self.addVolumeOptionMenu = ctk.CTkOptionMenu(self.addVolumeWindow, values=self.database.get_all_series_names())
        self.addVolumeOptionMenu.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)
        
        self.addVolumeTitleLabel = ctk.CTkLabel(self.addVolumeWindow, text="Title: ", font=ctk.CTkFont(size=25))
        self.addVolumeTitleLabel.grid(row=2, column=0, padx=20, pady=20)
        
        self.addVolumeTitlePrompt = ctk.CTkEntry(self.addVolumeWindow, corner_radius=3.5)
        self.addVolumeTitlePrompt.grid(row=2, column=1, sticky="nsew", padx=20, pady=20)
        
        self.addVolumeCoverLabel = ctk.CTkLabel(self.addVolumeWindow, text="Cover: ", font=ctk.CTkFont(size=25))
        self.addVolumeCoverLabel.grid(row=3, column=0, padx=20, pady=20)
        
        self.volumeImageEntryVar = ctk.StringVar()
        self.addVolumeWindowImageEntry = ctk.CTkEntry(self.addVolumeWindow, textvariable=self.volumeImageEntryVar, state="readonly", corner_radius=3.5)
        self.addVolumeWindowImageEntry.grid(row=3, column=1, sticky="nsew", padx=20, pady=20)
        
        self.addVolumeImageBrowseButton = ctk.CTkButton(self.addVolumeWindow, text="Browse Image", command=lambda: self.browse_cover_image(self.volumeImageEntryVar))
        self.addVolumeImageBrowseButton.grid(row=3, column=2, sticky="nsew", padx=20, pady=20)
        
        self.addVolumeSubmitButton = ctk.CTkButton(self.addVolumeWindow, text="Submit", command=lambda: self.submit_volume(self.addVolumeOptionMenu.get(), self.addVolumeTitlePrompt.get(), self.volumeImageEntryVar.get()))
        self.addVolumeSubmitButton.grid(row=4, column=1, sticky="nsew", padx=20, pady=20)
        
        self.addVolumeExitButton = ctk.CTkButton(self.addVolumeWindow, text="Cancel", command=lambda: self.addVolumeWindow.destroy())
        self.addVolumeExitButton.grid(row=4, column=2, sticky="nsew", padx=20, pady=20)
    
    def edit_volume_menu(self) -> None:
        self.editVolumeWindow = ctk.CTkToplevel(self)
        self.editVolumeWindow.title("Edit Volume")
        self.editVolumeWindow.geometry("900x500")
        self.editVolumeWindow.grab_set()
        
        self.editVolumeWindowLabel = ctk.CTkLabel(self.editVolumeWindow, text="Edit Volume", font=ctk.CTkFont(size=35, weight="bold"))
        self.editVolumeWindowLabel.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        self.editVolumeWindowSeriesOptionLabel = ctk.CTkLabel(self.editVolumeWindow, text="Choose Series: ", font=ctk.CTkFont(size=25, weight="bold"))
        self.editVolumeWindowSeriesOptionLabel.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
            
        self.editVolumeSeriesOptionMenu = ctk.CTkOptionMenu(self.editVolumeWindow, values=self.database.get_all_series_names(), command=self.editVolumeWindow_seriesOptionMenu_callback)
        self.editVolumeSeriesOptionMenu.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)
        
        self.editVolumeWindowSeriesOptionLabel = ctk.CTkLabel(self.editVolumeWindow, text="There are no volumes added to this series", font=ctk.CTkFont(size=25, weight="bold"))
        
        self.editVolumeWindowVolumeOptionLabel = ctk.CTkLabel(self.editVolumeWindow, text="Choose Volume: ", font=ctk.CTkFont(size=25, weight="bold"))

        self.editVolumeOptionMenu = ctk.CTkOptionMenu(self.editVolumeWindow, values=self.database.get_volumes_from_series(self.database.get_series_id_by_series_title(self.editVolumeSeriesOptionMenu.get())), command=self.editVolumeOptionMenu_callback)

        self.editVolumeTitleLabel = ctk.CTkLabel(self.editVolumeWindow, text="Title: ", font=ctk.CTkFont(size=25))

        self.volumeTitleEntryVar = ctk.StringVar()
        self.editVolumeTitlePrompt = ctk.CTkEntry(self.editVolumeWindow, textvariable=self.volumeTitleEntryVar, corner_radius=3.5)

        self.editVolumeCoverLabel = ctk.CTkLabel(self.editVolumeWindow, text="Cover: ", font=ctk.CTkFont(size=25))

        self.volumeImageEntryVar = ctk.StringVar()
        self.editVolumeWindowImageEntry = ctk.CTkEntry(self.editVolumeWindow, textvariable=self.volumeImageEntryVar, state="readonly", corner_radius=3.5)

        self.editVolumeImageBrowseButton = ctk.CTkButton(self.editVolumeWindow, text="Browse Image", command=lambda: self.browse_cover_image(self.volumeImageEntryVar))

        self.editVolumeSubmitButton = ctk.CTkButton(self.editVolumeWindow, text="Submit", command=lambda: self.submit_update_volume(self.editVolumeSeriesOptionMenu.get(), self.editVolumeTitlePrompt.get(), self.editVolumeOptionMenu.get(), self.volumeImageEntryVar.get()))

        self.editVolumeExitButton = ctk.CTkButton(self.editVolumeWindow, text="Cancel", command=lambda: self.editVolumeWindow.destroy())

        self.editVolumeWindow_seriesOptionMenu_callback(self.editVolumeSeriesOptionMenu.get())

    def submit_update_volume(self, seriesName: str, newTitle: str, oldTitle: str, cover: str) -> None:
        self.editVolumeWindow.destroy()
        seriesVolumes = self.database.get_volumes_from_series(self.database.get_series_id_by_series_title(seriesName))
        if not newTitle in seriesVolumes or newTitle == oldTitle:
            databaseResponse = self.database.update_volume(self.database.get_series_id_by_series_title(seriesName), seriesName, newTitle, oldTitle, cover)
            if databaseResponse == "ok":
                CTkMessagebox(title="Success", message="Volume added to Series!", icon="check", option_1="Ok")
            else:
                CTkMessagebox(title="Error", message=f"Error: {databaseResponse}", icon="cancel")
        else:
            CTkMessagebox(title="Error", message=f"Error: There is already volume so titled in this series!", icon="cancel")

    def editVolumeWindow_seriesOptionMenu_callback(self, choice) -> None:
        if self.database.get_volumes_from_series(self.database.get_series_id_by_series_title(choice)) == []:
                self.editVolumeWindowSeriesOptionLabel.grid(row=2, column=0, sticky="nsew", padx=20, pady=20)
                self.editVolumeExitButton.grid(row=3, column=1, sticky="nsew", padx=20, pady=20)
                self.editVolumeWindowVolumeOptionLabel.grid_forget()
                self.editVolumeOptionMenu.grid_forget()
                self.editVolumeTitleLabel.grid_forget()
                self.editVolumeTitlePrompt.grid_forget()
                self.editVolumeCoverLabel.grid_forget()
                self.editVolumeWindowImageEntry.grid_forget()
                self.editVolumeImageBrowseButton.grid_forget()
                self.editVolumeImageBrowseButton.grid_forget()
                self.editVolumeSubmitButton.grid_forget()
        else:
                self.editVolumeWindowSeriesOptionLabel.grid_forget()
                self.editVolumeExitButton.grid_forget()
                self.editVolumeWindowVolumeOptionLabel.grid(row=2, column=0, sticky="nsew", padx=20, pady=20)
                self.editVolumeOptionMenu.grid(row=2, column=1, sticky="nsew", padx=20, pady=20)
                self.editVolumeTitleLabel.grid(row=3, column=0, padx=20, pady=20)
                self.editVolumeTitlePrompt.grid(row=3, column=1, sticky="nsew", padx=20, pady=20)
                self.editVolumeCoverLabel.grid(row=4, column=0, padx=20, pady=20)
                self.editVolumeWindowImageEntry.grid(row=4, column=1, sticky="nsew", padx=20, pady=20)
                self.editVolumeImageBrowseButton.grid(row=4, column=2, sticky="nsew", padx=20, pady=20)
                self.editVolumeSubmitButton.grid(row=5, column=1, sticky="nsew", padx=20, pady=20)
                self.editVolumeExitButton.grid(row=5, column=2, sticky="nsew", padx=20, pady=20)
                self.volumeTitleEntryVar.set(self.editVolumeOptionMenu.get())
                self.volumeImageEntryVar.set(os.path.join(self.imagePath, f"volumes_covers\\{self.editVolumeSeriesOptionMenu.get().lower().replace(' ', '_')}\\{self.editVolumeOptionMenu.get().lower().replace(' ', '_')}.png"))
        
    def editVolumeOptionMenu_callback(self, choice) -> None:
        self.volumeTitleEntryVar.set(choice)
        self.volumeImageEntryVar.set(os.path.join(self.imagePath, f"volumes_covers\\{self.editVolumeSeriesOptionMenu.get().lower().replace(' ', '_')}\\{self.editVolumeOptionMenu.get().lower().replace(' ', '_')}.png"))  
        
    def submit_update_series(self, title: str, art: str, story: str, publisher: str, volumes: str, finished: str, logo: str) -> None:
        editedSeries = self.editSeriesOptionMenu.get()
        self.editSeriesWindow.destroy()
        if self.is_positive_integer(volumes):
            allSeries = self.database.get_all_series_names()
            if (not title in allSeries) or (editedSeries == title):
                databaseResponse = self.database.update_series(title, editedSeries, art, story, publisher, int(volumes), int(finished), logo)
                if databaseResponse == "ok":
                    CTkMessagebox(title="Success", message="Series has been updated in MangaShelf!", icon="check", option_1="Ok")
                else:
                    CTkMessagebox(title="Error", message=f"Error: {databaseResponse}", icon="cancel")
            else:
                CTkMessagebox(title="Error", message=f"Error: There is already this series in MangaShelf!", icon="cancel")
        else:
            CTkMessagebox(title="Error", message=f"Error: wrong volumes number!", icon="cancel")

    def editSeriesMenu_callback(self, choice) -> None:
        self.chosenSeries = self.database.get_from_series(self.database.get_series_id_by_series_title(choice))
        print(self.chosenSeries[0], self.chosenSeries[1], self.chosenSeries[2], self.chosenSeries[3], self.chosenSeries[4], self.chosenSeries[5])
        self.editSeriesTitleEntryVar.set(f"{self.chosenSeries[0]}")
        self.editSeriesArtEntryVar.set(f"{self.chosenSeries[1]}")
        self.editSeriesStoryEntryVar.set(f"{self.chosenSeries[2]}")
        self.editSeriesPublisherEntryVar.set(f"{self.chosenSeries[3]}")
        self.editSeriesVolumesPublishedEntryVar.set(f"{self.chosenSeries[4]}")
        if self.chosenSeries[5] == 1:
            self.editSeriesSwitch.toggle()

        self.seriesImageEntryVar.set(f"{self.imagePath}\\series_logos\\{self.chosenSeries[0].lower().replace(' ', '_')}SL.png")

    def submit_volume(self, seriesName: str, title: str, cover: str) -> None:
        self.addVolumeWindow.destroy()
        seriesVolumes = self.database.get_volumes_from_series(self.database.get_series_id_by_series_title(seriesName))
        if not title in seriesVolumes:
            databaseResponse = self.database.add_volume(self.database.get_series_id_by_series_title(seriesName), seriesName, title, cover)
            if databaseResponse == "ok":
                CTkMessagebox(title="Success", message="Volume added to Series!", icon="check", option_1="Ok")
            else:
                CTkMessagebox(title="Error", message=f"Error: {databaseResponse}", icon="cancel")
        else:
            CTkMessagebox(title="Error", message=f"Error: There is already volume so titled in this series!", icon="cancel")

    def submit_series(self, title: str, art: str, story: str, publisher: str, volumes: str, finished: str, logo: str) -> None:
        self.addSeriesWindow.destroy()
        if self.is_positive_integer(volumes):
            allSeries = self.database.get_all_series_names()
            if not title in allSeries:
                databaseResponse = self.database.add_series(title, art, story, publisher, int(volumes), int(finished), logo)
                if databaseResponse == "ok":
                    CTkMessagebox(title="Success", message="Series added to MangaShelf!", icon="check", option_1="Ok")
                else:
                    CTkMessagebox(title="Error", message=f"Error: {databaseResponse}", icon="cancel")
            else:
                CTkMessagebox(title="Error", message=f"Error: There is already this series in MangaShelf!", icon="cancel")
        else:
            CTkMessagebox(title="Error", message=f"Error: wrong volumes number!", icon="cancel")

    def is_positive_integer(self, s: str) -> bool:
        try:
            num = int(s)
            return num > 0
        except ValueError:
            return False
                

    def editProfileButton_menu(self) -> None:
        self.editUserWindow = ctk.CTkToplevel(self)
        self.editUserWindow.title("Edit User")
        self.editUserWindow.geometry("600x400")
        self.editUserWindow.grab_set()
        
        self.editUserWindowLabel = ctk.CTkLabel(self.editUserWindow, text="Edit User", font=ctk.CTkFont(size=35, weight="bold"))
        self.editUserWindowLabel.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        self.editUserWindowOptionLabel = ctk.CTkLabel(self.editUserWindow, text="Choose user:", font=ctk.CTkFont(size=25))
        self.editUserWindowOptionLabel.grid(row=1, column=0, padx=20, pady=20)
        
        self.editUserOptionMenu = ctk.CTkOptionMenu(self.editUserWindow, width=150, values=self.database.get_all_user_names(), command=self.editUserMenu_callback)
        self.editUserOptionMenu.grid(row=1, column=1, padx=20, pady=20)

        self.editUserWindowNameEntryVar = ctk.StringVar()
        self.editUserWindowNameEntryVar.set(self.editUserOptionMenu.get())
        
        self.editUserWindowNameLabel = ctk.CTkLabel(self.editUserWindow, text="User name:", font=ctk.CTkFont(size=25))
        self.editUserWindowNameLabel.grid(row=2, column=0, padx=20, pady=20)

        self.editUserNamePrompt = ctk.CTkEntry(self.editUserWindow, textvariable=self.editUserWindowNameEntryVar, corner_radius=3.5)
        self.editUserNamePrompt.grid(row=2, column=1, sticky="nsew", padx=20, pady=20)

        def remove_default_text(event):
            if self.editUserNamePrompt.get() == self.editUserOptionMenu.get():
                self.editUserNamePrompt.delete(0, ctk.END)

        self.editUserNamePrompt.bind("<FocusIn>", remove_default_text)

        self.editUserWindowImageLabel = ctk.CTkLabel(self.editUserWindow, text="Profile image:", font=ctk.CTkFont(size=25))
        self.editUserWindowImageLabel.grid(row=3, column=0, padx=20, pady=20)

        self.userImageEntryVar = ctk.StringVar()
        self.userImageEntryVar.set(f"{self.imagePath}\\profile_pictures\\{self.editUserOptionMenu.get()}PP.png")
        self.editUserWindowImageEntry = ctk.CTkEntry(self.editUserWindow, textvariable=self.userImageEntryVar, state="readonly", corner_radius=3.5)
        self.editUserWindowImageEntry.grid(row=3, column=1, sticky="nsew", padx=20, pady=20)

        editUserImageBrowseButton = ctk.CTkButton(self.editUserWindow, text="Browse Image", command=lambda x: self.browse_square_image(self.userImageEntryVar))
        editUserImageBrowseButton.grid(row=3, column=2, sticky="nsew", padx=20, pady=20)

        editUserSubmitButton = ctk.CTkButton(self.editUserWindow, text="Update", command=lambda: self.update_user_in_database(self.editUserNamePrompt.get(), self.editUserOptionMenu.get(), self.userImageEntryVar.get()))
        editUserSubmitButton.grid(row=4, column=0, sticky="nsew", padx=20, pady=20)
        
        editUserExitButton = ctk.CTkButton(self.editUserWindow, text="Cancel", command=lambda: self.editUserWindow.destroy())
        editUserExitButton.grid(row=4, column=1, sticky="nsew", padx=20, pady=20)

    def editUserMenu_callback(self, choice: str) -> None:
        self.editUserWindowNameEntryVar.set(self.editUserOptionMenu.get())
        self.userImageEntryVar.set(f"{self.imagePath}\\profile_pictures\\{choice}PP.png")

    def resetDbButton_handler(self) -> None:
        msg = CTkMessagebox(title="Reset Database", message="Are you sure you want to reset database?", icon="question", option_1="Cancel", option_2="Reset")
        response = msg.get()
        if response=="Reset":
            databaseResponse = self.database.reset_db()
            if databaseResponse == "ok":
                CTkMessagebox(title="Success", message="Mangashelf restored to default state", icon="check", option_1="Ok")
                self.refresh_add_frame()
                self.refresh_home_frame()
            else:
                CTkMessagebox(title="Error", message=f"Error: {databaseResponse}", icon="cancel")


    def update_user_in_database(self, newUserName: str, oldUserName: str, profilePicture: str) -> None:
        self.editUserWindow.destroy()
        databaseResponse = self.database.update_user(newUserName, oldUserName, profilePicture)
        if databaseResponse == "ok":
            CTkMessagebox(title="Success", message="User has been updated in MangaShelf", icon="check", option_1="Ok")
            self.refresh_home_frame()
            self.refresh_add_frame()
            self.select_frame_by_name("home")
        else:
            CTkMessagebox(title="Error", message=f"Error: {databaseResponse}", icon="cancel")
            
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

    def is_cover_image(self, file_path: str) -> bool:
        try:
            with Image.open(file_path) as img:
                width, height = img.size
                return width / 3 == height / 4
        except Exception as e:
            print(f"Error: {e}")
            return False

    def browse_square_image(self, entryVar: ctk.StringVar)-> None:
        filename = ctk.filedialog.askopenfilename(initialdir="/", title="Select Image", filetypes=(("Image files", "*.png;*.jpg;*.jpeg;*.gif"), ("all files", "*.*")))
        if filename:
            if self.is_square_image(filename):
                entryVar.set(filename)
            else:
                CTkMessagebox(title="Error", message="Please provide squared image!", icon="cancel")
                
    def browse_cover_image(self, entryVar: ctk.StringVar) -> None:
        filename = ctk.filedialog.askopenfilename(initialdir="/", title="Select Image", filetypes=(("Image files", "*.png;*.jpg;*.jpeg;*.gif"), ("all files", "*.*")))
        if filename:
            if self.is_cover_image(filename):
                entryVar.set(filename)
            else:
                CTkMessagebox(title="Error", message="Please provide 3:4 image!", icon="cancel")

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

        self.addUserImageBrowseButton = ctk.CTkButton(self.addUserWindow, text="Browse Image", command=lambda: self.browse_square_image(self.userImageEntryVar))
        self.addUserImageBrowseButton.grid(row=2, column=2, sticky="nsew", padx=20, pady=20)

        self.addUserSubmitButton = ctk.CTkButton(self.addUserWindow, text="Submit", command=lambda: self.add_user_to_database(userNamePrompt.get(), self.userImageEntryVar.get()))
        self.addUserSubmitButton.grid(row=3, column=0, sticky="nsew", padx=20, pady=20)
        
        self.addUserExitButton = ctk.CTkButton(self.addUserWindow, text="Cancel", command=lambda: self.addUserWindow.destroy())
        self.addUserExitButton.grid(row=3, column=1, sticky="nsew", padx=20, pady=20)

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
   
    def button_placeholder(self) -> None:
        print("button_placeholder")         
            
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
        