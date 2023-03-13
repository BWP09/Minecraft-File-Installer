import PySimpleGUI as sg
import distutils.dir_util as dir_util
import os, subprocess

import utils


def settings_window(icon: str, settings_dir_path: str, settings: dict):
    layout = [
        [sg.Button("Apply changes", font = "_ 13", size = (12, 1), key = "-APPLY-"), sg.Button("About MCFI", font = "_ 13", size = (12, 1), key = "-ABOUT-")],
        [sg.Text("Changes will take effect at next launch")],

        [sg.HSeparator()],

        [sg.Checkbox("Check for updates", default = settings["check_updates"], key = "check_updates")],
        [sg.Input(settings["theme"], size = (15, 1), key = "theme"), sg.Text("Theme")],
        [sg.Checkbox("Empty temp on exit", default = settings["empty_temp_on_exit"], key = "empty_temp_on_exit")]
    ]

    window = sg.Window("Settings", layout, icon = icon)

    while True:
        event, values = window.read()

        #print(event)
        #print(values)

        if event in (sg.WIN_CLOSED, "Exit"):
            break

        elif event == "-APPLY-":
            utils.write_json(settings_dir_path + "settings.json", values)
        
        elif event == "-ABOUT-":
            sg.popup_ok("Minecraft File Installer (MCFI) by Brandon Payne, or BWP09.\nDC: BWP09#5091, GH: github.com/BWP09, WS: bwp-dev.com")


def datapack_add_window(icon: str, temp_dp_path: str, mc_saves_path: str):
    
    layout = [
        [sg.Button("  Continue  ", font = "_ 12", key = "-CONTINUE-")],
        
        [sg.HSeparator()],
        
        [sg.Text("Add datapacks to the worlds...", font = "_ 12")],
    ]
    
    world_paths = []
    world_names = []
    for world_dir in os.listdir(mc_saves_path):
        world_dir_path = mc_saves_path + f"/{world_dir}/" 
        if os.path.isdir(world_dir_path):
            world_paths.append(world_dir_path)
            world_names.append(world_dir_path.removesuffix("/").split("/")[-1])
     
    amount = 0
    for i, name in enumerate(world_names):
        layout += [[sg.Checkbox(name, key = f"-{i}-")]]
        amount = i
    
    layout += [
        [sg.HSeparator()],
        
        [sg.Text("Progress: "), sg.Text("Not started", key = "-PROGRESS_2-")]
    ]

    window = sg.Window("Datapack options", layout, icon = icon, size = (275, 150 + (30 * amount)))


    while True:
        event, values = window.read() # type: ignore

        #print(event)
        #print(values)

        if event in (sg.WIN_CLOSED, "Exit"):
            break

        elif event == "-CONTINUE-":
            window["-PROGRESS_2-"].update("Started!") # type: ignore

            for key in values.keys():
                number = int(key.removeprefix("-").removesuffix("-"))

                if values[key]:
                    dir_util.copy_tree(temp_dp_path, world_paths[number] + "/datapacks")
            
            window["-PROGRESS_2-"].update("Done!") # type: ignore


