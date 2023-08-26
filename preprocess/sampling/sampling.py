'샘플링 코드'
import os
import random
import shutil
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

def sample_files(old_path, new_path, images_folder_name, ir_folder_name, json_folder_name, det_folder_name, seg_folder_name):
    'data/images/train 등에 있는 파일 1/5 비율로 샘플링'
    folder_names = ['train', 'val', 'test']
    image_folder_paths = [os.path.join(old_path, 'images', folder) for folder in folder_names]

    for folder_path in image_folder_paths:
        for old_image_root, _, image_file_names in os.walk(folder_path):
            image_file_names = random.sample(image_file_names, len(image_file_names)//5)
            progress_bar = tqdm(total=len(image_file_names), desc=f'{folder_path} 샘플링')
            old_image_root: str
            old_ir_root = ir_folder_name.join(old_image_root.rsplit(images_folder_name, 1))
            old_json_root = json_folder_name.join(old_image_root.rsplit(images_folder_name, 1))
            old_det_txt_root = det_folder_name.join(old_image_root.rsplit(images_folder_name, 1))
            old_seg_txt_root = seg_folder_name.join(old_det_txt_root.rsplit(det_folder_name, 1))
            new_image_root = new_path.join(old_image_root.rsplit(old_path, 1))
            new_ir_root = ir_folder_name.join(new_image_root.rsplit(images_folder_name, 1))
            new_json_root = json_folder_name.join(new_image_root.rsplit(images_folder_name, 1))
            new_det_txt_root = det_folder_name.join(new_image_root.rsplit(images_folder_name, 1))
            new_seg_txt_root = seg_folder_name.join(new_det_txt_root.rsplit(det_folder_name, 1))
            for new_root in [new_image_root, new_ir_root, new_json_root, new_det_txt_root, new_seg_txt_root]:
                os.makedirs(new_root, exist_ok=True)
            def parallel(image_file_name: str):
                image_file_name: str
                json_file_name = image_file_name.split('.')[0] + '.json'
                txt_file_name = image_file_name.split('.')[0] + '.txt'

                old_image_file_path = os.path.join(old_image_root, image_file_name)
                old_ir_file_path = os.path.join(old_ir_root, image_file_name)
                old_json_file_path = os.path.join(old_json_root, json_file_name)
                old_det_txt_file_path = os.path.join(old_det_txt_root, txt_file_name)
                old_seg_txt_file_path = os.path.join(old_seg_txt_root, txt_file_name)
                new_image_file_path = os.path.join(new_image_root, image_file_name)
                new_ir_file_path = os.path.join(new_ir_root, image_file_name)
                new_json_file_path = os.path.join(new_json_root, json_file_name)
                new_det_txt_file_path = os.path.join(new_det_txt_root, txt_file_name)
                new_seg_txt_file_path = os.path.join(new_seg_txt_root, txt_file_name)
                zipped = zip([old_image_file_path, old_ir_file_path, old_json_file_path, old_det_txt_file_path, old_seg_txt_file_path],
                             [new_image_file_path, new_ir_file_path, new_json_file_path, new_det_txt_file_path, new_seg_txt_file_path])
                zipped = [path_tuple for path_tuple in zipped if 'None' not in path_tuple[0]]
                for path_tuple in zipped:
                    if not os.path.exists(path_tuple[1]):
                        shutil.copy(*path_tuple)
                progress_bar.update(1)
            with ThreadPoolExecutor() as executor:
                executor.map(parallel, image_file_names)
            progress_bar.close()

if __name__ == '__main__':
    sample_files(r"F:\data\images_640", r'C:/Users/jinmo/Desktop/images_640', 'images', 'ir', 'None', 'labels_det', 'labels_seg')
