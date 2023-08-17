'''
진재님 이미지 사이즈 1920 -> 640 축소 스크립트 수정\n
data/images_pre에 축소한 이미지 저장
'''
import os
from tqdm import tqdm
import cv2
from concurrent import futures

current_path = os.path.abspath('.') # Team Project home directory / ex. Team Project2
# 원본 이미지 폴더 제외하고 resize 이미지 저장을 위한 새로운 폴더 생성(data_pre/images)
directory_name = {'data' : ['images_pre']}
# data 폴더 / images, labels 하위 폴더 생성
for folder, subfolders in directory_name.items():
    data_folder_path = os.path.join(current_path,folder)
    os.makedirs(data_folder_path, exist_ok=True)
    
    for subfolder in subfolders:
        subfolder_path = os.path.join(os.path.abspath('.'),folder, subfolder)
        os.makedirs(subfolder_path, exist_ok=True)
        # images 폴더 내 train/test/val 폴더 생성
        for subsubfolder in ['train','test','val']:
            subsubfolder_path = os.path.join(subfolder_path,subsubfolder)
            os.makedirs(subsubfolder_path, exist_ok=True)


# 원본 이미지 resize(1920x1080 → 640x640)하여 저장
def resize(folder_path, file, keep_aspect=True):
    '파일 열고 이미지 사이즈 조정 후 저장'
    image = cv2.imread(os.path.join(folder_path,file))
    if keep_aspect:
        h, w = image.shape[:2] # h,w
        nw = 640
        nh = int(nw / w * h)
        image = cv2.resize(image, (nw,nh)) # w,h
    else:
        image = cv2.resize(image, (640,640))
    
    # 주의. Team Project2(프로젝트 홈 디렉토리)에 data_pre, images, train/test/val 폴더 존재하지 않으면 이미지 저장안됨.
    save_path = os.path.join(current_path, 'data', 'images_pre', folder, file)
    cv2.imwrite(save_path, image)
    progress_bar.update(1)

for folder in ['train','test','val']:
    # # 주의. Team Project2(프로젝트 홈 디렉토리)에 data 폴더, images 폴더, train, test,val 폴더 및 내부 이미지 데이터 존재해야함.
    folder_path = os.path.join(current_path,'data','images_raw',folder) # ./Team Project2/data/images/ 폴더에 존재하는 train/test/val 각각의 path 접근
    file_list = os.listdir(os.path.join(current_path,'data','images_raw',folder)) # ↑ 각 폴더 내 이미지 파일 리스트화
    # tqdm 라이브러리 사용하여 진행상황 확인.
    progress_bar = tqdm(total=len(file_list), desc= f'{folder} : Data preprocessing is in progress')
    # 병렬
    with futures.ThreadPoolExecutor() as executor:
        executor.map(lambda file: resize(folder_path, file), file_list)
    progress_bar.close()