def add_mode(icon: str, temp_path: str, input_path: str, mc_path: str):
    unzipped_dir_name = input_path.split("/")[-1].removesuffix(".zip")
    unzipped_dir_path = temp_path + "/" + unzipped_dir_name + "/" + unzipped_dir_name

    utils.unzip_to_temp(temp_path, input_path, unzipped_dir_name)
    
    data = utils.read_json(unzipped_dir_path + "/data.json")

    types = data["data_type"]
    
    
    mods, rp, saves, dp, sp = False, False, False, False, False
    
    if "mods" in types: mods = True

    if "rp" in types or "resourcepacks" in types: rp = True

    if "saves" in types: saves = True

    if "dp" in types or "datapacks" in types: dp = True

    if "sp" in types or "shaderpacks" in types: sp = True
    
    
    layout = [
        [sg.Button("  Start  ", font = "_ 13", key = "-START-"), sg.Text(unzipped_dir_name + ".zip", font = "_ 12")],
        [sg.Text(f"Description: {data['description']}", key = "-TEXT_DESC-")],

        [sg.HSeparator()],
        
        [sg.Text("Include...", font = "_ 11")],
        [sg.Checkbox("Mods", key = "-MODS-", default = mods, disabled = not mods), sg.Checkbox("Resource Packs", key = "-RP-", default = rp, disabled = not rp), sg.Checkbox("Saves", key = "-SAVES-", default = saves, disabled = not saves)],
        [sg.Checkbox("Data Packs", key = "-DP-", default = dp, disabled = not dp), sg.Checkbox("Shader Packs", key = "-SP-", default = sp, disabled = not sp)],

        [sg.HSeparator()],

        [sg.Text("Progress: "), sg.Text("Not started", key = "-PROGRESS-")]
    ]

    window = sg.Window("Add Mode", layout, icon = icon)

    while True:
        event, values = window.read()

        #print(event)
        #print(values)

        if event in (sg.WIN_CLOSED, "Exit"):
            break
        
        elif event == "-START-":
            window["-PROGRESS-"].update("Started!") # type: ignore
            
            if values['-MODS-']:
                window["-PROGRESS-"].update("Adding mods") # type: ignore
                
                temp_mods_path = unzipped_dir_path + "/mods"
                mc_mods_path = mc_path + "mods"

                if not os.path.exists(mc_mods_path):
                    os.makedirs(mc_mods_path)
                
                dir_util.copy_tree(temp_mods_path, mc_mods_path)
            
            if values['-RP-']:
                window["-PROGRESS-"].update("Adding resource packs") # type: ignore
                
                temp_rp_path = unzipped_dir_path + "/resourcepacks"
                mc_rp_path = mc_path + "resourcepacks"

                dir_util.copy_tree(temp_rp_path, mc_rp_path)

            if values['-SAVES-']:
                window["-PROGRESS-"].update("Adding saves") # type: ignore
                
                temp_saves_path = unzipped_dir_path + "/saves"
                mc_saves_path = mc_path + "saves"

                dir_util.copy_tree(temp_saves_path, mc_saves_path)

            if values['-SP-']:
                window["-PROGRESS-"].update("Adding shader packs") # type: ignore
                
                temp_sp_path = unzipped_dir_path + "/shaderpacks"
                mc_sp_path = mc_path + "shaderpacks"

                if not os.path.exists(mc_sp_path):
                    os.makedirs(mc_sp_path)

                dir_util.copy_tree(temp_sp_path, mc_sp_path)

            if values['-DP-']:
                window["-PROGRESS-"].update("Adding data packs") # type: ignore
                
                temp_dp_path = unzipped_dir_path + "/datapacks"
                mc_saves_path = mc_path + "saves"

                datapack_add_window(icon, temp_dp_path, mc_saves_path)
            
            window["-PROGRESS-"].update("Done!") # type: ignore
    
    window.close()


def datapack_open_window(icon: str, mc_saves_path: str):
    layout = [
        [sg.Button("  Open Folder  ", font = "_ 13", size = (20, 1), key = "-OPEN-")],
        
        [sg.HSeparator()],
        
        [sg.Text("Open world datapacks...", font = "_ 11")],
    ]

    world_paths = []
    world_names = []
    for world_dir in os.listdir(mc_saves_path):
        world_dir_path = mc_saves_path + f"/{world_dir}/" 
        if os.path.isdir(world_dir_path):
            world_paths.append(world_dir_path)
            world_names.append(world_dir_path.removesuffix("/").split("/")[-1])
     
    amount = 0
    for i, name in enumerate(world_names):
        layout += [[sg.Radio(name, "RADIO1", key = f"-{i}-")]]
        amount = i


    window = sg.Window("Open datapack folders", layout, icon = icon)

    while True:
        event, values = window.read()

        #print(event)
        #print(values)

        if event in (sg.WIN_CLOSED, "Exit"):
            break

        elif event == "-OPEN-":
            for key in values.keys():
                number = int(key.removeprefix("-").removesuffix("-"))

                if values[key]:
                    dp_path = (world_paths[number] + "datapacks").replace("/", "\\")
                    subprocess.Popen(f'explorer "{dp_path}"')


