import pytest
import os
import sys

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(parent_dir)
from src.dih import utils

def test_convert_bytes():
    # 测试不需要文本形式的情况
    assert utils.convert_bytes(1024, "KB") == 1.0
    assert utils.convert_bytes(1048576, "MB") == 1.0
    assert utils.convert_bytes(1073741824, "GB") == 1.0
    assert utils.convert_bytes(1099511627776, "TB") == 1.0
    
    # 测试需要文本形式的情况
    assert utils.convert_bytes(1024, "KB", need_text=True) == "1.0 KB"
    assert utils.convert_bytes(1048576, "MB", need_text=True) == "1.0 MB"
    assert utils.convert_bytes(1073741824, "GB", need_text=True) == "1.0 GB"
    assert utils.convert_bytes(1099511627776, "TB", need_text=True) == "1.0 TB"

    # 测试不支持的单位
    with pytest.raises(TypeError):
        utils.convert_bytes(1024, "XB")

def test_is_name_includes():
    assert utils.is_name_includes("abcdef", ["abc", "def"], True) is True
    assert utils.is_name_includes("abcdef", ["ghi", "jkl"], True) is False
    assert utils.is_name_includes("abcdef", ["ghi", "jkl"], False) is False
    assert utils.is_name_includes("abcdef", ["ghi", "abc"], True) is False
    assert utils.is_name_includes("abcdef", [], True) is True

def test_is_name_excludes():
    assert utils.is_name_excludes("abcdef", ["abc", "def"]) is False
    assert utils.is_name_excludes("abcdef", ["ghi", "jkl"]) is True
    assert utils.is_name_excludes("abcdef", ["ghi", "abc"]) is False
    assert utils.is_name_excludes("abcdef", []) is True

def test_is_tarball(tmp_path):
    tarball_path = os.path.join(tmp_path, "test.tar")
    open(tarball_path, "w").close()
    assert utils.is_tarball(tarball_path) == tarball_path

    with pytest.raises(FileNotFoundError):
        utils.is_tarball("nonexistent_file.tar")

    with pytest.raises(TypeError):
        utils.is_tarball("test.txt")

def test_split_archive_name_ext():
    assert utils.split_archive_name_ext("test.tar.gz") == ("test", ".tar.gz")
    assert utils.split_archive_name_ext("test.tar") == ("test", ".tar")
    assert utils.split_archive_name_ext("test.zip") == ("test", ".zip")
    
    with pytest.raises(TypeError):
        utils.split_archive_name_ext("test.aaa")
        utils.split_archive_name_ext("test.txt")
        utils.split_archive_name_ext("test.t")

def test_get_base_archive_name():
    assert utils.get_base_archive_name("/path/to/file.tar.gz") == "file"
    assert utils.get_base_archive_name("/path/to/file.tar") == "file"
    assert utils.get_base_archive_name("/path/to/file.zip") == "file"

    with pytest.raises(TypeError):
        utils.split_archive_name_ext("test.aaa")
        utils.split_archive_name_ext("test.txt")
        utils.split_archive_name_ext("test.t")

def test_valid_docker_image_name():
    valid_image_names = [
        "ubuntu:latest",
        "my-registry/my-app:v1",
        "another-registry/nginx:1.19.2"
    ]
    for image_name in valid_image_names:
        assert utils.is_valid_docker_image_name(image_name)

def test_invalid_docker_image_name():
    invalid_image_names = [
        "invalid/image/name:",
        "too many/slashes/in/name:/tag",
        "no/tag/at/all"
    ]
    for image_name in invalid_image_names:
        assert not utils.is_valid_docker_image_name(image_name)

def test_get_image_name():
    valid_image_names = [
        ("ubuntu:latest", "ubuntu"),
        ("my-registry/my-app:v1", "my-app"),
        ("another-registry/nginx:1.19.2", "nginx")
    ]
    for input_service, expected_name in valid_image_names:
        assert utils.get_image_name(input_service) == expected_name

def test_get_image_name_invalid():
    invalid_image_names = [
        "invalid/image/name:",
        "too many/slashes/in/name:/tag",
        "no/tag/at/all"
    ]
    for image_name in invalid_image_names:
        try:
            utils.get_image_name(image_name)
        except TypeError as e:
            assert str(e) == 'Unexpected docker image name, please follow the rule: [registry/][namespace/]repository_name[:tag]'

def test_is_ivit_main_tarball_valid():
    assert utils.is_ivit_main_tarball("ivit-i-nvidia:v2.5-service.tar") is True
    assert utils.is_ivit_main_tarball("ivit-i-intel:v1.0-runtime.tar") is True
    assert utils.is_ivit_main_tarball("ivit-i-intel:v1.0-runtime.tar.gz") is True

def test_is_ivit_main_tarball_invalid():
    assert utils.is_ivit_main_tarball("invalid-image-name.tar.gz") is False
    assert utils.is_ivit_main_tarball("custom-image:latest.tar.gz") is False
