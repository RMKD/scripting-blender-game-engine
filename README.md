# Scripting Blender Game Engine

There's a lot of great tutorials for blender game engine, but most focus on using the modules. This repository contains references to various resources organized by topic and a tutorial file I use for teaching others about blender the way I wish someone had walked me through it when I was getting started.

## This Tutorial

The `tutorial.md` file contains a detailed walkthrough of various menus and how to build basic proficiency in writing python scripts for the Blender Game Engine. [read it now](./tutorial.md)

## Other Resources

http://www.blendenzo.com/tutBeginningBGEPython.html

https://wiki.blender.org/index.php/Doc:2.6/Tutorials/Frijoles

### CGMasters Tutorials

http://www.cgmasters.net/free-tutorials/gamedev-1-intro/

http://www.cgmasters.net/free-tutorials/gamedev-2/

http://www.cgmasters.net/free-tutorials/gamedev-3-gdd/

http://www.cgmasters.net/free-tutorials/gamedev-4-modularity-odd-angles-on-blenders-grid/

http://www.cgmasters.net/free-tutorials/game-dev-5-blender-game-prototype/

http://www.cgmasters.net/free-tutorials/game-dev-6-blender-game-engine-stalking-enemy-ai/

http://www.cgmasters.net/free-tutorials/fps-mouselook-script-plus-real-text/

http://www.cgmasters.net/free-tutorials/bge-python-reading-and-writing-rotation/

http://www.cgmasters.net/free-tutorials/what-to-know-when-creating-next-gen-assets/

### Networking a game
https://www.youtube.com/watch?v=A-OY1h_iPl4 totter333

https://www.youtube.com/watch?v=G7a_DraZBU4 Agnus Hollands

https://www.youtube.com/watch?v=4xZRfzOtxzA Goran Milovanovic

### Creating a Heads Up Display (HUD)
BornCG is a great place to start: https://www.youtube.com/watch?v=QboViMztemI

VideoCopilot Tutorial: http://www.videocopilot.net/tutorials/futuristic_hud/

### Making Menus

https://www.youtube.com/watch?v=I0RFuv6IxD4

https://www.youtube.com/watch?v=iZ7lmf1wj1A

### Creating a skybox

http://andrewrgray.webs.com/storage/skybox-generator.blend

### Particle Effects

[This is a great tutorial on particles with the Cycles component](https://www.youtube.com/watch?v=azXFwQWXjyQ)

[Particles in BGE](https://www.youtube.com/watch?v=uZ41C6Be_Ok)

https://www.youtube.com/watch?v=UXs7zTtTKP4

### Texturing Objects

http://www.katsbits.com/tutorials/blender/learning-materials-textures-images.php)

### Spawning Things

http://blender.stackexchange.com/questions/21605/how-can-i-spawn-a-moving-object-in-bge


### Blender Guru on Addons and Tricks

http://www.blenderguru.com/articles/must-blender-addons/

http://www.blenderguru.com/articles/11-useful-blender-tricks-you-may-not-know/


### Creating an addon
https://www.blender.org/api/blender_python_api_2_64_9/info_tutorial_addon.html

http://michelanders.blogspot.nl/p/creating-blender-26-python-add-on.html


## adding extra python libraries

Need some more python libraries to handle data acquisition or munging? You can install directly into the Blender python environment by passing a prefix path argument to pip. (note: you should have pip3 installed )

```
# add to your ~/.bashrc
export BLENDERPATH='/Applications/blender-2.77-OSX_10.6-x86_64/blender.app/Contents'
alias blenderpip='pip3 install --install-option="--prefix=$BLENDERPATH/Resources/2.77/python"'
```


## Can I Use this stuff for VR?
Not (quite) yet - but there are several threads worth following:

* https://github.com/OpenHMD/OpenHMD
* https://github.com/ValveSoftware/openvr
* https://github.com/cedeon/hmd_sdk_bridge/tree/cedeon-vive
* https://github.com/cedeon/virtual_reality_viewport/tree/vivetest
