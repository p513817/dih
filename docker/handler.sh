#!/bin/bash

# Argument checking
if [ ! "$#" -gt 1 ]; then
    echo "Usage: $0 [mode] [ubuntu] [command]"
    echo ""
    echo "Options:"
    echo " - mode: build|run"
    echo " - ubuntu: focal|20.04|jammy|22.04"
    echo " - command: only supported when 'handler.sh run'. e.g.\"bash\" "
    exit 1
fi

# Move to target path
script_dir=$(realpath $(dirname "$(dirname "$0")") )
cd "$script_dir"

# Get parameters
action="$1"
version="$2"
command="${3}"
echo $command

# Verify
# Check if the version is in the given options
if [[ "$version" =~ ^(focal|20\.04|jammy|22\.04)$ ]]; then
    # Map "20.04" or "22.04" to "focal" or "jammy"; otherwise, keep the original input
    case "$version" in
        "20.04")
        mapped_version="focal"
        ;;
        "22.04")
        mapped_version="jammy"
        ;;
        *)
        mapped_version="$version"
        ;;
    esac
else
      echo "Version $version is not a valid version option."
      exit 1
fi

version=$mapped_version
echo "Get ubuntu version: $mapped_version"

image_name="${version}-dind"
docker_file="./docker/${version}.dockerfile"

# ============================================

# Helper
check_docker_image_exists() {
    if docker inspect "$1" &> /dev/null; then
        return 0  # Image exists
    else
        return 1  # Image does not exist
    fi
}

build_docker_image() {
    docker build -t "$1" -f ${docker_file} .
}

run_docker_container() {
    docker run -it --rm --privileged \
    -w /workspace \
    -v $(pwd):/workspace \
    -v /var/run/docker.sock:/var/run/docker.sock \
    "$1" "$2"
}

if [ "$action" = "build" ]; then
    build_docker_image "$image_name"
    # if ! check_docker_image_exists "$image_name"; then
    #     echo "Image $image_name does not exist, building it..."
    #     build_docker_image "$image_name"
    # else
    #     echo "Image $image_name already exists, no need to build."
    # fi
elif [ "$action" = "run" ]; then
    run_docker_container "$image_name" "$command"
    # if check_docker_image_exists "$image_name"; then
    #     echo "Image $image_name exists, running a container..."
    #     run_docker_container "$image_name"
    # else
    #     echo "Image $image_name does not exist, please build it first."
    # fi
else
    echo "Invalid action, should be 'build' or 'run'"
    exit 1
fi