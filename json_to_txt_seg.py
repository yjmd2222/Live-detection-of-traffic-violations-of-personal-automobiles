'YOLO polygon points input .txt 파일 생성'
import os
import json
import re

def convert_to_yolo_seg(polygon, image_width, image_height):
    '''
    AI-Hub 제공 .json 파일 y-x 좌표 YOLO 형식으로 변환\n
    주의: y-x 순서
    '''
    # width, height으로 나누어 0-1 사이로 정규화
    polygon = list(map((lambda point: [point[0]/image_height, point[1]/image_width]),polygon))

    return polygon

def convert_to_yolo_txt_seg(folder_path):
    'AI-Hub 제공 .json 파일 YOLO segmentation .txt 형식으로 변환'
    # 해당하는 jpg 파일 있는지 확인하는 절차 아직 도입 안 함
    print('.json파일 .txt로 변환 시작')
    for count, filename in enumerate(os.listdir(folder_path)):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)
            
            annotations = data['annotations']['environment']
            image_width = data['description']['imageWidth']
            image_height = data['description']['imageHeight']

            yolo_polygons = []
            for annotation in annotations:
                polygon = annotation['points'] # x-y point들로 구성된 list
                yolo_polygon = convert_to_yolo_seg(polygon, image_width, image_height)
                yolo_polygons.append((annotation['area_code'], yolo_polygon))

            # 새로운 경로 설정
            new_labels_path = os.path.join(os.path.dirname(folder_path), 'labels_seg')
            os.makedirs(new_labels_path, exist_ok=True)
            output_file = os.path.join(new_labels_path, os.path.splitext(filename)[0] + ".txt")

            # 개별 JSON 파일에 해당하는 출력 파일 생성
            with open(output_file, 'w') as txt_file:
                for area_code, polygons in yolo_polygons:
                    yolo_polygons_str = re.sub(r'[^\d.\s]', '', str(polygons))
                    txt_file.write(f"{area_code} {yolo_polygons_str}\n")
                
                if count % 100 == 0:
                    print(f'{count}번째 파일: {output_file}')

    print('.json파일 .txt로 변환 완료')

if __name__ == '__main__':
    convert_to_yolo_txt_seg('데이터/labels_json')
