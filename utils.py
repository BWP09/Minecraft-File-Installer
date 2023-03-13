import json, shutil, os, urllib.request, requests


def write_key_json(path: str, key, value):  
    with open(path, "r+", encoding = "utf-8") as file:
        data = json.load(file)

        data[key] = value

        file.seek(0)
        file.write(json.dumps(data, indent = 4))
        file.truncate()
    
def write_json(path: str, data: dict):
    with open(path, "w", encoding = "utf-8") as file:
        file.seek(0)
        file.write(json.dumps(data, indent = 4))
        file.truncate()

def read_json(path: str) -> dict:
    with open(path, "r", encoding = "utf-8") as file:
        return json.load(file)
    
def del_key_json(path: str, key):
    with open(path, "r+", encoding = "utf-8") as file:
        data = json.load(file)

        del data[key]

        file.seek(0)
        file.write(json.dumps(data, indent = 4))
        file.truncate()

def unzip(path: str, output_dir: str):
    shutil.unpack_archive(path, output_dir, "zip")

def unzip_to_temp(temp_path: str, input_file_path: str, temp_dir_name: str):
    shutil.unpack_archive(input_file_path, temp_path + temp_dir_name, "zip")

def empty_dir(dir_path: str):
    for root, dirs, files in os.walk(dir_path):
        for f in files:
            os.unlink(os.path.join(root, f))
        
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

def download_file(url: str, path: str):
    urllib.request.urlretrieve(url, path)

def get_version_number(url: str):
    r = requests.get(url + "mcfi/update")

    return str(r.content).removeprefix("b'").removesuffix("'")