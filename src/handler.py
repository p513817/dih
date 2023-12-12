import glob
import abc
import re
import os
import sys
import random
import time

from collections import defaultdict
from typing import List, Union, Optional

# Custom
sys.path.append(os.path.dirname(__file__))
import handler
import utils
import gui
import docker_helper

class Wrapper(abc.ABC):
    """ Handle Innodisk Docker Image """

    _folder = ""
    _processes = defaultdict()
    _valid_index = []

    def __init__(self, folder: str):
        self.folder = folder
        self.handler = docker_helper.HandleDockerImage()

        # Define rich parameters
        self.progress = gui.get_rich_progress()
        self.table = gui.RichTable()

    @property
    def folder(self):
        return self._folder

    @folder.setter
    def folder(self, folder_path:str):
        if not isinstance(folder_path, str):
            raise TypeError("Should be a string.")
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Created a folder for saving docker image: {folder_path}")
        self._folder = folder_path

    @abc.abstractmethod
    def define_table(self):
        pass

    @abc.abstractmethod
    def update_table(self):
        pass

    @abc.abstractmethod
    def start(self):
        pass

    @property
    def valid_index(self):
        return self._valid_index

    @valid_index.setter
    def valid_index(self, value: List[Union[int, None]]):
        if value ==[] or isinstance(value, list):
            self._valid_index = value
            return
        raise TypeError("The valid_index should be list.")

    def filter_with_index(self, data:dict) -> list:
        
        if not data:
            raise ValueError("No docker images find. Please init the object first.")

        # Init
        _valid_index = []
        support_index = [ i for i in data.keys()]
        max_index = len(support_index)

        # Wait input
        input_indexes = input("Select the docker image you want to save (all/<id>,..,<id>): ")

        # All index
        if input_indexes.lower() == "all":
            return support_index

        # Filter mismatch data
        integer_pattern = re.compile(r'^\d+(,\d+)*$')
        if not integer_pattern.match(input_indexes):
            raise TypeError(f'Unexpected input: {input_indexes}')
        
        # Check the limit and convert format
        for index in sorted(set(input_indexes.split(','))):
            index = int(index)
            if max_index is None or index in support_index:
                _valid_index.append(index)

        if _valid_index == []:
            raise IndexError('There is no validated indexes. support is {}'.format(
                ', '.join([ str(idx) for idx in support_index])
            ))

        print('Validated Index: ', _valid_index)
        return _valid_index


class DockerSaver(Wrapper):
    """ Define save innodisk docker behavior """


    def define_table(self):
        # Define rich parameters
        self.table.define(["Index", "Name", "Size", "Create"])

    def update_table(self, data: dict):
        for idx, docker_data in data.items():
            self.table.update((
                str(idx), 
                docker_data['repo'], 
                str(utils.convert_bytes(docker_data['size'], "MB", need_text=True)),
                str(docker_data['created'])
            ))
        self.table.print_out()

    def start(self):
        
        # Temp process for rich progress
        rich_process = defaultdict() 

        # Save
        for idx, image in self.data.items():

            if self.valid_index and not (idx in self.valid_index):
                continue
            
            image_name = image["repo"]
            base_name = os.path.basename(image_name).strip()
            output_file = os.path.join(
                self._folder,
                f"{base_name}.tar" )

            self._processes[idx] = {
                "id": base_name,
                "proc": self.handler.save(image_name, output_file),
                "input": image_name,
                "output": output_file }

            # Add Task
            rich_process[idx] = self.progress.add_task(base_name, total=100)

        with self.progress:
        
            # Wait
            while not self.progress.finished:
                for idx, data in self._processes.items():
                    process_running = (data['proc'].poll() is None)
                    file_exists = (os.path.exists(data['output']))
                    if not process_running and file_exists:
                        self.progress.update(rich_process[idx], completed=100, style="green")
                        continue
                    self.progress.update(rich_process[idx], advance=random.uniform(0.01, 0.1))
                    
                    # self.progress.update(rich_process[idx], advance=random.uniform(0.05, 1), style="green")

                time.sleep(0.5)

    def __del__(self):
        for key, data in self._processes.items():
            data["proc"].terminate()
        print('Cleared process!')

    def __init__(self, folder: str, includes=['inno'], excludes=['none']):
        super().__init__(folder)
        self.data = self.handler.find(
            includes=includes, 
            excludes=excludes )
        
        self.define_table()
        self.update_table(self.data)

        # Additional
        self.valid_index = self.filter_with_index(self.data)


