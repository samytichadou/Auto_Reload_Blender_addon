'''
Copyright (C) 2018 Samy Tichadou (tonton)
samytichadou@gmail.com

Created by Samy Tichadou

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


# IMPORT
##################################

from . import   (
    addon_prefs,
    properties,
    gui,
    reload,
    reload_operator,
)


# register
##################################
def register():
    addon_prefs.register()
    properties.register()
    gui.register()
    reload.register()
    reload_operator.register()

def unregister():
    addon_prefs.unregister()
    properties.unregister()
    gui.unregister()
    reload.unregister()
    reload_operator.unregister()
