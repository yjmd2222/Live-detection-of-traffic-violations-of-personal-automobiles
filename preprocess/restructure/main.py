'''
원천데이터 -> images\n
라벨링데이터 -> labels_json\n\n
YOLO 형식으로 변환\n\n
train, val, test로 split
'''
from _restructure_aihub_data import restructure_aihub_data
from _json_to_txt import convert_to_yolo_txt
from _train_val_test_split import train_val_test_split

if __name__ == '__main__':
    restructure_aihub_data('data')
    convert_to_yolo_txt('data/labels_json')
    train_val_test_split()
