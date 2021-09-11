# Auto Reload - Blender (2.9x) addon

[Auto Reload Releases](https://github.com/samytichadou/Auautoreload_to_reload_Images-Blender_addon/releases://www.example.com/my%20great%20page) 

Auto Reload is a Blender addon design to help user refresh external files (*images* and *libraries*) from inside Blender.


## **Panels**

*Auto Reload* operators are located in several places in Blender :
### Top Bar Menu
![Top Bar Menu](https://raw.githubusercontent.com/samytichadou/Auto_Reload_Blender_addon/master/help_images/top_bar_menu_open.png)

### Libraries Inspector Panel (in the *Scene Properties*)
![Libraries Inspector Panel](https://raw.githubusercontent.com/samytichadou/Auto_Reload_Blender_addon/master/help_images/libraries_inspector_panel.png)


### Images Inspector Panel (in the *Scene Properties*)
![Images Inspector Panel](https://raw.githubusercontent.com/samytichadou/Auto_Reload_Blender_addon/master/help_images/images_inspector_panel.png)

## **Operators**

### ***Reload Images* operator**
**Located in the *Top Bar Menu* and the *Images Inspector Panel***
<gif>

This operator will reload all modified images.

### ***Check Libraries* operator**
**Located in the *Libraries Inspector Panel* UI List**
<gif>

This operator will check all used Libraries for modification **without** reloading them (reloading used libraries should be let to the user to prevent some unwanted modifications).

### ***Reload Library* operator**
**Located in the *Libraries Inspector Panel* UI List**
<gif>

This operator will reload selected Library.

### ***Save and Revert* operator**
**Located in the *Top Bar Menu*, *Images Inspector Panel* and *Libraries Inspector Panel***
![Save and Revert operator](/assets/images/san-juan-mountains.jpg)

This operator will save current Blend file and reload it, all external Images and Libraries will be reloaded.

### ***Reveal in Explorer* operator**
**Located in the *Images Inspector Panel* and *Libraries Inspector Panel***
<gif>

This operator will open an explorer at the location of the selected Image/Library.

### ***Open Library* operator**
**Located in the *Libraries Inspector Panel***
<gif>

This operator will open selected Library in a Blender instance.

### ***Modify Image* operator**
**Located in the *Images Inspector Panel***
<gif>

This operator will open selected Image in an external Image Editor (specified in the *Addon Preferences*).

### ***Remove Image/Library* operator**
**Located in the *Images Inspector Panel* and *Libraries Inspector Panel***
![Remove Image/Library* operator](/assets/images/san-juan-mountains.jpg)

This operator will remove selected Image/Library from the Blend file.

### ***Check Addon Updates* operator**
**Located in the *Addon Preferences***
<gif>

This operator will check for new version of the Addon online. If found, a popup message will show User a direct link to download it.

Nb : This operator is performed at Blender startup by default (specified in the *Addon Preferences*).


## **Timer**
**Located in the *Top Bar Menu***
<gif>

The *Timer property* is a way to reload external images and check libraries for modifications at regular intervals of time (specified in the *Addon Preferences*). Every *n* seconds, Blender will look for modified Images and Libraries, and if found, will reload Images.

User can deactivate the Check for modified Libraries from the *Addon Preferences*.

## **Addon Preferences**
![Addon Preferences](https://raw.githubusercontent.com/samytichadou/Auto_Reload_Blender_addon/master/help_images/addon_preferences.png)

- **Image Timer Frequency :** 
set here the time interval for automatic Check/Reload for external Images and Libraries
- **Image Editor :** Path to executable file of Image Editor (like Gimp, Krita...)
- **Launch Image Reload Timer on Startup :**
- **Include Libraries Check in the Reload Timer :**
- **Check for Updates on Startup :**
- **Check Addon Updates operator :** Check manually for Addon Updates (see above for details)