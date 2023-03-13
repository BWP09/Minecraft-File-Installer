import os
import PySimpleGUI as sg

import utils, modes


# -a --add             :: use "add" mode
# -s --save            :: use "save" mode
# -l --load            :: use "load" mode
# -d --download        :: use "download" mode

# -z --zipped          :: use zipped file as input
# -f --folder          :: use folder as input

# -m --mods            :: add to mods folder
# -rp --resourcepacks  :: add to resourcepacks folder
# -ws --worldsaves     :: add to saves folder
# -sc --screenshots    :: hmm
# -sp --shaderpacks    :: add to shaderpacks folder

# python main.py -a -z -m mods.zip
# python main.py -s -m my_mods

VERSION = "0001"

WEBSITE_URL = "http://bwp-dev.com/"

APPDATA = os.getenv("APPDATA")
LOCAL_APPDATA = os.getenv("LOCALAPPDATA")

DEFAULT_MC_PATH = (str(APPDATA) + "/.minecraft/").replace("\\", "/")
TEMP_PATH = (str(LOCAL_APPDATA) + "/Temp/mc_file_installer/").replace("\\", "/")
SETTINGS_DIR_PATH = (str(APPDATA) + "/mc_file_installer/").replace("\\", "/")


if not os.path.exists(SETTINGS_DIR_PATH):
    settings = {
        "check_updates": True,
        "empty_temp_on_exit": True,
        "theme": "DarkAmber"
    }
    
    os.makedirs(SETTINGS_DIR_PATH)

    utils.write_json(SETTINGS_DIR_PATH + "settings.json", settings)
    utils.download_file(WEBSITE_URL + "mcfi/icon.ico", SETTINGS_DIR_PATH + "icon.ico")

if not os.path.exists(TEMP_PATH):
    os.makedirs(TEMP_PATH)

ICON = SETTINGS_DIR_PATH + "icon.ico"

settings = utils.read_json(SETTINGS_DIR_PATH + "settings.json")


sg.theme(settings["theme"])

col_1 = [
    [sg.Text("Minecraft Path", font = "_ 14", key = "-MC_PATH_TEXT-")],
    [sg.In(DEFAULT_MC_PATH, key = "-MC_PATH_TEXTBOX-", size = (35, 1)), sg.FolderBrowse(key = "-MC_PATH-")]
]

col_2 = [
    [sg.Text("Input File Path", font = "_ 14", key = "-INPUT_PATH_TEXT-")],
    [sg.In("Click Browse", key = "-INPUT_PATH_TEXTBOX-", size = (35, 1)), sg.FileBrowse(file_types = (("Zip file", "*.zip"), ("7zip file", "*.7z"), ("All files", ".*")), key = "-INPUT_PATH-")]
]

layout = [
    [sg.Column(col_1), sg.VSeparator(), sg.Column(col_2)],
    [sg.HSeparator()],

    [
     sg.Text("Mode:    ", font = "_ 14"),
     sg.Radio("Add    ", "RADIO1", key = "-RADIO1-", font = "_ 13", tooltip = "Add files to Minecraft"),
     sg.Radio("Open    ", "RADIO1", key = "-RADIO2-", font = "_ 13", tooltip = "Open a Minecraft folder"),
     sg.Radio("Delete    ", "RADIO1", key = "-RADIO3-", font = "_ 13", tooltip = "Clear items in folder inside of the Minecraft directory"),
     sg.Radio("Save    ", "RADIO1", key = "-RADIO4-", font = "_ 13", tooltip = "Save a list of Minecraft files"),
     sg.Text("                               "), sg.Button("Settings", font = "_ 12", key = "-SETTINGS_BUTTON-")
    ],

    [sg.Button("Continue", font = "_ 14", size = (61, 2), key = "-CONTINUE_BUTTON-")]
]


window = sg.Window("Minecraft file installer (MCFI)", layout, icon = ICON)


if settings["check_updates"]:
    latest = utils.get_version_number(WEBSITE_URL)
    if int(latest) > int(VERSION):
        sg.Popup("There is a newer version available!\nGo to the website for more information", title = "Update!", icon = ICON)


while True:
    event, values = window.read()

    #print(event)
    #print(values)

    if event in (sg.WIN_CLOSED, "Exit"):
        if settings["empty_temp_on_exit"]:
            utils.empty_dir(TEMP_PATH)
            
        break

    elif event == "-SETTINGS_BUTTON-":
        modes.settings_window(ICON, SETTINGS_DIR_PATH, settings)

    elif event == "-CONTINUE_BUTTON-":
        if values["-RADIO1-"]:
            if not values["-INPUT_PATH-"]:
                sg.popup_ok("You must first select an input file!", title = "Attention!")
                continue
            
            modes.add_mode(ICON, TEMP_PATH, values["-INPUT_PATH-"], DEFAULT_MC_PATH if not values["-MC_PATH-"] else values["-MC_PATH-"])
        
        elif values["-RADIO2-"]:
            modes.open_mode(ICON, DEFAULT_MC_PATH if not values["-MC_PATH-"] else values["-MC_PATH-"])

        elif values["-RADIO3-"]:
            sg.PopupOK("This feature is not yet implemented.\nIt is coming in the next update!", title = "Attention!")
            #modes.delete_mode(ICON, DEFAULT_MC_PATH if not values["-MC_PATH-"] else values["-MC_PATH-"])
        
        elif values["-RADIO4-"]:
            sg.PopupOK("This feature is not yet implemented.\nIt is coming in the next update!", title = "Attention!")
            #print("Save + Cont")

window.close()