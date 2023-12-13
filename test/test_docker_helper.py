import sys
import os
import docker
import subprocess
import pytest

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(parent_dir)

from src.dih.docker_helper import FindDockerImage, SaveDockerImage, LoadDockerImage, is_name_includes, is_name_excludes

@pytest.fixture(scope="module")
def docker_client():
    return docker.from_env()

@pytest.fixture(scope="module")
def ubuntu_latest_image(docker_client):
    # 下载 ubuntu:latest 镜像
    docker_client.images.pull("ubuntu:latest")
    return "ubuntu:latest"

@pytest.fixture(scope="module")
def docker_saver():
    return SaveDockerImage()

@pytest.fixture(scope="module")
def docker_loader():
    return LoadDockerImage()

@pytest.fixture(scope="function")
def get_ubuntu_name(tmp_path):
    return os.path.join(tmp_path, "ubuntu_latest.tar")

def test_save_docker_image(docker_client, docker_saver, get_ubuntu_name, ubuntu_latest_image):
    output_file = get_ubuntu_name
    process = docker_saver.save(ubuntu_latest_image, output_file )
    process.wait()
    assert os.path.exists(output_file)
    assert output_file.endswith(".tar")

def test_save_docker_image_wait(docker_client, docker_saver, get_ubuntu_name, ubuntu_latest_image):
    output_file = get_ubuntu_name
    process = docker_saver.save(ubuntu_latest_image, output_file, wait=True )
    assert os.path.exists(output_file)
    assert output_file.endswith(".tar")

def test_load_docker_image(docker_client, docker_saver, docker_loader, get_ubuntu_name, ubuntu_latest_image):
    output_file = get_ubuntu_name

    docker_saver.save(ubuntu_latest_image, output_file, wait=True )
    assert os.path.exists(output_file)

    # Remove docker image
    docker_client.images.remove(ubuntu_latest_image)

    # 加载 tar 文件中的镜像
    process = docker_loader.load(output_file)
    process.wait()

    # 确保加载成功
    assert process.returncode == 0

    # 检查加载后的镜像是否存在
    loaded_image = docker_client.images.get(ubuntu_latest_image)
    assert loaded_image is not None

