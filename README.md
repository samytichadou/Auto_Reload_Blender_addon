# Auto Reload - Blender addon

**This addon is available from the [Blender Extension Platform](https://extensions.blender.org/add-ons/auto-reload/) and directly inside Blender (from the *Preferences*, *Get Extensions* category)**  

[Auto Reload Releases](https://github.com/samytichadou/Auto_Reload_Blender_addon/releases)  

Auto Reload is a Blender addon design to automatically refresh external files when modified (*images, movie clips, libraries, sound and cache files*).  

A timer will look every n seconds for modified external files, if there is some, they will be reloaded inside Blender  

If you like this addon, you can help me [here](https://ko-fi.com/tonton_blender) through Donation, to buy me a coffee and allow me to continue to develop free tools.
___

## **UI**

*Auto Reload* interface :  

### - ***Popover***

![Popover](https://raw.githubusercontent.com/samytichadou/Auto_Reload_Blender_addon/master/resources/graphics/autoreload_img01_popover.jpg)

Handy accessible menu located in the right part of the topbar to quickly activate/deactivate *Timer* through the *stopwatch button*, and select what to reload from the popover.

### - ***Preferences***

![Addon Preferences](https://raw.githubusercontent.com/samytichadou/Auto_Reload_Blender_addon/master/resources/graphics/autoreload_img02_prefs.jpg)

- **Timer Frequency :** 
set here the time interval for automatic Check/Reload for external files
- **On Startup section :** Setup general behavior of the addon on Blender startup

___

## **Known Issues**

- Cache files (*alembic and usd*) can be *sequential* (one file per frame for animation). This is not supported for now. 
If any user has some sample sequential cache files to test the addon, it could be implemented quickly.
