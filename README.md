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

## 🟧 Blender to 🟩 Substance to 🟦 Unreal Workflow

Take ONE simple prop all the way through (Model ➡️ UV ➡️ Texture in Substance ➡️ Import into UE). You'll hit every pipeline problem on something small and cheap to fix.

UE5 Mannequin Explained: https://www.youtube.com/watch?v=CgqYlF45fcM

* 🟧 Blender
  * **Modifiers:** Apply all modifiers. Object ➡️ Convert ➡️ Mesh
  * **Transforms:** Apply all transforms. Object Mode ➡️ CTRL+A ➡️ All Transforms (Scale, at minimum)
  * **Join all meshes:** Object Mode ➡️ CTRL+J
  * **Origins:** Set pivot for Unreal. Put it where the object should "sit". (Bottom center for props.)
  * **Normals:** Find invisible faces. Header ➡️ Overlays ➡️ Face Orientation. (Red faces will look broken or missing in Unreal.)
  * **Materials:** Keep one material per texture set and rebuild the material in Unreal. (Blender material nodes do NOT transfer.)
  * **UVs:** Every mesh needs to be unwrapped if you want textures on it.
  * **Animations:**
    * Export animations seperately to update them without wiping out your model/material setup in Unreal.
    * Animations exported are from the NLE editor. Remember to push them down.
    * Keep polycount reasonable, especially for animated characters. (No > 1 million poly assets, please)
    * If you get animations shrinking, is because the size and/or scale isnt right.
    * Root bone needs to be renamed from the default "**Armature**" otherwise import error saying the ref post is incorrect.
* 🟩 Substance Painter
  * **Export textures using the Unreal preset:** It will give you Base, Normal and ORM, AO.
  * **Unwrap from Blender:** Turn auto-unwrapping OFF.
    * You can technically use Substance Painter Auto Unwrap if you re-import the fbx into blender: Object Mode ➡️ Select Object ➡️ Link/Transfer Data ➡️ Copy UV Maps.
* 🟦 Unreal
  * **Import:** Content Drawer ➡️ New Folder ➡️ Import
    * Choose your favorite master material on the Import screen. Avoids having to re-assign dozens of bad master materials.
      * Something with Base, Normal and ORM texture slots is a great start (For Substance Textures).
  * 🔰 Common Errors
    * "Ref pose is incorrect" Your root bone is named "Armature" add a period or rename it.
