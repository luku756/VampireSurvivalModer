'''
Resources 인스턴스를 전달받아 unpack/repack


'''

import Resources
import os
from PIL import Image


class Packer:
    unpack_dst_path = "unpack_result"

    def __init__(self):
        print("packer")

    # 전달받은 Resources 오브젝트를 언팩
    def unpack(self, resources_instance):

        if not os.path.isdir(self.unpack_dst_path):
            os.mkdir(self.unpack_dst_path)

        resources = resources_instance.get_resources()

        for res_name in resources:
            print(res_name)
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
            if os.path.isfile(img_path):
                print(f" * {img_path} 가 이미 존재합니다. 덮어쓰기됩니다.")
            else:
                print(f" * {img_path} 에 저장!.")

            try:
                crop_img.save(img_path)  # 잘라낸 이미지를 저장. 이전 파일이 있다면 덮어쓰기됨
            except KeyError as e:
                print(e)



def test():
    img = Image.open('data/characters.png')
    print(img.size)  # (900, 1000)의 크기로 출력
    print(img.format)  # gif 포멧으로 출력

    x = 5
    y = 1
    h = 31
    w = 29

    # 이미지 잘라내기
    xy = (x, y, x + w, y + h)  # (100, 200), (600, 700)을 지나는 직사각형으로 자른다.
    crop_img = img.crop(xy)  # crop 메서드를 이용해서 자른다.
    crop_img.show()  # 이미지를 띄운다.
    crop_img.save("data/res.png")
