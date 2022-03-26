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
    json_skeleton_name = "json_skeleton.json"

    default_pack_dst_path = "repack_result"
    root_dir_name = "img"  # 루트 폴더명

    def __init__(self):
        self.unpack_dir_path = ""
        self.sprite_resource_dir_path = ""  # 스프라이트 형태의 리소스를 언팩해서 저장하는 위치
        self.single_resource_dir_path = ""  # 단일 파일 리소스를 언팩해서 저장하는 위치
        self.pack_src_dir_path = ""  # 재압축 시 원본 파일의 위치
        self.pack_dir_path = ""  # 재압축 시 최종적으로 파일들이 들어갈 위치

    # 전달받은 Resources 오브젝트를 언팩
    def unpack(self, resources_instance, dst_path=""):
        if dst_path != "":  # unpack 폴더 경로
            self.unpack_dir_path = os.path.join(Packer.default_unpack_dst_path, dst_path)
        else:
            self.unpack_dir_path = os.path.join(Packer.default_unpack_dst_path, "img")

        self.sprite_resource_dir_path = os.path.join(self.unpack_dir_path, "sprite")
        self.single_resource_dir_path = os.path.join(self.unpack_dir_path, "single")

        print(f"Start Unpack Resources")
        print(f" * output path : {self.unpack_dir_path}")


        # 폴더 생성
        if not os.path.isdir(self.default_unpack_dst_path):
            os.mkdir(self.default_unpack_dst_path)

        # 기존 데이터 제거
        if os.path.isdir(self.unpack_dir_path):
            shutil.rmtree(self.unpack_dir_path)
        os.mkdir(self.unpack_dir_path)
        os.mkdir(self.sprite_resource_dir_path)
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

        return os.path.abspath(self.unpack_dir_path)

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
            print(f" * {sprite_path} is error!!!  json size: ({resource_object.w} / {resource_object.h}), real size : {img.size}")

        img_list = resource_object.get_image_list()

        for frame in img_list:
            area = frame.get_area()  # 잘라낼 사각형 범위
            crop_img = img.crop(area)  # crop 메서드를 이용해서 자른다.
            img_path = os.path.join(unpack_img_dir_path, frame.filename)

            # todo : 이거 필요한지 확인.
            # 원본 이미지가 잘려나가 있는 경우 복구. (필요한가?)
            if frame.w != frame.src_w or frame.h != frame.src_h:
                json_obj = {"sourceSize": {"w": frame.src_w, "h": frame.src_h},
                            "spriteSourceSize": {"x": frame.sprite_x, "y": frame.sprite_y},
                            "frame": {"w": frame.w, "h": frame.h}}
                trimmed_list[frame.filename] = json_obj
                # crop_img = self.restore_trimmed_image(crop_img, frame.src_w, frame.src_h)  # 이미지 복구

            try:
                crop_img.save(img_path)  # 잘라낸 이미지를 저장. 이전 파일이 있다면 덮어쓰기됨
            except KeyError as e:
                print(e)

        # trimmed_list 저장
        with open(os.path.join(unpack_img_dir_path, self.trimmed_json_name), "w") as f:
            f.write(json.dumps(trimmed_list))

        # json_skeleton 저장
        with open(os.path.join(unpack_img_dir_path, self.json_skeleton_name), "w") as f:
            f.write(json.dumps(resource_object.get_json_skeleton()))

    # noinspection PyMethodMayBeStatic
    # trim 된 이미지를 원본의 모습으로 복구
    def restore_trimmed_image(self, trimmed_image, original_w, original_h):
        # todo : 실제로 구현하려면, 원본 json 의 spriteSourceSize x,y 값을 보고 하는 것이 엄밀하다. 꼭 양방향이 일정하게 잘리는게 아님.
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

    # unpack 된 리소스를 다시 packing
    def repack(self, unpacked_path, dst_path=""):
        print(f"Start Packing Resources")
        print(f" * input path : {unpacked_path}")
        self.pack_src_dir_path = unpacked_path

        # 폴더 경로
        if dst_path == "":
            pack_path = self.default_pack_dst_path
        else:
            pack_path = dst_path

        if os.path.isdir(pack_path):  # 기존이 있으면 삭제
            shutil.rmtree(pack_path, ignore_errors=True)

        os.mkdir(pack_path)
        self.pack_dir_path = os.path.join(pack_path, self.root_dir_name)
        os.mkdir(self.pack_dir_path)

        print(f" * output path : {self.pack_dir_path}")

        # 스프라이트 리소스 packing
        self.pack_sprite_resources()

        # 단일 파일 복사
        self.copy_single_resources()

        return self.pack_dir_path

    # 단일 파일 복사
    def copy_single_resources(self):
        # unpack 은 single 파일에 담겨있지만, packed 상태에서는 그냥 img 안에 들어가있음
        single_dir_src_path = os.path.join(self.pack_src_dir_path, "single")
        single_dir_dst_path = self.pack_dir_path

        for file in os.listdir(single_dir_src_path):
            src_path = os.path.join(single_dir_src_path, file)
            dst_path = os.path.join(single_dir_dst_path, file)
            shutil.copy(src_path, dst_path)
            # print(f" * move single resource [{src_path}] to [{dst_path}]")

    # 스프라이트 리소스 packing
    def pack_sprite_resources(self):
        sprite_dir_src_path = os.path.join(self.pack_src_dir_path, "sprite")

        # sprite dir list
        sprite_list = os.listdir(sprite_dir_src_path)

        for sprite in sprite_list:
            print(f" > pack sprite - {sprite}")
            sprite_dir_path = os.path.join(sprite_dir_src_path, sprite)

            # json 파일. 뼈대를 json_skeleton.json 파일에서 가져온다.
            skeleton_path = os.path.join(sprite_dir_path, self.json_skeleton_name)

            with open(skeleton_path, "r") as f:
                json_str = f.read()
                sprite_json = json.loads(json_str)

            # print(sprite_json)

            # trimmed 된 리소스 목록
            trimmed_list_path = os.path.join(sprite_dir_path, self.trimmed_json_name)

            with open(trimmed_list_path, "r") as f:
                json_str = f.read()
                trimmed_list = json.loads(json_str)

            # print(trimmed_list)

            # 스프라이트 시트 계산
            resource_positions, sheet_size = self.calculate_sprite_sheet_size(sprite_dir_path)
            # print(resource_positions)
            # print(f"시트 사이즈 : {sheet_size[0]}, {sheet_size[1]}")

            # 스프라이트 시트 생성
            self.create_sheet_and_json(resource_positions, sheet_size, sprite_dir_path, sprite_json)

    # noinspection PyMethodMayBeStatic
    # 스프라이트 시트(texture atlas) 에 각 이미지가 위치할 영역 계산
    # 리턴 : resource_positions, (w, h)
    def calculate_sprite_sheet_size(self, target_sprite_dir):

        resource_list = os.listdir(target_sprite_dir)
        resource_metas = []

        for resource in resource_list:
            ext = os.path.splitext(resource)
            if ext[1] == '.png':  # png 만 지원
                img_path = os.path.join(target_sprite_dir, resource)
                with Image.open(img_path) as img:  # 크기 가져오기
                    # print(f"{resource} size : {img.size[0]}, {img.size[1]}")
                    resource_metas.append({"name": resource, "w": img.size[0], "h": img.size[1]})

        # 줄바꿈 너비
        max_width = 1024
        # 각 이미지 리소스가 스프라이트 시트에서 차지할 위치
        resource_positions = {}  # key : name, value : (x, y, w, h)

        now_x = 0  # 현재 오른쪽 끝 x 값 (커서 위치)
        now_top = 0  # 현재 라인의 y 값 (천장)
        this_line_max_y = 0  # 이번 라인의 최대 y값
        max_line_width = 0  # 전체 라인의 최대 width

        for resource in resource_metas:
            # print(f"step for {resource}, now_x:{now_x}, now_top:{now_top}, this_line_max_y:{this_line_max_y}, max_line_width:{max_line_width}")
            if now_x + resource['w'] < max_width:  # 이번 라인에 추가할 수 있음
                resource_positions[resource['name']] = (now_x, now_top, resource['w'], resource['h'])
                now_x = now_x + resource['w'] + 1  # 커서 이동
                this_line_max_y = max(resource['h'], this_line_max_y)  # 라인 높이 계산
                max_line_width = max(now_x, max_line_width)  # 최대 가로 크기 계산
            else:  # 줄바꿈
                max_line_width = max(now_x, max_line_width)  # 최대 가로 크기 계산
                now_top = now_top + this_line_max_y + 1  # y 커서 추가 (다음 라인)
                resource_positions[resource['name']] = (0, now_top, resource['w'], resource['h'])
                # 초기화
                now_x = resource['w']
                this_line_max_y = resource['h']

        sheet_width = max_line_width
        sheet_height = now_top + this_line_max_y

        return resource_positions, (sheet_width, sheet_height)

    # 시트 작성
    def create_sheet_and_json(self, resource_positions, sheet_size, sprite_dir_path, sprite_json):
        resource_name = os.path.basename(sprite_dir_path)

        # trimmed_list 가져오기
        trimmed_list_path = os.path.join(sprite_dir_path, self.trimmed_json_name)
        with open(trimmed_list_path, "r") as f:
            json_str = f.read()
            trimmed_list = json.loads(json_str)

        # 시트에 크기 정보 기록
        sprite_json["textures"][0]["size"]["w"] = sheet_size[0]
        sprite_json["textures"][0]["size"]["h"] = sheet_size[1]
        frame_list = sprite_json["textures"][0]["frames"]

        # 최종적인 이미지
        sprite_sheet = Image.new("RGBA", sheet_size, (255, 255, 255, 0))

        for resource in resource_positions:  # key : 파일명
            img_path = os.path.join(sprite_dir_path, resource)
            with Image.open(img_path) as img:  # 크기 가져오기
                if img.mode == 'P':
                    img = img.convert("RGBA")
                    # print(f"{resource} is convert to RGBA")
                # 시트에 이미지 넣기
                sprite_sheet.paste(img, (resource_positions[resource][0], resource_positions[resource][1]))

            # json 정보 작성
            x, y, w, h = resource_positions[resource]  # frame 정보
            trimmed = False
            # trimmed 되지 않은 디폴트 옵션
            sprite_source_size_x, sprite_source_size_y = 0, 0
            source_size_w, source_size_h = w, h

            if resource in trimmed_list:  # trim 된 이미지
                # trimmed_list 에 적혀있는 파일 크기(frame)와, 현재 파일 크기가 같으면 동일 파일로 본다.
                # 파일 크기가 변화한 경우 모드로 수정한 리소스로 본다.
                # print(f"{resource} 는 trimmed resource 입니다.")
                trimmed_data = trimmed_list[resource]
                if trimmed_data["frame"]["w"] == w and trimmed_data["frame"]["h"] == h:  # 파일 변경 없음. trimmed 상태
                    trimmed = True
                    source_size_w, source_size_h = trimmed_data["sourceSize"]["w"], trimmed_data["sourceSize"]["h"]
                    # w, h 는 frame 과 같음.
                    sprite_source_size_x, sprite_source_size_y = trimmed_data["spriteSourceSize"]["x"], trimmed_data["spriteSourceSize"]["y"]
                # else:
                #     print("-----변경됐네요??????")

            frame = {
                "filename": resource,
                "rotated": False,
                "trimmed": trimmed,
                "sourceSize": {
                    "w": source_size_w,
                    "h": source_size_h
                },
                "spriteSourceSize": {
                    "x": sprite_source_size_x,
                    "y": sprite_source_size_y,
                    "w": w,
                    "h": h
                },
                "frame": {
                    "x": x,
                    "y": y,
                    "w": w,
                    "h": h
                }
            }
            frame_list.append(frame)

        # resource json 저장
        with open(os.path.join(self.pack_dir_path, resource_name+".json"), "w") as f:
            f.write(json.dumps(sprite_json))

        # 시트 저장
        sprite_sheet_path = os.path.join(self.pack_dir_path, resource_name+".png")
        sprite_sheet.save(sprite_sheet_path)
