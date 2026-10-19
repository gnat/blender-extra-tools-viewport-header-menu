# 🧊 Blender: Extra Tools for Viewport Header Menu

Get some conveniences of Blender for Artists. Zero dependency add-on.

Adds buttons in the 3D Viewport for:

* Global Search
* Common views (Front, Top, Bottom, Left, Right, Back)
* Undo / Redo
* Import / Export
* Unreal Engine export

## 👁️ How does it look?

<img width="581" height="340" alt="image" src="https://github.com/user-attachments/assets/2aa09071-d84c-4d66-be98-048a0728fb38" />



## 🎁 Install

[Download](https://github.com/gnat/blender-extra-tools-viewport-header-menu/archive/refs/heads/main.zip) and extract `blender-extra-tools-viewport-header-menu` into your Blender addons folder.

* Linux: `~/.config/blender/5.3/scripts/addons/`
* Windows: `C:\Users\USER\AppData\Roaming\Blender Foundation\Blender\5.3\scripts\addons`

Enable it: Start Blender ➡️ Edit ➡️ Preferences ... ➡️ Add-ons ➡️ Extra Tools for Viewport Header Menu ✅

## Unreal to Blender Workflow

* Blender
  * Apply all transforms before exporting.
    * Object Mode ➡️ CTRL+A ➡️ Scale (or even All Transforms)
    * Origins: Put it where the object should "sit" (bottom center for props. It becomes the pivot in Unreal!)
  * Normals
    * Overlays ➡️ Face Orientation. Red faces will look broken or invisible in Unreal.
  * UVs
    * Every
  * Materials
    * Blender material nodes don't transfer. Keep one material per texture set and rebuild the material in Unreal.
* Unreal
  * Content Drawer ➡️ New Folder ➡️ Import
    * Choose the base master material that you can drag in your textures to. Avoid having to re-assign a bad one.
