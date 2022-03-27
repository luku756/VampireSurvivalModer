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

    # 각 json 이 업데이트된 파일인지 아닌지 확인.
    # 생각해보면 원본과 모드의 크기가 동일하면 적용 안되겠네. 제대로 하려면 unpack 상태에서 (merge와 original unpack) 이미지를 다 비교해야 한다. ...무겁겠네...
    def check_sprite_update(self, new_resource_path, original_resource_path):

        new_resource_json_list = {}
        original_resource_json_list = {}

        # 모드와 합쳐진 리소스
        file_list = os.listdir(new_resource_path)
        for path in file_list:
            ext = os.path.splitext(path)  # 파일 확장자
            if ext[1] == '.json':
                json_path = os.path.join(new_resource_path, path)
                with open(json_path, "r") as f:
                    json_str = f.read()
                    json_object = json.loads(json_str)
                    new_resource_json_list[ext[0]] = json_object
                    # new_resource_json_list.append(json_object)

        # 원본 리소스
        file_list = os.listdir(original_resource_path)
        for path in file_list:
            ext = os.path.splitext(path)  # 파일 확장자
            if ext[1] == '.json':
                json_path = os.path.join(original_resource_path, path)
                with open(json_path, "r") as f:
                    json_str = f.read()
                    json_object = json.loads(json_str)
                    original_resource_json_list[ext[0]] = json_object
                    # new_resource_json_list.append(json_object)

        for json_name in new_resource_json_list:
            update_flag = self.compare_json_frames(new_resource_json_list[json_name], original_resource_json_list[json_name])


    # 두 json 의 frame 들이 동일한지 확인. (frame 의 x,y는 무시)
    def compare_json_frames(self, target_1, target_2):
        frames_1 = target_1["textures"][0]["frames"]
        frames_2 = target_2["textures"][0]["frames"]

        # 파일명 순서로 정렬
        # frames_1.sort(key=lambda x: x['filename'])
        # frames_2.sort(key=lambda x: x['filename'])

        frame1_dict = {}
        frame2_dict = {}

        for frame_name in frames_1:
            frame1_dict[os.path.splitext(frame_name['filename'])[0]] = frame_name
        for frame_name in frames_2:
            frame2_dict[os.path.splitext(frame_name['filename'])[0]] = frame_name

        # print(f"compare {target_1['textures'][0]['image']}")
        # print(f" resource size : {len(frame1_dict)}, {len(frame2_dict)}")
        if len(frame1_dict) != len(frame2_dict):
            print("왜 다르지?")

        update_flag = False

        for i, frame_name in enumerate(frame1_dict):
            if frame_name not in frame2_dict:
                print(f"{frame_name}가 원본에 없음!!!.")
            else:
                # print(f"{i} : {frame_name}, {frame2_dict[frame_name]['filename']}")
                f1, f2 = frame1_dict[frame_name], frame2_dict[frame_name]
                if f1["trimmed"] != f2["trimmed"] or f1["sourceSize"] != f2["sourceSize"] or \
                        f1["spriteSourceSize"] != f2["spriteSourceSize"] or \
                        f1["frame"]['w'] != f2["frame"]['w'] or f1["frame"]['h'] != f2["frame"]['h']:
                    update_flag = True
                    break
                    # print(f"변동 사항 확인. {frame_name} is updated resource.")
                    # print(f1)
                    # print(f2)

        if update_flag:
            print(f"{target_1['textures'][0]['image']} 는 업데이트 된 리소스입니다.")
        else:
            print(f"{target_1['textures'][0]['image']} 는 모드로 인해 업데이트되지 않았습니다. 원본 사용.")



        return update_flag
