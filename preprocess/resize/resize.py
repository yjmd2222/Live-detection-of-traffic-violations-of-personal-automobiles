'''
진재님 이미지 사이즈 축소 스크립트 수정\n
data/images_pre에 축소한 이미지 저장
'''
import os
from tqdm import tqdm
import cv2
from concurrent.futures import ThreadPoolExecutor

# 원본 이미지 resize(1920x1080 → nw x nh)하여 저장
def resize(old_image_root, new_image_root, nw, keep_aspect, progress_bar, file, is_png):
    '파일 열고 이미지 사이즈 조정 후 저장'
    # dir or 기타 파일
    if os.path.isdir(os.path.join(old_image_root, file)) or not any([file.endswith(ext) for ext in ['jpg','jpeg','png']]):
        progress_bar.update(1)
        return
    # jpg
    else:
        pass
    # path 생성
    old_image_file_path = os.path.join(old_image_root, file)
    new_image_file_path = os.path.join(new_image_root, file)
    if is_png:
        new_image_file_path = new_image_file_path.split('.')[0] + '.png'
    # 파일 있으면 quit
    if os.path.isfile(new_image_file_path):
        progress_bar.update(1)
        return
    else:
        pass
    image = cv2.imread(old_image_file_path)
    if keep_aspect:
        h, w = image.shape[:2] # h,w
        nh = int(nw / w * h)
        image = cv2.resize(image, (nw,nh)) # w,h
    else:
        image = cv2.resize(image, (nw,nw))

    # 파일 저장
    new_parent_path = os.path.dirname(new_image_file_path)
    os.makedirs(new_parent_path, exist_ok=True)
    cv2.imwrite(new_image_file_path, image)
    progress_bar.update(1)

def main(old_path, new_path, nw=1280, keep_aspect=True, is_png=True):
    '이미지 resize'
    # data 폴더 / images, labels 하위 폴더 생성
    for old_image_root, _, files in os.walk(old_path):
        new_image_root = old_image_root.replace(old_path, new_path)
        progress_bar = tqdm(total=len(files), desc=old_image_root)
        with ThreadPoolExecutor() as executor:
            executor.map(lambda file: resize(old_image_root, new_image_root, nw, keep_aspect, progress_bar, file, is_png), files)
        progress_bar.close()

if __name__ == '__main__':
    # main('data/images_raw', 'D:/data/images_1280/images', 1280)
    # main('data/images_raw', 'D:/data/images_640/images', 640)
    main('data/images_raw', 'data/images_resize_png', 640)
