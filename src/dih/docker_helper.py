import yaml
import sys
import os
import subprocess
from collections import defaultdict
from typing import Optional, List
import docker

sys.path.append(os.path.dirname(__file__))
from utils import is_name_excludes, is_name_includes, YamlFile

class FindDockerImage:
    """Find docker image via specific rule."""

    def find(self, includes: Optional[list]=None, excludes: Optional[list]=None) -> dict[dict]:
        """Find docker image and filter with the includes_key and excludes_key

        Args:
            includes (Optional[list], optional): the image name includes. Defaults to None.
            excludes (Optional[list], optional): the image name excludes. Defaults to None.

        Returns:
            dict[dict]: the docker image data with an index.

        Examples:
            {
                0: {
                    id: <id>,
                    repo: <repo>,
                    created: <created>,
                    size: <size>,
                }, ...
            }
        """
        client = docker.from_env()
        total_images = client.images.list()
        valid_images = defaultdict(dict)
        valid_number = 0
        
        for image in total_images:
            
            if not image.attrs["RepoTags"]: continue

            repo_tag = image.attrs["RepoTags"][0]

            # Ensure the image name is fit the rule
            is_correct = ( is_name_excludes(repo_tag, excludes) \
                and is_name_includes(repo_tag, includes))
            if not is_correct: continue
            
            valid_images[valid_number].update({
                "id": image.id,
                "repo": repo_tag,
                "created": image.attrs["Created"],
                "size": image.attrs["Size"],
            })
            valid_number += 1
        
        return valid_images

class SaveDockerImage:
    """An object to save docker image"""

    def save(self, image_name:str, output_file:str, wait:bool=False):
        if not output_file.endswith('.tar'):
            raise TypeError('Only support tarball file.')

        proc = subprocess.Popen(["docker", "save", "-o", output_file, image_name])

        if wait:
            return proc.wait()
        else:
            return proc

class LoadDockerImage:
    """An object to load docker image"""

    def load(self, input_file: str, wait:bool=False):
        if not os.path.exists(input_file):
            raise FileNotFoundError('The tarball file not found. ({})'.format(input_file))

        proc = subprocess.Popen(f"docker load -i {input_file} > /dev/null", shell=True)

        if wait:
            return proc.wait()
        else:
            return proc
        
class HandleDockerImage(FindDockerImage, SaveDockerImage, LoadDockerImage):
    """Docker Handler with several features

    Args:
        FindDockerImage: find the docker image with specific rule.
        SaveDockerImage: Save the docker image with the image name.
        LoadDockerImage: Load the docker image with tarball file.
    """

# ========================

class DockerComposeHandler(YamlFile):
    
    def __init__(self, yaml_path:str):
        super().__init__(yaml_path)
    
    def get_services(self) -> list:
        """Get the name of all services. 

        Returns:
            list: return a list of services 
        """
        return list(self.content["services"].keys())
    
    def get_images(self) -> list:
        """Get the image name of all services.

        Returns:
            list: return a list of the image of each services.
        """
        return [ serv["image"] for serv in self.content["services"].values() ]

if __name__ == "__main__":
    
    DCH = DockerComposeHandler( yaml_path="./compose.yml" )

    print(DCH.get_services())
    print(DCH.get_images())
    

