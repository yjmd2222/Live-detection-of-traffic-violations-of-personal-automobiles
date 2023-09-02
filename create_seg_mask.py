import numpy as np
import torch
import cv2
from PIL import Image
import os
from ultralytics import YOLO

model = YOLO(r'YOLOv8_segmentation\epochs169_batch64_size640360_count9027\runs\segment\train\weights\best.pt')

def create_seg_mask(image_paths, new_paths):
    if not image_paths:
        return
    for idx in range(len(image_paths)):
        results = model(image_paths[idx])
        print(image_paths[idx])

        for r in results:
            # im_array = r.plot()
            # im = Image.fromarray(im_array[..., ::-1])
            # im.show()
            # class * 10
            seg_image = sum(r.boxes.cls[i]*10 * r.masks.data[i] for i in range(len(r.boxes.cls)))
            if isinstance(seg_image, int):
                continue
            seg_image = seg_image.to(torch.uint8)
            seg_image = seg_image.numpy()
            image = cv2.imread(image_paths[idx])
            h, w = image.shape[:2]
            seg_image = cv2.resize(seg_image, (w,h))
            seg_image = np.expand_dims(seg_image, -1)
            merged_image = cv2.merge((image, seg_image))
            os.makedirs(os.path.dirname(new_paths[idx]), exist_ok=True)
            cv2.imwrite(new_paths[idx], merged_image)

def main(old_base_path, new_base_path):
    for old_root, _, files in os.walk(old_base_path):
        files = [os.path.join(old_root, file) for file in files if any(file.endswith(ext) for ext in ('jpg', 'jpeg', 'png'))]
        new_files = [file.replace(old_base_path, new_base_path).replace('jpg', 'png') for file in files]
        create_seg_mask(files, new_files)

if __name__ == '__main__':
    main(r'C:\Users\jinmo\Documents\GitHub\tp2\data\Traffic-Violation-Detection.v3i.yolov5pytorch', r'C:\Users\jinmo\Documents\GitHub\tp2\data\generated_4ch_roboflow')
