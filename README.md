# **H3 HotA Map Editor X <small>v0.3</small>**
### **Supports HotA v1.7.1**

This is a fork of the original project by Shakajiub (https://github.com/Shakajiub/h3_map_editor).

The goal of **H3 HotA Map Editor X** is to build upon the foundations of the original program and provide additional functionality for editing maps for Heroes 3: Horn of the Abyss. Eventually there will be a GUI version.

><small>**Note:** The editor can load two maps at a time. Currently, there's no reason to do so, but soon the `swap` script will support swapping map layers between two different maps, giving you up to four layers to work with.</small>

## Launching the editor
><small>**Note:** In the future, there will be an installer/executable. For now, use the below methods to launch the editor.</small>

><small>**Note:** Loading a map on launch has been temporarily disabled  due to the modifications that allow two maps to be loaded simultaneously. Support for loading one map / two maps on launch will be added in the future.</small>  

### Windows
Run this .bat file: `H3 HotA Map Editor X.bat`

### **Linux / macOS**
Run this command in a terminal: `./H3_HotA_Map_Editor_X.py`

## Basic commands

`help`&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;`h`  
Shows you a list of basic commands and script commands.

><small>**Tip:** You can omit the .h3m extension when loading/saving a map via the next two commands below.</small>

`load`&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;`open`  
Allows you to open either one or two map files.  
You will be prompted to enter how many maps to open and then to enter the filename(s).

`save`  
Allows you to save your changes into a new map file(s).  
You will be prompted to enter one or two filenames depending on how many maps you have loaded.

><small>**Note:** The below commands are preceded by `/` so they aren't interpreted as filenames during load/save prompts.</small>

`/back`&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;`/return`&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;`/b`&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;`/r`  
Backs out of prompts.

`/exit`&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;`/quit`&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;`/e`&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;`/q`  
Exits the editor.

## Script commands

The commands in this section run scripts for various purposes including:
- Changing map data
- Displaying map data for reference
- Exporting file types other than .h3m (e.g., .json, .png)

The following commands are supported:

`count`  
Displays how many instances of each object type there are.

`export <filename>.json`  
Exports all map data to a .json file.  
> <small>**Note:** Currently, you must include the `.json` extension when typing the filename.</small>

`minimap`  
Generates the minimap image(s) in PNG format.

`print <key>`  
Displays the parsed data for a specific data key.  
> <small>**Note:** See [Data keys](#data-keys) for a list of keys.</small>

`swap`  
Swaps the layers in a map, including terrain, objects, and settings such as main towns and win/loss conditions.

`towns`  
Enables spell research, all spells, and all buildings in all towns on the map. (This does not affect whether a spell is enabled globally, and it does not build any buildings, just enables them all.)

### Data keys
The following data keys can be used with the `print <key>` command (replace `<key>` with one of the keys below) to specify what category of parsed data you want to display:

`general`  
`player_specs`  
`conditions`  
`teams`  
`start_heroes`  
`ban_flags`  
`rumors`  
`hero_data`  
`terrain`  
`object_defs`  
`object_data`  
`events`  
`null_bytes`  
