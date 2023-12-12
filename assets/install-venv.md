# Install virtualenv and wrapper

## Install package and module 
```bash
sudo apt-get install python3-pip
sudo pip3 install virtualenv
sudo pip3 install virtualenvwrapper
```
## Add into environment
```bash
source $(which virtualenvwrapper.sh)
vim ~/.bashrc
```
```bash
# Add into ~/.bashrc
export WORKON_HOME=~/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
# END of ~/.bashrc
```
```bash
source ~/.bashrc
```

