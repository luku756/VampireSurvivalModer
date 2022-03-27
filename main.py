# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import shutil
import sys

from Resources import Resources
from Packer import Packer
from Installer import Installer

from Controller import Controller

import GUI
import logging
logging.basicConfig(level=logging.INFO)


# logging.info("=" * 40)
# logging.info(f" <*> Start Install Mode")
#
# original_resource_dir_path = "resources2\\app\\.webpack\\renderer\\assets\\img"
# mode_resource_dir_path = "mode\\Holo Survivors (v0.3.2 - EA, 1.0)\\Vampire Survivors\\resources\\app\\.webpack\\renderer\\assets\\img"
#
# logging.info(f" * original path : {original_resource_dir_path}")
# logging.info(f" * mode path : {mode_resource_dir_path}")
#
# unpack_dir_name = "unpack_result"
# build_dir_name = "merge"
# repack_dir_name = "repack_result"
# resource_dir_name = "img"
#
# original_unpack_dir_name = "original"
# mode_unpack_dir_name = "mode"
# pk = Packer()
#
# # 원본 리소스 읽고 언팩
# rs1 = Resources()
# rs1.read(original_resource_dir_path)
# pk.unpack(rs1, dst_path=original_unpack_dir_name)
#
# # 모드 리소스 읽고 언팩
# rs2 = Resources()
# rs2.read(mode_resource_dir_path)
# pk.unpack(rs2, dst_path=mode_unpack_dir_name)
#
#
# # 모드 파일 비교 및 적용
# installer = Installer()
# original_unpack_dir_path = os.path.join(unpack_dir_name, original_unpack_dir_name)
# mode_unpack_dir_path = os.path.join(unpack_dir_name, mode_unpack_dir_name)
# installer.install_mode(original_unpack_dir_path, mode_unpack_dir_path, dst_path=build_dir_name)
#
# # 모드 리팩
# pk.repack(build_dir_name, dst_path=repack_dir_name)
#
# # 중간 파일 정리 (원본 언팩, 모드 언팩, 모드 병합)
# # shutil.rmtree(unpack_dir_name)
# # shutil.rmtree(build_dir_name)
#
# output_dir_path = os.path.join(repack_dir_name, resource_dir_name)
# installer.rollback_non_update_sprites(repack_dir_name, build_dir_name, original_unpack_dir_path)
#
# # 결과 파일로 원본 덮어쓰기 (설치 완료)
# # output_dir_path = os.path.join(repack_dir_name, resource_dir_name)
# # shutil.rmtree(original_resource_dir_path)  # 원본 삭제
# # shutil.copytree(output_dir_path, original_resource_dir_path)
# #
# # # 결과 파일 삭제
# # shutil.rmtree(repack_dir_name)
#
# logging.info(f" <-> Install Mode Finish\n")

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




GUI.create_gui()



# controller = Controller()
# # controller.unpack_resource("C:\\Program Files (x86)\\Steam\\steamapps\\common\\Vampire Survivors")
# controller.install_mode("C:\\Program Files (x86)\\Steam\\steamapps\\common\\Vampire Survivors", "C:\\Users\\jsl\\Downloads\\Holo Survivors (v0.3.2 - EA, 1.0)")
# controller = Controller()
# # controller.unpack_resource("resources")
# #
# # controller.repack_resource("unpack_result\img")
#
# controller.install_mode("resources2", "mode")

#
