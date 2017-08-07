# Teleport - A small alias manager
### License: [MIT]
Teleport is a small bash script to enable quick cds using folder nicknames for use in current and future shells


## Manually Install
1. Copy teleport into a folder of your choice
2. Make a directory in ~ with the name ~/.teleport and create a file named "aliases"
3. In your bashrc file or any file which your bash uses to source aliases, source the tp and aliases files
4. Go to your favorite/most used directories and add them to the script

## Command Line Install/Uninstall
### Linux/MAC or Windows with Bash Shell
```sh
# Install Teleport
$ git clone https://github.com/whitegreyblack/Teleport.git
$ cd Teleport/
$ src/install

# Uninstall Teleport 
$ src/uninstall
$ cd
$ rm -rf Teleport # to remove the script directory
```
## Script Usage
Using alias commands, teleport imports directory paths into shell to use as shortcuts
```sh
# Commands: print, add, subtract
$ tp # prints all aliases if they exist
$ tp -a [nickname] [optional: directory] # if directory not given, uses current working directory
$ tp -s [nickname]
```
Example: adding a directory nickname and using the nickname in the same shell
```sh
whitegreyblack@local ~/Documents/examplefolder/examplesubfolder
$ tp -a sub  # add cwd to tp alias list and to current shell environment
$ alias
alias sub='cd ~/Documents/examplefolder/examplesubfolder/'

whitegreyblack@local ~/Documents/examplefolder/examplesubfolder
$ cd ~

whitegreyblack@local ~
$ sub

whitegreyblack@local ~/Documents/examplefolder/examplesubfolder
$           # directory changed to current example folder
```
Example: subtracting a directory nickname from shell
```sh
whitegreyblack@local ~
$tp
alias sub='cd ~/Documents/examplefolder/examplesubfolder/'

whitegreyblack@local ~
$tp -s sum
no alias of that name

whitegreyblack@local ~
$tp -s sub
$tp
no aliases used for teleport
```
