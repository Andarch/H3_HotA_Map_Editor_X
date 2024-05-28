# h3_map_editor_plus v0.3

## Disclaimer
This is a fork of the original project by Shakajiub (https://github.com/Shakajiub/h3_map_editor) with some enhancements.

## Change log (since fork)
	- Added help/h/help command to show available commands and scripts
	- Added swap_layers script
	- Added missing value of 255 (Random) to the Town class.
	- Added functionality to load 2 maps and choose which one to edit when launching scripts.
	- Also can save 2 maps
	- Added town_settings and JSON export scripts
	- Added minimap generation script

# Usage

## Launch

```
./h3_map_editor_plus.py
```

## Basic Commands

```
> open | load
```
Can be used to open 1 or 2 maps while the editor is running.

```
> save
```
To write your changes into 1 or 2 new map files. You can omit the ".h3m" extension here as well, the editor will add it if necessary.

```
> h | hlp | help
```
Shows you a list of available commands and scripts.

```
> /b | /r | /back | /return
```
To back out of prompts.

```
> /quit | /q | /exit
```
To exit the editor.


## Special Commands

To actually make changes in the map file, you will need to use custom scripts. All scripts should be implemented in [src/scripts.py](src/scripts.py).

```
> count
```
Goes through all the objects placed in the map and prints out how many copies of each object can be found.

```
> export <filename>
```
Exports all map data to a .json file.

```
> guards
```
Goes through specific objects (Pandora's Boxes, Artifacts, Resources, etc.) and checks if the last line in the object's message box is "-guards XXX". Whenever it finds that, it generates guards for the object with a total AI value of XXX, then replaces the text with a "Guarded by XYZ" description. See the script itself for a more detailed explanation.

```
> minimap
```
Generates the minimap in PNG format (two PNG files if two layers).

```
> print <key>
```
Shows you the parsed data for a specific key (e.g. "general"). See [h3_map_editor_plus.py](h3_map_editor_plus.py) (map_data) for a list of all the keys.

```
> swap
```
Swaps the layers in a map, including terrain, objects, and settings such as main towns and win/loss conditions.

```
> towns
```
Enables spell research, all spells, and all buildings in all towns on the map. (This does not affect whether a spell is enabled globally, and it does not build any buildings, just enables them all.)
