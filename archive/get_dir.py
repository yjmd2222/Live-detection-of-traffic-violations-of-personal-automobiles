import os

def list_all_directories(path):
    directories = []
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            directories.append(os.path.join(root, dir))
    return directories

directory_path = 'C:\\Users\\jinmo\\Downloads\\120.개인형 이동장치 안전 데이터\\01.데이터\\2.Validation'
all_directories = list_all_directories(directory_path)

for directory in all_directories:
    print(directory)