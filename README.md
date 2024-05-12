# Disclaimer
This is a fork of the original project by Shakajiub (https://github.com/Shakajiub/h3_map_editor) with some enhancements.

## Change log
	- Added help/h/help command to show available commands and scripts
	- Added swap_layers script
	- Added missing value of 255 (Random) to the Town class.

# h3_map_editor_plus.py
Simple command-line HoMM 3 Map Editor made with pure python. Allows you to open a map, run custom scripts to edit the map, then save it. Useful for mass changes that are tedious to make with the normal editor, or changing things that the normal map editor does not allow you to change, like passing the limits for monster or resource quantities, having Seer's Huts that want you to bring a Cannon, or reward you with the Titan's Lightning Bolt directly into your spellbook. Currently supports HotA version 1.7.1.


## Usage

```
./h3_map_editor_plus.py [filename]
```

When launching the editor, you can specify which map to open with the first argument. You can omit the ".h3m" extension and the editor will still find the file. The filepath starts in the directory of the main script.

### Commands

```
> help/h/hlp
```
Shows you a list of available commands and scripts.

```
> open [filename]
```
Can be used to open a map while the editor is running.

```
> save [filename]
```
To write your changes into a new map file. You can omit the ".h3m" extension here as well, the editor will add it if necessary. If you do not specify the filename, the map will be saved as "output.h3m".

```
> print/show [key]
```
Shows you the parsed data for a specific key (e.g. "general"). See [h3_map_editor.py](h3_map_editor.py) (map_data) for a list of all the keys.

```
> quit/q/exit
```
To exit the editor.


## Scripts

To actually make changes in the map file, you will need to use custom scripts. All scripts should be implemented in [src/scripts.py](src/scripts.py), which also has a few examples described below. Adding a custom script right now means implementing your functions in the scripts file, then adding a corresponding command to run the script in the main function. You may also use the "temp" script at the top of the file for testing your scripts.

```
> swap_layers [> swap_layers]
```
Swaps the layers in a map, including terrain, objects, and settings such as main towns and win/loss conditions.

```
count_objects [> count]
```
Is a simple example that goes through all the objects placed in the map and prints out how many copies of each object can be found.

```
generate_guards [> guards]
```
Is a more complex example. The script goes through specific objects (Pandora's Boxes, Artifacts, Resources, etc.) and checks if the last line in the object's message box is "-guards XXX". Whenever it finds that, it generates guards for the object with a total AI value of XXX, then replaces the text with a "Guarded by XYZ" description. See the script itself for a more detailed explanation.


## Contributions

Everyone is completely welcome to contribute in any way, be it by fixing typos, bugs, adding comments or useful scripts. The code needs quite a lot of cleanup, which is an ongoing project. The goal is for the editor to be as easy to use and expand as possible, especially for making custom scripts.
