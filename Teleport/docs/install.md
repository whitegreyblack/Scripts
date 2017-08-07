# Install
### Files created
```bash
# will hold the teleport program
~/.teleport/.teleport

# will hold the aliases used in teleport
~/.teleport/.aliases
```
### Files modified
```
# calls source on bash_aliases and teleport
~/.bashrc

# calls source on teleport aliases
~/.bash_aliases
```
### Installation Script
```bash
# checks if tp file exists in installation directory before starting installation
[ ! -f $PWD/tp ] && echo -e "Teleport not found" && exit 1

# checks the file tree to install missing folders
[ ! -d ~/.teleport ] && mkdir -p ~/.teleport

# checks the file tree to install missing files
[ ! -f ~/.teleport/.teleport ] && touch ~/.teleport/.teleport
[ ! -f ~/.teleport/.aliases ] && touch ~/.teleport/.aliases
```
