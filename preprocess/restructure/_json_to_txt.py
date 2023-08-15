'YOLO input .txt 파일 생성'
import os
import json
import re
import numpy as np

from _settings import det_aihub_to_yolo_mapper, seg_aihub_to_yolo_mapper
from _json_to_txt_det import convert_to_yolo_det
from _json_to_txt_seg import convert_to_yolo_seg

def convert_to_yolo_txt(folder_path):
    'AI-Hub 제공 .json 파일 YOLO .txt 형식으로 변환'
    print('.json파일 .txt로 변환 시작')
    for count, filename in enumerate(os.listdir(folder_path)):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)
            
            annotations_pm = data['annotations']['PM']
            annotations_env = data['annotations']['environment']

            # 3072 이미지 확인
            resolution_off = ['T007931', 'T008034', 'T008037']
            if any(i in filename for i in resolution_off):
                image_width, image_height = 3072, 1728
            else:
                image_width, image_height = 1920, 1080

            # det 정보 변환
            yolo_bboxes = []
            for annotation in annotations_pm:
                bbox = annotation['points'] # xywh
                yolo_bbox = convert_to_yolo_det(bbox, image_width, image_height)
                yolo_bboxes.append((det_aihub_to_yolo_mapper[int(annotation['PM_code'])], yolo_bbox))

            # seg 정보 변환
            yolo_polygons = []
            for annotation in annotations_env:
                polygon = annotation['points'] # x-y point들로 구성된 list
                yolo_polygon = convert_to_yolo_seg(polygon, image_width, image_height)
                yolo_polygons.append((seg_aihub_to_yolo_mapper[int(annotation['area_code'])], yolo_polygon))

            # 새로운 경로 설정
            labels_det_path = os.path.join(os.path.dirname(folder_path), 'labels_det')
            labels_seg_path = os.path.join(os.path.dirname(folder_path), 'labels_seg')
            os.makedirs(labels_det_path, exist_ok=True)
            os.makedirs(labels_seg_path, exist_ok=True)
            output_det_file = os.path.join(labels_det_path, os.path.splitext(filename)[0] + ".txt")
            output_seg_file = os.path.join(labels_seg_path, os.path.splitext(filename)[0] + ".txt")

            # det 정보 저장
            with open(output_det_file, 'w') as txt_file:
                for pm_code, bbox in yolo_bboxes:
                    yolo_bbox_str = re.sub(r'[^\d.\s]', '', str(bbox))
                    txt_file.write(f"{pm_code} {yolo_bbox_str}\n")

            # seg 정보 저장
            with open(output_seg_file, 'w') as txt_file:
                for area_code, polygons in yolo_polygons:
                    yolo_polygons_str = re.sub(r'[^\d.\s]', '', str(polygons))
                    txt_file.write(f"{area_code} {yolo_polygons_str}\n")
                
                if count % 100 == 0:
                    print(f'{count}번째 파일: {filename}')

    print('.json파일 .txt로 변환 완료')

if __name__ == '__main__':
    convert_to_yolo_txt('data/labels_json')
