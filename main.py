# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from Resources import Resources
from Packer import Packer
from Installer import Installer

from Controller import Controller


#
# rs = Resources()
# rs.read()
# # #rs.parse_resource("UI")
# #
# pk = Packer()
# pk.unpack(rs)
# # #
# #
# holo_path = "mode\\Holo Survivors (v0.3.2 - EA, 1.0)\\Vampire Survivors\\resources\\app\\.webpack\\renderer\\assets\\img"
#
# rs = Resources()
# rs.read(holo_path)
#
# pk = Packer()
# pk.unpack(rs, "홀로")
#
#
#
# original_path = "unpack_result\\img"
# mode_path = "unpack_result\\홀로"
#
# ins = Installer()
# ins.install_mode(original_path, mode_path)
#
# unpack_path = "build"
#
# pk = Packer()
# pk.repack(unpack_path)


controller = Controller()
# controller.unpack_resource("resources")
#
# controller.repack_resource("unpack_result\img")

controller.install_mode("resources2", "mode")

#
