'샘플링 코드'
import os
import random
import shutil
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

def sample_files():
    'data/images/train 등에 있는 파일 1/5 비율로 샘플링'
    folder_names = ['train', 'val', 'test']
    image_folder_paths = [os.path.join('data/images/', folder) for folder in folder_names]

    for folder_path in image_folder_paths:
        for old_image_root, _, image_file_names in os.walk(folder_path):
            image_file_names = random.sample(image_file_names, len(image_file_names)//5)
            progress_bar = tqdm(total=len(image_file_names), desc=f'{folder_path} 샘플링')
            old_image_root: str
            old_json_root = old_image_root.replace('images', 'labels_json')
            old_det_txt_root = old_json_root.replace('_json', '_det')
            old_seg_txt_root = old_det_txt_root.replace('_det', '_seg')
            new_image_root = old_image_root.replace('images', 'images_sample')
            new_json_root = new_image_root.replace('images', 'labels_json')
            new_det_txt_root = new_json_root.replace('_json', '_det')
            new_seg_txt_root = new_det_txt_root.replace('_det', '_seg')
            for new_root in [new_image_root, new_json_root, new_det_txt_root, new_seg_txt_root]:
                os.makedirs(new_root, exist_ok=True)
            def parallel(image_file_name: str):
                image_file_name: str
                json_file_name = image_file_name.split('.')[0] + '.json'
                txt_file_name = json_file_name.replace('.json', '.txt')

                old_image_file_path = os.path.join(old_image_root, image_file_name)
                old_json_file_path = os.path.join(old_json_root, json_file_name)
                old_det_txt_file_path = os.path.join(old_det_txt_root, txt_file_name)
                old_seg_txt_file_path = os.path.join(old_seg_txt_root, txt_file_name)
                new_image_file_path = os.path.join(new_image_root, image_file_name)
                new_json_file_path = os.path.join(new_json_root, json_file_name)
                new_det_txt_file_path = os.path.join(new_det_txt_root, txt_file_name)
                new_seg_txt_file_path = os.path.join(new_seg_txt_root, txt_file_name)
                for path_tuple in zip([old_image_file_path, old_json_file_path, old_det_txt_file_path, old_seg_txt_file_path],
                                    [new_image_file_path, new_json_file_path, new_det_txt_file_path, new_seg_txt_file_path]):
                    shutil.copy(*path_tuple)
                progress_bar.update(1)
            with ThreadPoolExecutor() as executor:
                executor.map(parallel, image_file_names)
            progress_bar.close()

if __name__ == '__main__':
    sample_files()
