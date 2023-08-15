'이미지, txt 파일 train, val, test 셋으로 구분'
import os
import numpy as np

def train_val_test_split(train_ratio=0.8, val_ratio=0.1):
    '''
    이미지, json, txt 폴더 하위 폴더로 trian, val, test 셋으로 구분\n
    기본 구조 'data/images/image0.jpg' 등으로 가정.
    '''
    # 폴더 생성
    for folder in ['images', 'labels_json', 'labels_det', 'labels_seg']:
        for split in ['train', 'val', 'test']:
            os.makedirs(f'data/{folder}/{split}', exist_ok=True)

    # 섞기
    image_file_names = list(set(os.listdir('data/images')) - {'train', 'val', 'test'})
    np.random.seed(42)
    np.random.shuffle(image_file_names)

    # 구분 사이즈
    train_size = len(image_file_names) * train_ratio
    val_size = len(image_file_names) * val_ratio

    # 부모 디렉터리
    old_image_parent_path = 'data/images'
    old_json_parent_path = 'data/labels_json'
    old_det_txt_parent_path = 'data/labels_det'
    old_seg_txt_parent_path = 'data/labels_seg'

    print('train-val-test split 시작')
    for idx, image_file_name in enumerate(image_file_names):
        # 파일이름
        json_file_name = image_file_name.split('.')[0]+'.json'
        txt_file_name = json_file_name.replace('.json', '.txt')
        # 구분
        if idx < train_size:
            split = 'train'
        elif idx < train_size + val_size:
            split = 'val'
        else:
            split = 'test'

        # paths
        old_image_file_path = os.path.join(old_image_parent_path, image_file_name)
        old_json_file_path = os.path.join(old_json_parent_path, json_file_name)
        old_det_txt_file_path = os.path.join(old_det_txt_parent_path, txt_file_name)
        old_seg_txt_file_path = os.path.join(old_seg_txt_parent_path, txt_file_name)
        new_image_file_path = os.path.join(old_image_parent_path, split, image_file_name)
        new_json_file_path = os.path.join(old_json_parent_path, split, json_file_name)
        new_det_txt_file_path = os.path.join(old_det_txt_parent_path, split, txt_file_name)
        new_seg_txt_file_path = os.path.join(old_seg_txt_parent_path, split, txt_file_name)

        # 이동
        os.replace(old_image_file_path, new_image_file_path)
        os.replace(old_json_file_path, new_json_file_path)
        os.replace(old_det_txt_file_path, new_det_txt_file_path)
        os.replace(old_seg_txt_file_path, new_seg_txt_file_path)
        if idx % 100 == 0:
            print(f'{idx}번째 파일 이동')

    print('train-val-test split 종료')

if __name__ == '__main__':
    train_val_test_split()