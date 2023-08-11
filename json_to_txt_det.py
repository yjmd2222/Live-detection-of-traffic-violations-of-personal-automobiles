'YOLO PM detection input .txt 파일 생성'
import os
import json

def convert_to_yolo_det(bbox, image_width, image_height):
    'AI-Hub 제공 .json 파일 xywh 좌표 YOLO 형식으로 변환'
    x_min, y_min, width, height = bbox
    center_x = (x_min + width/2) / 2
    center_y = (y_min + height/2) / 2

    # 좌표를 정규화
    yolo_center_x = center_x / image_width
    yolo_center_y = center_y / image_height
    yolo_width = width / image_width
    yolo_height = height / image_height

    return yolo_center_x, yolo_center_y, yolo_width, yolo_height

def convert_to_yolo_txt_det(folder_path):
    'AI-Hub 제공 .json 파일 YOLO .txt 형식으로 변환'
    print('.json파일 .txt로 변환 시작')
    for count, filename in enumerate(os.listdir(folder_path)):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)
            
            annotations = data['annotations']['PM']
            image_width = data['description']['imageWidth']
            image_height = data['description']['imageHeight']

            yolo_bboxes = []
            for annotation in annotations:
                bbox = annotation['points'] # xywh
                yolo_bbox = convert_to_yolo_det(bbox, image_width, image_height)
                yolo_bboxes.append((annotation['PM_code'], yolo_bbox))

            # 새로운 경로 설정
            new_labels_path = os.path.join(os.path.dirname(folder_path), 'labels')
            os.makedirs(new_labels_path, exist_ok=True)
            output_file = os.path.join(new_labels_path, os.path.splitext(filename)[0] + ".txt")

            # 개별 JSON 파일에 해당하는 출력 파일 생성
            with open(output_file, 'w') as txt_file:
                for pm_code, bbox in yolo_bboxes:
                    yolo_bbox_str = ' '.join([str(val) for val in bbox])
                    txt_file.write(f"{pm_code} {yolo_bbox_str}\n")
                
                if count % 100 == 0:
                    print(f'{count}번째 파일: {output_file}')

    print('.json파일 .txt로 변환 완료')

if __name__ == '__main__':
    convert_to_yolo_txt_det('데이터/labels_json')
