# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# write by SaiLing, 2013/01/10


bl_info = {
    "name": "SaiToolsKit",
    "author": "SaiLing",
    "version": (0,0,1),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar",
    "description": "My usually tools",
    "warning": "",
    "wiki_url": "https://hackmd.io/@Sai",
    "tracker_url": "",
    "category": "Generic"}

import bpy
# import imp

from . import SaiTools_ui


classes = (
    SaiTools_ui.CursorOriginPanel,
    SaiTools_ui.MaterialToolsPanel,
    SaiTools_ui.MeshToolsPanel,
    SaiTools_ui.Sai_Ui_Ops
)
    
def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    
    print("Sai is Coming")


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
  
    print("Sai is Leaving")

