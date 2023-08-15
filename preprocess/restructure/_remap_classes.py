'json_to_txt_*.py 파일 수정 전 이미 변환한 .txt 파일에서 class label 다시 매핑'
import os

from _settings import det_aihub_to_yolo_mapper, seg_aihub_to_yolo_mapper

def remap_classes_aihub_to_yolo(path, mapper):
    'mapper로 label 변환'
    sub_paths = [os.path.join(path, sub_path) for sub_path in os.listdir(path)]
    for sub_path in sub_paths:
        for count, filename in enumerate(os.listdir(sub_path)):
            if count % 100 == 0:
                print(f'{count}번째 파일: {filename}')
            file_path = os.path.join(sub_path, filename)
            with open(file_path, 'r') as txt_file:
                contents = txt_file.readlines()
                new_contents = []
                for line in contents:
                    class_, numbers = line.split(' ', maxsplit=1)
                    new_class_ = str(mapper[int(class_)])
                    new_contents.append(f'{new_class_} {numbers}')
            with open(file_path, 'w') as txt_file:
                txt_file.writelines(new_contents)

def remap_classes_aihub_to_yolo_save(det_path, seg_path):
    '.txt 파일 다시 저장'
    # det
    for path, mapper in zip([det_path, seg_path], [det_aihub_to_yolo_mapper, seg_aihub_to_yolo_mapper]):
        if path == det_path: continue
        remap_classes_aihub_to_yolo(path, mapper)

if __name__ == '__main__':
    remap_classes_aihub_to_yolo_save('data/labels', 'data/labels_seg')