def open_mode(icon: str, mc_path: str):
    layout = [
        [sg.Button("  Open Folder  ", font = "_ 13", size = (20, 1), key = "-OPEN-")],

        [sg.HSeparator()],
        
        [sg.Text("Open folder...", font = "_ 11")],
        [sg.Radio("Saves", "RADIO1", key = "-RADIO1-")],
        [sg.Radio("Screenshots", "RADIO1", key = "-RADIO2-")],
        [sg.Radio("Mods", "RADIO1", key = "-RADIO3-")],
        [sg.Radio("Resource packs", "RADIO1", key = "-RADIO4-")],
        [sg.Radio("Shader packs", "RADIO1", key = "-RADIO5-")],
        [sg.Radio("Data packs", "RADIO1", key = "-RADIO6-")],
    ]

    window = sg.Window("Open Mode", layout, icon = icon)

    while True:
        event, values = window.read()

        #print(event)
        #print(values)

        if event in (sg.WIN_CLOSED, "Exit"):
            break
        
        elif event == "-OPEN-":
            if values["-RADIO1-"]:
                saves_path = (mc_path + "saves").replace("/", "\\")
                
                if not os.path.exists(saves_path):
                    os.makedirs(saves_path)
                
                subprocess.Popen(f'explorer "{saves_path}"')
            
            elif values["-RADIO2-"]:
                sc_path = (mc_path + "screenshots").replace("/", "\\")

                if not os.path.exists(sc_path):
                    os.makedirs(sc_path)

                subprocess.Popen(f'explorer "{sc_path}"')

            elif values["-RADIO3-"]:
                mods_path = (mc_path + "mods").replace("/", "\\")

                if not os.path.exists(mods_path):
                    os.makedirs(mods_path)

                subprocess.Popen(f'explorer "{mods_path}"')

            elif values["-RADIO4-"]:
                rp_path = (mc_path + "resourcepacks").replace("/", "\\")

                if not os.path.exists(rp_path):
                    os.makedirs(rp_path)

                subprocess.Popen(f'explorer "{rp_path}"')

            elif values["-RADIO5-"]:
                sp_path = (mc_path + "shaderpacks").replace("/", "\\")

                if not os.path.exists(sp_path):
                    os.makedirs(sp_path)

                subprocess.Popen(f'explorer "{sp_path}"')
            
            elif values["-RADIO6-"]:
                saves_path = (mc_path + "saves").replace("/", "\\")
                datapack_open_window(icon, saves_path)
    
    window.close()


def delete_mode(icon: str, mc_path: str):
    layout = [
        [sg.Button("  Clear folders  ", font = "_ 13", size = (30, 1), key = "-CLEAR-")],
        
        [sg.HSeparator()],

        [sg.Checkbox("Mods", key = "-MODS-"), sg.Checkbox("Resource Packs", key = "-RP-"), sg.Checkbox("Saves", key = "-SAVES-")],
        [sg.Checkbox("Data Packs", key = "-DP-"), sg.Checkbox("Shader Packs", key = "-SP-")],

        [sg.HSeparator()],

        [sg.Text("Progress: "), sg.Text("Not started", key = "-PROGRESS-")]
    ]

    window = sg.Window("Delete Mode", layout, icon = icon)

    while True:
        event, values = window.read()

        #print(event)
        #print(values)

        if event in (sg.WIN_CLOSED, "Exit"):
            break

        elif event == "-CLEAR-":
            window["-PROGRESS-"].update("Started!") # type: ignore
            
            if values['-MODS-']:
                window["-PROGRESS-"].update("Clearing mods") # type: ignore
                
                utils.empty_dir(mc_path + "mods")
            
            if values['-RP-']:
                window["-PROGRESS-"].update("Clearing resource packs") # type: ignore

                utils.empty_dir(mc_path + "resourcepacks")

            if values['-SAVES-']:
                window["-PROGRESS-"].update("Clearing saves") # type: ignore

                utils.empty_dir(mc_path + "saves")

            if values['-SP-']:
                window["-PROGRESS-"].update("Clearing shader packs") # type: ignore
                
                utils.empty_dir(mc_path + "shaderpacks")

            if values['-DP-']:
                window["-PROGRESS-"].update("Clearing data packs") # type: ignore

                #utils.empty_dir(mc_path + "mods")

            window["-PROGRESS-"].update("Done!") # type: ignore