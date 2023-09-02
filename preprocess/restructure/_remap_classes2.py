'진재님 올려주신 코드. RoboFlow 라벨 AI-Hub 라벨에 맞게 변경'
import os
'-_-R_20230830_105407_0906_jpg.rf.5d77f9fbd8056d32d311e87f778fada9'
def main(current_path):
    for i in ['train','test','valid']:
        directory = os.path.join(current_path,f'Traffic-Violation-Detection.v3i.yolov5pytorch/{i}/labels')

        for filename in os.listdir(directory):
            if filename.endswith(".txt"):
                file_path = os.path.join(directory, filename)
                
                with open(file_path, "r") as file:
                    content = file.read()

                new_content = ""
                for line in content.split("\n"):
                    if line.strip() != "":
                        parts = line.strip().split()
                        if parts[0] == "2":
                            parts[0] = "13" 
                        elif parts[0] == "3":
                            parts[0] = "14" 
                        elif parts[0] == "4":
                            parts[0] = "3"
                        elif parts[0] == "8":
                            parts[0] = "9"
                        
                        new_content += " ".join(parts) + "\n"

                with open(file_path, "w") as file:
                    file.write(new_content)

if __name__ == '__main__':
    main('data')
