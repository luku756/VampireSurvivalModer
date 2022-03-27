'''
전체 기능을 관리하는 컨트롤러

'''
import os
import shutil

from Resources import Resources
from Packer import Packer
from Installer import Installer


import logging


class Controller:
    resource_dir_name = "img"  # img 만 지원
    unpack_dir_name = "unpack_result"  # 언팩 리소스가 들어가는 폴더
    repack_dir_name = "repack_result"
    build_dir_name = "merge"  # 모드 병합 결과가 들어가는 폴더

    # def __init__(self):
    #     logging.info("controller")

    # 리소스를 언팩한다.
    def unpack_resource(self, resource_path):
        logging.info("=" * 40)
        # img 찾기
        dir_path = self.find_dir_path(resource_path)
        if dir_path == "":  # 없음
            logging.error(" <X> img 폴더를 찾을 수 없습니다.")
            # print(" <X> img 폴더를 찾을 수 없습니다.")
            return None
        else:
            logging.info(f" <*> Start Unpack Resources")
            # print(f" <*> Start Unpack Resources")

        # 리소스 읽기
        rs = Resources()
        rs.read(dir_path)

        # 리소스 언팩
        pk = Packer()
        abspath = pk.unpack(rs)  # 폴더 경로 미지정

        logging.info(f" <-> Unpack Resources Finish\n")
        return abspath

    # 리소스를 다시 패킹한다.
    def repack_resource(self, unpack_resource_path):
        logging.info("=" * 40)
        logging.info(f" <*> Start Repack Resources")

        # 폴더 확인
        if not os.path.isdir(os.path.join(unpack_resource_path, "single")) or \
                os.path.isdir(os.path.join(unpack_resource_path, "sprite")):
            logging.error(f" <X> {unpack_resource_path} 는 unpack 폴더가 아닙니다.")
            return None

        pk = Packer()
        abspath = pk.repack(unpack_resource_path, dst_path=self.repack_dir_name)

        logging.info(f" <-> Repack Resources Finish\n")
        return abspath

    # 모드를 설치한다.
    # 원본 언팩, 모드 언팩, 컴바인, 리팩, 업데이트 비교, 비 업데이트 사항 롤백
    def install_mode(self, original_resource_path, mode_path):
        logging.info("=" * 40)
        logging.info(f" <*> Start Install Mode")

        original_resource_dir_path = self.find_dir_path(original_resource_path)
        mode_resource_dir_path = self.find_dir_path(mode_path)

        if original_resource_dir_path == "" or mode_resource_dir_path == "":
            logging.error(f" <X> {self.resource_dir_name} 폴더를 찾을 수 없습니다! ")
            return None

        logging.info(f" * original path : {original_resource_dir_path}")
        logging.info(f" * mode path : {mode_resource_dir_path}")

        original_unpack_dir_name = "original"
        mode_unpack_dir_name = "mode"
        pk = Packer()

        # 원본 리소스 읽고 언팩
        rs1 = Resources()
        rs1.read(original_resource_dir_path)
        pk.unpack(rs1, dst_path=original_unpack_dir_name)

        # 일러스트 하드코딩
        if os.path.isfile(os.path.join(mode_resource_dir_path, "illustrations.png")) and \
            not os.path.isfile(os.path.join(mode_resource_dir_path, "illustrations.json")):
            shutil.copy(os.path.join(original_resource_dir_path, "illustrations.json"), os.path.join(mode_resource_dir_path, "illustrations.json"))

        # 모드 리소스 읽고 언팩
        rs2 = Resources()
        rs2.read(mode_resource_dir_path)
        pk.unpack(rs2, dst_path=mode_unpack_dir_name)


        # 모드 파일 비교 및 적용
        installer = Installer()
        original_unpack_dir_path = os.path.join(self.unpack_dir_name, original_unpack_dir_name)
        mode_unpack_dir_path = os.path.join(self.unpack_dir_name, mode_unpack_dir_name)
        installer.install_mode(original_unpack_dir_path, mode_unpack_dir_path, dst_path=self.build_dir_name)

        # 모드 리팩
        pk.repack(self.build_dir_name, dst_path=self.repack_dir_name)

        # 중간 파일 정리 (원본 언팩, 모드 언팩, 모드 병합)
        shutil.rmtree(self.unpack_dir_name)
        shutil.rmtree(self.build_dir_name)

        # installer.check_sprite_update(self.repack_dir_name, self.resource_dir_name)

        # 결과 파일로 원본 덮어쓰기 (설치 완료)
        output_dir_path = os.path.join(self.repack_dir_name, self.resource_dir_name)
        shutil.rmtree(original_resource_dir_path)  # 원본 삭제
        shutil.copytree(output_dir_path, original_resource_dir_path)

        # 결과 파일 삭제
        shutil.rmtree(self.repack_dir_name)

        logging.info(f" <-> Install Mode Finish\n")
        return original_resource_dir_path

    # img 폴더를 찾아서 리턴한다.
    def find_dir_path(self, path):
        find_path = ""
        for root, directory, files in os.walk(path):
            for dir_name in directory:
                if dir_name == self.resource_dir_name:  # find
                    find_path = os.path.join(root, dir_name)
                    return find_path
        return find_path

