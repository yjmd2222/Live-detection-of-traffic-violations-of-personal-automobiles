import os

def get_visible_filenames_without_extension(directory):
    filenames = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path) and not item.startswith('.') and not item.endswith('.DS_Store'):
            filename, _ = os.path.splitext(item)
            filenames.append(filename)
    return filenames

def find_different_filenames(folder1, folder2):
    filenames_folder1 = set(get_visible_filenames_without_extension(folder1))
    filenames_folder2 = set(get_visible_filenames_without_extension(folder2))

    different_filenames = filenames_folder1.symmetric_difference(filenames_folder2)
    return different_filenames

def main(folder1_path, folder2_path):

    different_filenames = find_different_filenames(folder1_path, folder2_path)
    
    if len(different_filenames) == 0:
        print("No different filenames found.")
    else:
        print("Different filenames:")
        for filename in different_filenames:
            print(filename)

if __name__ == "__main__":
    main(folder1_path = "./data/roboflow_labels/train", folder2_path = "./data/generated_4ch_roboflow/train")
