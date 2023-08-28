'''
레이블 polygon 데이터로 4번째 채널 만들어서 이미지 병합\n
main(기존이미지전체폴더경로, 새로운이미지전체폴더경로, merge=True)\n
merge==True는 4차원 이미지 생성, merge==False는 1차원 이미지 생성
'''
import cv2
import os
import numpy as np
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from preprocess.restructure._settings import seg_yolo_to_aihub_mapper

def add_polygon_channel(old_image_root, new_image_root, txt_root, progress_bar, merge, file):
    '이미지에 polygon 추가'
    file: str
    # 파일 확인: dir or 기타파일
    if os.path.isdir(os.path.join(old_image_root, file)) or not (file.endswith('jpg') or file.endswith('jpeg')):
        print('')
        progress_bar.update(1)
        return
    # 파일 확인: jpg
    else:
        pass
    # path 생성
    old_image_file_path = os.path.join(old_image_root, file)
    new_image_file_path = os.path.join(new_image_root, file)
    txt_file_path = old_image_file_path.replace(old_image_root, txt_root).replace('jpg', 'txt').replace('jpeg', 'txt')
    # 원본이미지로부터 dim 추출
    raw_image = cv2.imread(old_image_file_path)
    height, width = raw_image.shape[:2]
    # fourth_channel 빈 이미지 생성
    fc_image = np.zeros((height, width, 1), np.uint8)
    # .txt 파일에서 polygon 읽어서 표기
    with open(txt_file_path, 'r') as txtfile:
        lines = txtfile.readlines()
        for line in lines:
            parts = line.strip().split()
            class_id = seg_yolo_to_aihub_mapper[int(parts[0])]
            class_id: int
            numbers = [float(p) for p in parts[1:]]
            yolo_points = [numbers[i:i+2] for i in range(0,len(numbers),2)]
            pixel_points = np.array([(int(point[0] * width), int(point[1] * height)) for point in yolo_points], dtype=np.int64)
            cv2.fillPoly(fc_image, [pixel_points], class_id)
    # 파일 저장
    new_parent_path = os.path.dirname(new_image_file_path)
    os.makedirs(new_parent_path, exist_ok=True)
    if merge:
        merged_image = cv2.merge((raw_image, fc_image))
        new_image_file_path = new_image_file_path.replace('jpg', 'png').replace('jpeg', 'png')
        cv2.imwrite(new_image_file_path, merged_image)
    else:
        cv2.imwrite(new_image_file_path, fc_image)
    progress_bar.update(1)
    return

def main(old_path, new_path, txt_path, merge):
    '모든 이미지에 polygon 추가 후 저장'
    for old_image_root, _, files in os.walk(old_path):
        new_image_root = old_image_root.replace(old_path, new_path)
        txt_root = old_image_root.replace(old_path, txt_path)
        progress_bar = tqdm(total=len(files), desc=old_image_root)
        with ThreadPoolExecutor() as executor:
            executor.map(lambda file: add_polygon_channel(old_image_root, new_image_root, txt_root, progress_bar, merge, file), files)
        progress_bar.close()

if __name__ == '__main__':
    # main('data/images_sample', 'data/images_seg_four_sample', 'data/labels_seg', True)
    main('data/images', 'data/ir', 'data/labels_seg', False)
