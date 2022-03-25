'''
Resources 인스턴스를 전달받아 unpack/repack


'''

import Resources
import os
from math import ceil, floor
from PIL import Image


class Packer:
    default_unpack_dst_path = "unpack_result"

    def __init__(self):
        print("packer")
        self.unpack_dst_path = os.path.join(Packer.default_unpack_dst_path, "img")

    # 전달받은 Resources 오브젝트를 언팩
    def unpack(self, resources_instance, dst_path=""):
        if dst_path != "":  # unpack 폴더 경로
            self.unpack_dst_path = os.path.join(Packer.default_unpack_dst_path, dst_path)

        # 폴더 생성 확인
        if not os.path.isdir(self.default_unpack_dst_path):
            os.mkdir(self.default_unpack_dst_path)
        if not os.path.isdir(self.unpack_dst_path):
            os.mkdir(self.unpack_dst_path)

        resources = resources_instance.get_resources()

        for res_name in resources:
            # print(res_name)
            self.unpack_sprite(res_name, resources[res_name])

    # 하나의 스프라이트 이미지를 조각내기
    def unpack_sprite(self, resource_name, resource_object):
        root_path = Resources.Resources.img_resource_dir_path  # 리소스 홈폴더
        sprite_path = os.path.join(root_path, resource_object.filename)

        # unpack 된 리소스를 저장할 폴더 생성
        unpack_img_dir_path = os.path.join(self.unpack_dst_path, resource_name)
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

            # 원본 이미지가 잘려나가 있는 경우.
            if frame.w != frame.src_w or frame.h != frame.src_h:
                # print('so')

                # print(f'trimmed 이미지 복구! {frame.filename}')
                crop_img = self.restore_trimmed_image(crop_img, frame.src_w, frame.src_h)  # 이미지 복구

            # if os.path.isfile(img_path):
            #     print(f" * {img_path} 가 이미 존재합니다. 덮어쓰기됩니다.")
            # else:
            #     print(f" * {img_path} 에 unpacked 이미지 저장!")

            try:
                crop_img.save(img_path)  # 잘라낸 이미지를 저장. 이전 파일이 있다면 덮어쓰기됨
            except KeyError as e:
                print(e)

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