class DockerLoader(Wrapper):
    
    data = None

    def find_tars(self, folder:str, extension: str="tar") -> dict:  
        """Get tarball files

        Args:
            folder (str): the folder place the tarball files.
            extension (str, optional): the extension of compressed file. Defaults to "tar".

        Raises:
            FileNotFoundError: can not find any compressed file.

        Returns:
            dict: return the information we captured

        Examples:
            {
                0: {
                    input: <the tarball path>,
                    base_name: <the base name of the tarball file>,
                    size: <the size of the tarball file>,
                    verify: 0
                }, ...
            }
        """
        temp = defaultdict(dict)
        for idx, tar in enumerate(glob.glob(os.path.join(folder, f"*.{extension}"))):
            size = utils.convert_bytes(os.stat(tar).st_size, unit='MB', need_text=True)
            base_name = os.path.basename(tar)
            temp[idx] = {
                'input': tar,
                'base_name': base_name,
                'size': size,
                'verify': 0 
            }
        if not temp:
            raise FileNotFoundError('Can not find any docker tarball files in {}.'.format(folder))
        return temp

    def define_table(self):
        self.table.define(["Index", "Name", "Size", "Verify"])

    def update_table(self):
        
        for idx, tar in self.data.items():
            
            (status, style) = ('FAIL', 'red')
            if tar['verify']:
                status, style = 'PASS', ''

            self.table.update((
                str(idx),
                tar['input'],
                tar['size'],
                status
            ), style = style )
        self.table.print_out()

    def start(self):

        # Temp process for rich progress
        rich_process = defaultdict()

        for idx, tar in self.data.items():
            
            # Conditions
            if not tar["verify"]: continue
            if self.valid_index and not (idx in self.valid_index):
                continue
            
            self._processes[idx] = {
                "id": tar["base_name"],
                "proc": self.handler.load(os.path.realpath(tar["input"])),
                "input": tar["input"],
            }
            rich_process[idx] = self.progress.add_task(
                tar["base_name"], total=100)

        with self.progress:
            # Wait
            while not self.progress.finished:

                for idx, data in self._processes.items():

                    process_running = (data['proc'].poll() is None)
                    if not process_running:
                        self.progress.update(rich_process[idx], completed=100, style="green")
                        continue
                    self.progress.update(rich_process[idx], advance=random.uniform(0.01, 0.05))
                    
                    # self.progress.update(rich_process[idx], advance=random.uniform(0.05, 1), style="green")

                time.sleep(1)
            
    def __del__(self):
        for key, data in self._processes.items():
            data["proc"].terminate()

    def verify_services(self, tarballs: dict, services: list) -> dict:

        # Helper
        add_space = lambda x, n: ' '*n + x
        add_title = lambda x: f'[VERIFY] {x}'
        print_h1 = lambda x: print(add_title(f'{add_space(x, 0)}'))
        print_h2 = lambda x: print(add_title(f'{add_space(x, 4)}'))

        # Start
        print_h1('Compare {} tar in folder and {} services in compose:'.format(
            len(tarballs), len(services)
        ))
        base_name_tarballs = { idx:data['base_name'] for idx, data in tarballs.items() }

        # Get the invalid service
        kick_tarballs = []
        invalid_services = services.copy()

        for idx, tarball in base_name_tarballs.items():
            
            # Main service is not in compose
            if utils.is_ivit_main_tarball(tarball):
                tarballs[idx]['verify'] = 1
                print_h2('Find main service: {}'.format(tarball))
                continue

            # If tarball is correct then keep services
            need_pop = None
            for service in invalid_services:
                if utils.get_image_name(service) in tarball:
                    need_pop = service
                    tarballs[idx]['verify'] = 1
                    break
            # Else kick out tarball
            else:
                kick_tarballs.append(tarball)

            # Pop out valid service   
            if need_pop:
                invalid_services.remove(need_pop)

        # If has invalid services
        if invalid_services:
            num_services, num_invalid_services = \
                len(services), len(invalid_services)
            raise RuntimeError('Basic Services [{}/{}]: Missing {}'.format(
                num_services-num_invalid_services,
                num_services,
                ', '.join(invalid_services)))

        # Log
        # print_h2(kick_tarballs)
        # print_h2(invalid_services)

        return tarballs

    def allow_all_tarballs(self, data):
        for idx, tar in data.items():
            data[idx]['verify'] = 1

    def __init__(self, folder: str, compose_file: Optional[str]=None, manual: bool=False):
        # Init
        super().__init__(folder)
        self.handler = docker_helper.HandleDockerImage()
        
        # Find tar
        tarballs = self.find_tars( self.folder )

        # Validate with tarball and service from compose
        if compose_file:
            compose_handler = \
                docker_helper.DockerComposeHandler(compose_file)            
            self.verify_services(
                tarballs, 
                compose_handler.get_images())
        else:
            self.allow_all_tarballs(tarballs)

        # Update data variable
        self.data = tarballs

        # Rich
        self.define_table()
        self.update_table()

        # Add manual select
        if manual:
            self.valid_index = self.filter_with_index(self.data)


TEST_FOLDER='./archives'
COMPOSE_PATH='./compose.yml'
def test_ids():
    ids = DockerSaver(folder=TEST_FOLDER)
    ids.start()

def test_idl():
    idl = DockerLoader(
        folder=TEST_FOLDER,
        compose_file=COMPOSE_PATH)
    idl.start()

if __name__ == "__main__":
    test_idl()
