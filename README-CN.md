README 语言（Language）：[中文版](https://github.com/samytichadou/Auto_Reload_Blender_addon/blob/master/README-CN.md)、[英文版（English）](https://github.com/samytichadou/Auto_Reload_Blender_addon/blob/master/README.md)

# Auto Reload - Blender (2.9x) 插件

[Auto Reload 发布](https://github.com/samytichadou/Auto_Reload_Blender_addon/releases)  

Auto Reload 是一种 Blender 插件，可帮助用户从 Blender 内部刷新外部文件（*图像* 和 *库*）。

这是插件的展示视频 
https://www.youtube.com/watch?v=EwUSCX48Lkw

如果你喜欢这个插件，你可以[通过捐赠](https://ko-fi.com/tonton_blender)来帮助我，给我买杯咖啡，让我继续开发免费工具。
___

## **面板**

*Auto Reload* 操作模块位于 Blender 的几个地方：

### - ***顶部菜单***

![顶部菜单](https://raw.githubusercontent.com/samytichadou/Auto_Reload_Blender_addon/master/help_images/top_bar_menu_open.png)

方便访问的菜单可快速切换 *Timer* 或 *Reload* 和 *Check* 图像/库。您还可以从此处*保存并还原* Blend 文件。

### - *库检查器面板*（在*场景属性*中）

![Libraries Inspector 面板](https://raw.githubusercontent.com/samytichadou/Auto_Reload_Blender_addon/master/help_images/libraries_inspector_panel.png)

从此处管理库，可以访问 Blend 文件中使用的外部库的*名称*和*路径*。
*显示*、*在 Blender 实例中打开*、*重新加载* 或 *删除*。  

*库名称*上方的文件图标显示用户*库*已修改。

![Modified Library](https://raw.githubusercontent.com/samytichadou/Auto_Reload_Blender_addon/master/help_images/modified_library.png)

### - *Images Inspector 面板* (在*场景属性*中)

![Images Inspector 面板](https://raw.githubusercontent.com/samytichadou/Auto_Reload_Blender_addon/master/help_images/images_inspector_panel.png)

从此处管理图像，可以访问Blend文件中使用的外部图像的*名称*和*路径*。
*Preview* 子面板允许用户检查所选图像。
在图像编辑器中*显示*、*修改*或*删除*。
___

## **操作**

### - ***Reload Images* 操作**
**位于*顶栏菜单*和*图像检查器面板*中**

![Top Bar Reload Images operator](https://raw.githubusercontent.com/samytichadou/Auto_Reload_Blender_addon/master/help_images/topbar_reload_images.png)
![Reload Images operator](https://raw.githubusercontent.com/samytichadou/Auto_Reload_Blender_addon/master/help_images/reload_images.png)

此操作将重新加载所有修改的图像。

### - ***Check Libraries* 操作**
**位于*顶栏菜单*和*库检查器面板*UI列表中**

![Top Bar Check Libraries operator](https://raw.githubusercontent.com/samytichadou/Auto_Reload_Blender_addon/master/help_images/topbar_check_libraries.png)
![Check Libraries operator](https://raw.githubusercontent.com/samytichadou/Auto_Reload_Blender_addon/master/help_images/check_libraries.png)

该操作将检查所有使用过的库是否有修改**而无需**重新加载它们（应该让用户重新加载使用过的库以防止一些不需要的修改）。

### - ***Reload Library* 修改**
**位于 *Libraries Inspector 面板* 的UI列表中**

![Reload Library operator](https://raw.githubusercontent.com/samytichadou/Auto_Reload_Blender_addon/master/help_images/reload_library.png)

此操作将重新加载选定的库。

### - ***Save and Revert* 操作**
**位于*顶栏菜单*、*Images Inspector 面板*和*Libraries Inspector 面板*中**

![Top Bar Save and Revert operator](https://raw.githubusercontent.com/samytichadou/Auto_Reload_Blender_addon/master/help_images/topbar_save_revert.png)
![Images Save and Revert operator](https://raw.githubusercontent.com/samytichadou/Auto_Reload_Blender_addon/master/help_images/images_save_revert.png)
![Libraries Save and Revert operator](https://raw.githubusercontent.com/samytichadou/Auto_Reload_Blender_addon/master/help_images/libraries_save_revert.png)

此操作将保存当前的 Blend 文件并重新加载，所有外部图像和库都将重新加载。


### - ***Reveal in Explorer* 操作**
**位于 *Images Inspector 面板*和 *Libraries Inspector 面板*中**

![Reveal Image in Explorer](https://raw.githubusercontent.com/samytichadou/Auto_Reload_Blender_addon/master/help_images/reveal_image.png)
![Reveal Library in Explorer](https://raw.githubusercontent.com/samytichadou/Auto_Reload_Blender_addon/master/help_images/reveal_library.png)

此操作将在所选图像/库的位置打开一个资源管理器。


### - ***Open Library* 操作**
**位于 *Libraries Inspector 面板*中**

![Open Library* operator](https://raw.githubusercontent.com/samytichadou/Auto_Reload_Blender_addon/master/help_images/open_library.png)

该操作将在 Blender 实例中打开选定的库。


### - ***Modify Image* 操作**
**位于 *Images Inspector 面板*中**

![Modify Image operator](https://raw.githubusercontent.com/samytichadou/Auto_Reload_Blender_addon/master/help_images/modify_image.png)

此操作将在外部图像编辑器（在*插件首选项*中指定）中打开选定的图像。


### - ***Remove Image/Library* 操作**
**位于*Images Inspector 面板* 和*Libraries Inspector 面板*中**

![Remove Image operator](https://raw.githubusercontent.com/samytichadou/Auto_Reload_Blender_addon/master/help_images/remove_image.png)
![Remove Library operator](https://raw.githubusercontent.com/samytichadou/Auto_Reload_Blender_addon/master/help_images/remove_library.png)

此操作符将从 Blend 文件中删除选定的图像/库。


### - ***Check Addon Updates* 操作**
**位于 *插件首选项*中**

![Check Addon Updates operator](https://raw.githubusercontent.com/samytichadou/Auto_Reload_Blender_addon/master/help_images/check_addon_updates.png)

该操作将在线检查插件的新版本。如果找到，弹出消息将向用户显示直接下载链接。

注：默认情况下，此运算符在 Blender 启动时执行（在 *插件首选项* 中指定）。

___

## **Timer**
**位于 *顶部菜单*中**

![Timer](https://raw.githubusercontent.com/samytichadou/Auto_Reload_Blender_addon/master/help_images/timer.png)

*Timer 属性* 是一种重新加载外部图像并定期检查库是否有修改的方法（在 *插件首选项* 中指定）。每隔 *n* 秒，Blender 将查找修改过的图像和库，如果找到，将重新加载图像。  

如果 *Timer* 打开，用户将在*顶部菜单*标题旁边看到*秒表图标*。  

用户可以从*插件首选项*中停用检查修改的库。

___

## **插件首选项**

![Addon Preferences](https://raw.githubusercontent.com/samytichadou/Auto_Reload_Blender_addon/master/help_images/addon_preferences.png)

- **Image Timer Frequency :** 在此设置外部图像和库的自动检查/重新加载的时间间隔
- **Image Editor :** 图像编辑器（如 Gimp、Krita 等）的可执行文件路径
- **Launch Image Reload Timer on Startup :** 在启动时启动图像重新加载计时器
- **Include Libraries Check in the Reload Timer :** 在重新加载计时器中包含库检查
- **Check for Updates on Startup :** 启动时检查更新
- **Check Addon Updates operator :** 手动检查插件更新（详见上文）

___

## **已知问题**

在 *Linux*（也可能是 *Mac*）上，*Reveal File* 操作不会在打开的资源管理器窗口中选择文件。

*VSE* 中的*Image Strips* 不会使用*Auto Reload* 进行更新，Blender 将它们作为单独的实体进行管理。处理这些问题在路线图中，但目前尚未整合。

从 *Inspector 面板* 重命名图像/库将更改列表顺序，*Preview Image 子面板*不会刷新，直到用户更改突出显示的列表条目。
