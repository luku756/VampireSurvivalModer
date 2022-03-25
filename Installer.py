'''
기존 리소스와 현재 리소스를 비교, 업데이트한다.

절차
- 원본 읽기, 언팩
- 모드 읽기, 언팩 (언팩이 필요한 경우 - json이 있는 경우)

'''
import os
import shutil


class Installer:

    # mode 가 설치된 결과물 폴더
    build_path = "build"

    def __init__(self):
        print()
        self.original_resource_list = []
        self.mode_resource_list = []
        self.original_path = ""
        self.mode_path = ""

    def install_mode(self, original_path, mode_path):
        self.original_path = original_path
        self.mode_path = mode_path

        # 두 리소스를 비교, 설치해야 하는 파일만 남김.
        self.compare_mode()

        # 설치
        build_path = self.build_path
        if os.path.isdir(build_path):  # 기존이 있으면 삭제
            shutil.rmtree(build_path, ignore_errors=True)
        # os.mkdir(build_path)

        # 원본을 복사
        shutil.copytree(self.original_path, build_path)

        # 모드 파일을 복사
        for path in self.mode_resource_list:
            src_path = self.mode_path + path
            shutil.copy(src_path, build_path + path)


    # 원본과 모드의 비교
    def compare_mode(self):
        print("Start Compare Original and Mode")
        self.load_resource_list()

        # 모드에 있는 모든 파일이 원본에 존재하는지 체크, 원본에 없는 파일은 제거.
        for path in self.mode_resource_list:
            if path not in self.original_resource_list:
                self.mode_resource_list.remove(path)
                print(f" * {path} not in original!!!")

        print(f"Mode has {len(self.mode_resource_list)} resource images.")

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
