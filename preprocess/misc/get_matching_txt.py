'image 파일 있는 txt만 골라내기'
import os

images_base_path = 'data/generated_4ch_roboflow'
old_labels_base_path = 'data/Traffic-Violation-Detection.v3i.yolov5pytorch'
new_labels_base_path = 'data/roboflow_labels'
folders = ['train', 'val', 'test']
for folder in folders:
    path = os.path.join(images_base_path, folder)
    for file in os.listdir(path):
        file: str
        if file.endswith('.png'):
            old_file_path = os.path.join(old_labels_base_path, folder, file).replace('.png', '.txt').replace('png', 'jpg')
            new_file_path = old_file_path.replace(old_labels_base_path, new_labels_base_path).replace('jpg', 'png')
            os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
            try:
                os.replace(old_file_path, new_file_path)
            except:
                continue
