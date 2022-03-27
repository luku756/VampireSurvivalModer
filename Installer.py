'''
기존 리소스와 현재 리소스를 비교, 업데이트한다.

절차
- 원본 읽기, 언팩
- 모드 읽기, 언팩 (언팩이 필요한 경우 - json이 있는 경우)

'''
import os
import shutil
import json
import logging
from PIL import Image, ImageChops

class Installer:

    # mode 가 설치된 결과물 폴더
    build_path = "merge"

    def __init__(self):
        self.original_resource_list = []
        self.mode_resource_list = []
        self.original_path = ""
        self.mode_path = ""

    def install_mode(self, original_path, mode_path, dst_path=""):
        self.original_path = original_path
        self.mode_path = mode_path

        # 두 리소스를 비교, 설치해야 하는 파일만 남김.
        self.compare_mode()

        # 설치
        if dst_path == "":
            build_path = self.build_path
        else:
            build_path = dst_path
        if os.path.isdir(build_path):  # 기존이 있으면 삭제
            shutil.rmtree(build_path)
        # os.mkdir(build_path)

        # 원본을 복사
        shutil.copytree(self.original_path, build_path)

        # 모드 파일을 복사
        for path in self.mode_resource_list:
            if os.path.basename(path) == 'trimmed_list.json':  # 이 파일은 덮어쓰기가 아닌 병합이 필요.
                self.combine_trimmed_list(build_path, path)
            elif os.path.basename(path) != 'json_skeleton.json':  # 스켈레톤 파일은 덮어쓰지 않음. 원본의 것 사용
                # 복사해서 덮어쓰기
                src_path = self.mode_path + path
                shutil.copy(src_path, build_path + path)

        # 업데이트 여부 확인
        # non_update_list = self.check_sprite_update_image_compare(build_path, original_path)
        # 업데이트 되지 않은 파일은 원본의 것으로 복구

    # 원본과 모드의 비교
    def compare_mode(self):
        logging.info("\nStart Compare Original and Mode")
        self.load_resource_list()

        remove_list = []

        # 모드에 있는 모든 파일이 원본에 존재하는지 체크, 원본에 없는 파일은 제거.
        for path in self.mode_resource_list:
            # if path not in self.original_resource_list and "illustrations.png" not in path:  # illustrations.png 는 예외 todo: 제거
            if path not in self.original_resource_list:  # illustrations.png 는 예외 todo: 제거
                remove_list.append(path)
                logging.warning(f" * {path} not in original!!!")

        for path in remove_list:
            self.mode_resource_list.remove(path)

        logging.info(f" * Mode has {len(self.mode_resource_list)} resource images.")

    # 원본과 모드에 있는 리소스 목록 가져오기
    def load_resource_list(self):
        for root, directory, files in os.walk(self.original_path):
            for file in files:
                path = os.path.join(root, file)
                path = path.replace(self.original_path, "")  # root path 제외
                self.original_resource_list.append(path)

        for root, directory, files in os.walk(self.mode_path):
            for file in files:
                path = os.path.join(root, file)
                path = path.replace(self.mode_path, "")  # root path 제외
                self.mode_resource_list.append(path)

    # 원본과 모드의 trimmed_list 를 합쳐서 하나의 파일로 저장.
    def combine_trimmed_list(self, build_path, path):
        path = path[1:]   # 앞쪽에 \ 가 붙어있음

        original_trimmed_path = os.path.join(self.original_path, path)
        with open(original_trimmed_path, "r") as f:
            json_str = f.read()
            trimmed_json = json.loads(json_str)

        mode_trimmed_path = os.path.join(self.mode_path, path)
        with open(mode_trimmed_path, "r") as f:
            json_str = f.read()
            mode_json = json.loads(json_str)

        # mode 에 있는 건 덮어쓰기
        for item in mode_json:
            trimmed_json[item] = mode_json[item]

        # trimmed_list 저장
        with open(os.path.join(build_path, path), "w") as f:
            f.write(json.dumps(trimmed_json))

    # unpack 상태의 이미지를 비교하여 모드로 인한 업데이트 여부 확인
    # 업데이트 되지 않은 스프라이트 목록 리턴
    def check_sprite_update_image_compare(self, merge_resource_dir_path, original_unpack_resource_dir_path):

        logging.info(f"\nStart Check Update Sprite.")

        non_update_list = []

        merge_sprite_path = os.path.join(merge_resource_dir_path, "sprite")
        original_sprite_path = os.path.join(original_unpack_resource_dir_path, "sprite")
        # 스프라이트 목록
        sprite_list = os.listdir(merge_sprite_path)
        for sprite_name in sprite_list:
            merge_path = os.path.join(merge_sprite_path, sprite_name)
            original_path = os.path.join(original_sprite_path, sprite_name)

            logging.info(f" * check sprite {sprite_name}")
            update_flag = self.compare_sprite_images(merge_path, original_path)

            if update_flag:
                logging.info(f"   > {sprite_name} is updated by mode.")
            else:
                non_update_list.append(sprite_name)
        print(non_update_list)
        return non_update_list

    # noinspection PyMethodMayBeStatic
    # 각 이미지를 비교하여 스프라이트의 업데이트 여부 확인
    def compare_sprite_images(self, merge_path, original_path):

        update_flag = False

        # key : filename, value : 이미지 경로
        merge_resource_list = {}
        original_resource_list = {}

        # 모드와 합쳐진 리소스
        file_list = os.listdir(merge_path)
        for path in file_list:
            ext = os.path.splitext(path)  # 파일 확장자
            if ext[1] == '.png':
                img_path = os.path.join(merge_path, path)
                merge_resource_list[path] = img_path

        # 원본 리소스
        file_list = os.listdir(original_path)
        for path in file_list:
            ext = os.path.splitext(path)  # 파일 확장자
            if ext[1] == '.png':
                img_path = os.path.join(original_path, path)
                original_resource_list[path] = img_path

        # 리소스 비교
        for img_name in merge_resource_list:
            if img_name not in original_resource_list:
                logging.warning(f"{img_name} 가 merge 에는 있는데 original 에 없다?!")
            else:
                # 알파를 비교하지 못함.
                new_image = Image.open(merge_resource_list[img_name]).convert('RGBA')
                original_image = Image.open(original_resource_list[img_name]).convert('RGBA')

                diff = ImageChops.difference(new_image, original_image)

                if diff.getbbox():
                    update_flag = True
                    return update_flag

        return update_flag

    # repack 후 업데이트 되지 않은 스프라이트를 확인하고 원본의 png 와 json 을 사용한다.
    def rollback_non_update_sprites(self, repack_path, original_unpack_path, merge_path):
        non_update_list = self.check_sprite_update_image_compare(merge_path, original_unpack_path)


