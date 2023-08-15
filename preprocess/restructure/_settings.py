'class label 0부터 세는 매핑 정보'

seg_labels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
seg_aihub_to_yolo_mapper = {seg_labels[idx]: idx for idx in range(len(seg_labels))}
seg_yolo_to_aihub_mapper = {v: k for k,v in seg_aihub_to_yolo_mapper.items()}

det_labels = [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
            # !!!34 없음!!!
              35, 36]
det_aihub_to_yolo_mapper = {det_labels[idx]: idx for idx in range(len(det_labels))}
det_yolo_to_aihub_mapper = {v: k for k,v in det_aihub_to_yolo_mapper.items()}
