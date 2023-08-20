'이미지 선택해주는 모듈. 모델 폴더 안에서 호출해서 실행해야 함'
import os
import random

def select_image(path):
    '''
    이미지 선택\n
    디렉터리 입력하면 디렉터리 내 임의 선택, 이미지 파일까지 입력하면 파일 선택\n
    디렉터리 예시: 'test'\n
    파일 예시: 'train/00000_000.jpg'\n
    '''
    full_path = os.path.join('../../data/images', path)
    if os.path.isdir(full_path):
        full_image_path = os.path.join(full_path, random.choice(os.listdir(full_path)))
    else:
        full_image_path = full_path

    print(full_image_path)
    return full_image_path

if __name__ == '__main__':
    image_path = select_image('test') # 무조건 디렉터리 출력
