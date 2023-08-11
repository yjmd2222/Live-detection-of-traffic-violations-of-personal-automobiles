import os

def restructure_aihub_data(data_root):
    '''
    AI-hub 데이터 디렉터리 구조 변경\n
    원천데이터 -> images폴더 안 name.jpg
    라벨링데이터 -> labels폴더 안 name.json
    '''
    print('디렉터리 구조 변경 시작')
    # images, labels 폴더 없으면 생성
    parent_paths = [os.path.join(data_root, parent) for parent in ['images', 'labels']]
    for parent_path in parent_paths:
        os.makedirs(parent_path, exist_ok=True)

    # 디렉터리 구조 재구성
    for count, (root, _, files) in enumerate(os.walk(data_root)):
        for file in files:
            new_parent_path = 'labels' if '.json' in file else 'images'
            os.popen(f'cp {os.path.join(root, file)} {os.path.join(data_root, new_parent_path, file)}')
            if count % 100 == 0:
                print(f'{count}번째 파일: {file}')

    print('디렉터리 구조 변경 완료')

if __name__ == '__main__':
    restructure_aihub_data('데이터')
