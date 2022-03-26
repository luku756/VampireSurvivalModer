import os
import shutil

filename = 'Vampire Survival Moder'

# 빌드하기
# os.system(f'pyinstaller -F -n "{filename}" main.py)  # 처음 실행
os.system(f'pyinstaller -F -n "{filename}" "Vampire Survival Moder.spec"')  # spec 수정 후 이걸로 실행
