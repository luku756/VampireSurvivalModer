'''
기본 리소스를 읽어들인다.

Vampire Survivors 폴더 안의 리소스 중 resources\app\.webpack\renderer\assets\img 내의 리소스를 사용.
json이 존재하는 파일만을 대상으로 한다.

C:\Program Files (x86)\Steam\steamapps\common\Vampire Survivors\resources\app\.webpack\renderer\assets\img
'''

import os
import json


class Resources:
    img_resource_dir_path = "resources\\app\\.webpack\\renderer\\assets\\img"

    def __init__(self):
        self.resource_name_list = []  # 리소스 종류(이름)
        self.resources = {}  # key : 리소스 이름, value : ResourceObject

    # 리소스 읽기
    def read(self):
        print('Resource Read Start')
        self.get_json_resource()

    # 목록 중에서 json 이 존재하는 파일만 추출
    def get_json_resource(self):
        file_list = os.listdir(self.img_resource_dir_path)
        for path in file_list:
            ext = os.path.splitext(path)  # 파일 확장자
            if ext[1] == '.json':
                self.resource_name_list.append(ext[0])
        print(self.resource_name_list)

        for res in self.resource_name_list:
            self.parse_resource(res)

    # json 파일 읽어들이기
    def parse_resource(self, resource_name):
        json_path = os.path.join(self.img_resource_dir_path, resource_name + ".json")
        with open(json_path, "r") as f:
            json_str = f.read()
            json_object = json.loads(json_str)

            obj = ResourceObject(resource_name, json_object)
            self.resources[resource_name] = obj

    # resources 리턴
    def get_resources(self):
        return self.resources


# json 형태로 된 리소스의 정보와 목록
class ResourceObject:
    title = ""
    image_list = []  # 이미지 목록. ResourceImage 배열
    
    def __init__(self, title, json_object):
        self.title = title
        self.image_list = []
        # print(title)
        # print(json_object)

        textures = json_object["textures"][0]  # 0번만 사용됨
        self.filename = textures["image"]


        self.format = textures["format"]
        self.w = textures["size"]["w"]
        self.h = textures["size"]["h"]
        self.scale = textures["scale"]

        # 메타 정보
        self.meta = json_object["meta"]

        # 각 프레임(개별 이미지) 읽어들이기
        self.parse_images(textures["frames"])

    # 각 이미지 정보를 수집하여 저장
    def parse_images(self, json_list):
        for img in json_list:
            resource_image = ResourceImage(img)
            self.image_list.append(resource_image)

    def get_image_list(self):
        return self.image_list


# 개별 이미지 리소스 정보
class ResourceImage:

    def __init__(self, json_obj):
        self.filename = json_obj["filename"]

        print(self.filename)
        if 'psd' in self.filename.lower():
            print(self.filename)

        # psd 타입으로 저장 불가. png 로 변환
        ext = os.path.splitext(self.filename)  # 파일 확장자
        if ext[1].lower() == ".psd":
            self.filename = ext[0] + '.png'

        self.rotated = json_obj["rotated"]
        self.trimmed = json_obj["trimmed"]
        self.x = json_obj["frame"]["x"]
        self.y = json_obj["frame"]["y"]
        self.w = json_obj["frame"]["w"]
        self.h = json_obj["frame"]["h"]

        if self.w != json_obj["spriteSourceSize"]["w"] or self.h != json_obj["spriteSourceSize"]["h"]:
            if not self.trimmed:  # trimmed 된 경우, 원본의 크기와 frame 상의 크기가 달라질 수 있음.
                self.src_w = json_obj["spriteSourceSize"]["w"]
                self.src_h = json_obj["spriteSourceSize"]["h"]
            else:
                print("this is bug... " + self.filename)
        else:
            self.src_w = self.w
            self.src_h = self.h

    # 스프라이트 이미지상에서의 영역. (x, y, x + w, y + h)
    def get_area(self):
        return self.x, self.y, self.x + self.w, self.y + self.h

    
