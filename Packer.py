'''
Resources 인스턴스를 전달받아 unpack/repack


'''
import json

import Resources
import os
from math import ceil, floor
from PIL import Image
import shutil


class Packer:
    default_unpack_dst_path = "unpack_result"
    trimmed_json_name = "trimmed_list.json"

    def __init__(self):
        self.unpack_dst_path = ""
        self.sprite_resource_dir_path = ""  # 스프라이트 형태의 리소스를 언팩해서 저장하는 위치
        self.single_resource_dir_path = ""  # 단일 파일 리소스를 언팩해서 저장하는 위치

    # 전달받은 Resources 오브젝트를 언팩
    def unpack(self, resources_instance, dst_path=""):
        if dst_path != "":  # unpack 폴더 경로
            self.unpack_dst_path = os.path.join(Packer.default_unpack_dst_path, dst_path)
        else:
            self.unpack_dst_path = os.path.join(Packer.default_unpack_dst_path, "img")

        self.sprite_resource_dir_path = os.path.join(self.unpack_dst_path, "sprite")
        self.single_resource_dir_path = os.path.join(self.unpack_dst_path, "single")

        print(f"Start Unpack resources to {self.unpack_dst_path}")

        # 폴더 생성 확인
        if not os.path.isdir(self.default_unpack_dst_path):
            os.mkdir(self.default_unpack_dst_path)
        if not os.path.isdir(self.unpack_dst_path):
            os.mkdir(self.unpack_dst_path)
        if not os.path.isdir(self.sprite_resource_dir_path):
            os.mkdir(self.sprite_resource_dir_path)
        if not os.path.isdir(self.single_resource_dir_path):
            os.mkdir(self.single_resource_dir_path)

        root_path = resources_instance.get_resource_dir_path()  # 리소스 홈폴더
        resources = resources_instance.get_sprite_resources()

        for res_name in resources:
            # print(res_name)
            self.unpack_sprite(root_path, res_name, resources[res_name])

        # sprite 가 아닌 리소스를 복사
        non_sprite_resources = resources_instance.get_single_resources()
        for res_name in non_sprite_resources:
            shutil.copy(non_sprite_resources[res_name], os.path.join(self.single_resource_dir_path, res_name))

    # 하나의 스프라이트 이미지를 조각내기
    def unpack_sprite(self, root_path, resource_name, resource_object):
        sprite_path = os.path.join(root_path, resource_object.filename)
        trimmed_list = {}  # trimmed 된 이미지 정보를 저장. key : 파일명, value : (w, h, src_w, src_h)

        # unpack 된 리소스를 저장할 폴더 생성
        unpack_img_dir_path = os.path.join(self.sprite_resource_dir_path, resource_name)
        if not os.path.isdir(unpack_img_dir_path):
            os.mkdir(unpack_img_dir_path)

        # 이미지 열기
        img = Image.open(sprite_path)

        # 이미지 크기 오류 체크
        if img.size[0] != resource_object.w or img.size[1] != resource_object.h:
            print(f"{sprite_path} is error!")
            print((resource_object.w, resource_object.h))
            print(img.size)

        img_list = resource_object.get_image_list()

        for frame in img_list:
            area = frame.get_area()  # 잘라낼 사각형 범위
            crop_img = img.crop(area)  # crop 메서드를 이용해서 자른다.
            img_path = os.path.join(unpack_img_dir_path, frame.filename)

            # todo : 이거 필요한지 확인.
            # 원본 이미지가 잘려나가 있는 경우 복구. (필요한가?)
            if frame.w != frame.src_w or frame.h != frame.src_h:
                json_obj = {"sourceSize": {"w": frame.src_w, "h": frame.src_h}, "frame": {"w": frame.w, "h": frame.h}}
                trimmed_list[frame.filename] = json_obj
                # crop_img = self.restore_trimmed_image(crop_img, frame.src_w, frame.src_h)  # 이미지 복구

            try:
                crop_img.save(img_path)  # 잘라낸 이미지를 저장. 이전 파일이 있다면 덮어쓰기됨
            except KeyError as e:
                print(e)

        # trimmed_list 저장
        with open(os.path.join(unpack_img_dir_path, self.trimmed_json_name), "w") as f:
            f.write(json.dumps(trimmed_list))

    # noinspection PyMethodMayBeStatic
    # trim 된 이미지를 원본의 모습으로 복구
    def restore_trimmed_image(self, trimmed_image, original_w, original_h):
        width, height = trimmed_image.size
        trimmed_width = original_w - width
        margin_width = (int(floor(trimmed_width / 2)), int(ceil(trimmed_width / 2)))
        trimmed_height = original_h - height
        margin_height = (int(floor(trimmed_height / 2)), int(ceil(trimmed_height / 2)))

        # print(f"trimmed now: ({width}, {height}) / add: ({trimmed_width}, {trimmed_height}) , start with ({margin_width[0]}, {margin_height[0]})")

        # 팔레트 모드인 경우, RGBA 로 변환.
        if trimmed_image.mode == 'P':
            trimmed_image = trimmed_image.convert("RGBA")
        result = Image.new(trimmed_image.mode, (original_w, original_h), (255, 255, 255, 0))
        result.paste(trimmed_image, (margin_width[0], margin_height[0]))

        return result

