import sys
import os
import docker
import subprocess
import pytest
import docker

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(parent_dir)

from src.handler import (
    DockerSaver
)

@pytest.fixture(scope="module")
def docker_client():
    return docker.from_env()

@pytest.fixture(scope="module")
def ivit_nginx(docker_client):
    repo = "innodiskorg/ivit-i-nginx:1.23.4-bullseye"
    docker_client.images.pull(repo)
    return repo

@pytest.fixture(scope="function")
def get_path(tmp_path):
    folder = os.path.join(tmp_path, "docker_images")
    os.makedirs(folder)
    return folder

def test_filter_images_with_index_valid_input(get_path, monkeypatch, ivit_nginx):
    monkeypatch.setattr('builtins.input', lambda _: '0')
    ids = DockerSaver(get_path)
    assert ids.valid_index == [0]

def test_filter_images_with_index_all(get_path, monkeypatch, ivit_nginx):
    monkeypatch.setattr('builtins.input', lambda _: 'all')
    ids = DockerSaver(get_path)
    assert len(ids.valid_index)>0

def test_filter_images_with_index_invalid_input(get_path, monkeypatch, ivit_nginx):
    monkeypatch.setattr('builtins.input', lambda _: "a,b,c")
    with pytest.raises(TypeError):
        ids = DockerSaver(get_path)

def test_filter_images_with_index_out_of_range(get_path, monkeypatch, ivit_nginx):
    monkeypatch.setattr('builtins.input', lambda _: "100")
    with pytest.raises(IndexError):
        ids = DockerSaver(get_path)

def test_filter_images_with_index_out_of_range_2(get_path, monkeypatch, ivit_nginx):
    monkeypatch.setattr('builtins.input', lambda _: "0,100")
    ids = DockerSaver(get_path)
    assert len(ids.valid_index)==1
