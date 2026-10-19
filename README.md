# 🧊 Blender: Game Art Quick Tools

Adds often used features for Game Developers into the header bar. Tiny, zero dependency add-on. 

* Quick switch viewpoints. Switch orientations more intuitively (inspired by [Blender for Artists](https://www.bforartists.de/)).
* Quick Import / Export
* Special **Unreal Engine** export (inspired by [Blend File Importer](https://www.fab.com/listings/5f84f927-88b0-44b1-8757-ac2caccab624))
* Quick Global Search

## 👁️ How does it look?

<img alt="image" src="https://github.com/user-attachments/assets/33eef43c-f531-43cf-9f7e-5faaca40a9ec" />

## 🎁 Install

[Download](https://github.com/gnat/blender-game-art-quick-tools/archive/refs/heads/main.zip) and extract `blender-game-art-quick-tools` into your Blender addons folder.

* Linux: `~/.config/blender/5.3/scripts/addons/`
* Windows: `C:\Users\USER\AppData\Roaming\Blender Foundation\Blender\5.3\scripts\addons`

Enable it: Start Blender ➡️ Edit ➡️ Preferences ... ➡️ Add-ons ➡️ Extra Tools for Viewport Header Menu ✅

## Unreal to Blender Workflow

Take ONE simple prop all the way through (Model ➡️ UV ➡️ Texture in Substance ➡️ Import into UE). You'll hit every pipeline problem on something small and cheap to fix.

* Blender
  * Apply all transforms before exporting.
    * Object Mode ➡️ CTRL+A ➡️ Scale (or even All Transforms)
    * Origins: Put it where the object should "sit" (bottom center for props. It becomes the pivot in Unreal!)
  * Normals
    * Overlays ➡️ Face Orientation. Red faces will look broken or invisible in Unreal.
  * Materials
    * Blender material nodes don't transfer. Keep one material per texture set and rebuild the material in Unreal.
  * UVs
    * Every mesh needs to be unwrapped if you want textures on it
  * Animations
    * Export animations seperately to update them without wiping out your model/material setup in Unreal.
    * Animations exported are from the NLE editor. Remember to push them down.
* Unreal
  * Content Drawer ➡️ New Folder ➡️ Import
    * Choose your favorite master material on the Import screen. Avoids having to re-assign dozens of bad master materials.
      * Something with Base, Normal and ORM texture slots is a great start (For Substance Textures).
