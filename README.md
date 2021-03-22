# imger.py
## An implementation of Pillow for Piqueserver.

This plugin allows users to print images on the map, with emotes implemented by default.

## Requirements
Pillow, version > 5.4.0

## Installation guide
Add imger.py to your scripts folder and modify config.toml accordingly. The /img/ folder needs to be placed at the root of your piqueserver installation, alongside the already existing "game_modes", "data", "core_commands", etc.

## Adding images
Once the server is running, the script will pick up all files dropped into /img/ automatically. Images can then be added at your leisure.

Images should respect the following conditions for the plugin to behave properly:
- Be in a square format (32x32, 16x16)
- Be in .png format
- Use pure black for transparency

(Images up to 32x32 may be printed with no noticeable lag on the server. However, 64x64 may dip the tps of less fortunate players, and up to 128x128 will flat-out crash some people. It is up to the server administrator to be smart with their image sizes.)

## Usage and commands
### /img
Toggles imger on and off client-side. Also adds or removes the player's name from DISABLED_USERS.txt in /img/userdata/ so the server remembers their favored setting.

### /emotelist
Prints the name of every available image in /img/ folder.

### /emote <name>
Prints the image at the player's position. Emotes are not saved to the map, and thus are only visible to players provided they are connected at the same time as the user placing the emote. Anyone joining the server is always met with a clean map, to prevent spam and an easy way to clean up the map client-side.

## Additionnal infos
I've left some unused variables in global and processvoxels() for the case scenarios where something other than an emote wishes to be implemented and needs to behave differently (be saved to the map, bound to specific coords rather than the player position or be forcefully sent to all players.)

In the case scenario where pixels need to be saved to the map, a different global dictionary must be used for the voxel processing. VOXEL_PROC_HEAVEN is left unused for that very case scenario and can be changed/defined/renamed as wished.
