import subprocess
import os
import sys
import importlib
import yaml
import re
from typing import List, Optional, Union, Literal

def install_module(module_name):
    try:
        subprocess.check_call(["pip", "install", module_name])
        print(f"Successfully installed {module_name}")
    except subprocess.CalledProcessError:
        print(f"Failed to install {module_name}")

def import_module(module_name):
    try:
        module = importlib.import_module(module_name)
        print(f"Imported {module_name} successfully")

        if module:
            globals()[module_name] = module

    except ImportError:
        print(f"Failed to import {module_name}")

def convert_bytes(
    bytes: int, 
    unit: Literal["KB", "MB", "GB", "TB"], 
    need_text: bool = False ) -> Union[str, float]:
    """Convert the bytes value to target unit.

    Args:
        bytes (int): the input bytes value.
        unit (Literal[&quot;KB&quot;, &quot;MB&quot;, &quot;GB&quot;, &quot;TB&quot;]): _description_
        need_text (bool, optional): return the string with format - "{value} {unit}". Defaults to False.

    Raises:
        TypeError: Unsupported unit

    Returns:
        Union[str, float]: return a string if need_text is True else return value
    """

    unit_map = { "KB": 1, "MB": 2, "GB": 3, "TB": 4 }
    num_decimal = 1
    N = unit_map.get(unit)
    if N is None:
        raise TypeError("Expect unit is {}, but got {}".format(
            ', '.join(unit_map.keys()), unit ))
    value = bytes/(1024**N)
    ret_value = round(value, num_decimal)    
    return f"{ret_value} {unit}" if need_text else ret_value

def is_name_includes(name:str, include_keys: Optional[list]=None, include_all:bool=True) -> bool:
    """Is name includes the keyword

    Args:
        name (str): the input name
        include_keys (Optional[list], optional): the include keywords. Defaults to None.

    Returns:
        bool: is include keywords
    """
    if not include_keys: return True
    
    includes, not_includes = [], []

    for key in include_keys:
        # Include
        if key in name:
            includes.append(key)
            continue
        # Not include
        if include_all:
            return False
        not_includes.append(key)

    if len(includes)==0:
        return False

    print('Input: {} includes {}'.format(name, ', '.join(includes)))
    return True

def is_name_excludes(name:str, exclude_keys: Optional[list]=None) -> bool:
    """Is name excludes the keyword.

    Args:
        name (str): the input name
        exclude_keys (Optional[list], optional): the exclude keywords. Defaults to None.

    Returns:
        bool: is exclude all keywords
    """
    if not exclude_keys: return True
    for exc in exclude_keys:
        if exc in name:
            return False
    return True

def is_tarball(file_path: str) -> str:
    
    if not file_path.endswith('tar'):
        raise TypeError("Only support tarball file.")

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f'File not find. ({file_path})')
    
    return file_path

def get_current_path() -> str:
    """ get current file """
    cur_script_path = os.path.realpath(sys.argv[0])
    cur_script_folder = os.path.dirname(cur_script_path)
    return cur_script_folder

class YamlFile:

    _path: str=""
    _content: dict={}

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, input_path: str):
        if not os.path.isfile(input_path):
            raise FileNotFoundError(f'Can not find compose file: {path}')
        self._path = input_path

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, input_content: str):
        if not isinstance(input_content, dict):
            raise TypeError('Should be dict')
        self._content = input_content

    def __init__(self, yaml_path:str):
        self.path = yaml_path
        self.content = self._get_yaml(self.path)

    def _get_yaml(self, path: str) -> dict:
        with open(path, 'r') as yaml_file:
            data = yaml.load(yaml_file, Loader=yaml.FullLoader)
        return data

def split_archive_name_ext(file: str) -> tuple[str, str]:
    exts = [
        '.tar',
        '.tar.gz',
        '.zip',
    ]
    for ext in exts:
        if file.endswith(ext):
            return file.replace(ext, ''), ext
    
    raise TypeError('Unexpected file extensions ({}), support is {}'.format(
        file, ', '.join(exts)
    ))

def get_base_archive_name(file: str) -> str:
    name, ext = split_archive_name_ext(file)
    return os.path.basename(name)

def is_valid_docker_image_name(image_name) -> bool:
    pattern = r'^[a-zA-Z0-9_.-]+(/[a-zA-Z0-9_.-]+)*:[a-zA-Z0-9_.-]+$'
    return True if re.match(pattern, image_name) else False
         
def get_image_name(service: str) -> str:
    # verify is service or not
    # [registry/][namespace/]repository_name[:tag]
    if not is_valid_docker_image_name(service):
        raise TypeError('Unexpected docker image name, please follow the rule: [registry/][namespace/]repository_name[:tag]')
    return os.path.basename(service).split(':')[0]

def is_ivit_main_tarball(tarball:str) -> bool:
    return True if re.match(
        r'^ivit-i-(intel|nvidia|jetson):v\d+(\.\d+)?-(dev|runtime|service)$', 
        get_base_archive_name(tarball)
    ) else False

def check_docker_engine():
    try:
        subprocess.check_output(["docker", "--version"])
        # print("Docker is installed.")
    except subprocess.CalledProcessError:
        print("Docker is not installed.")
        sys.exit(1)

if __name__ == "__main__":
    print(convert_bytes(1048576, "MB", 0))
    
    a = YamlFile('./compose.yml')
    print(a.path, a.content)