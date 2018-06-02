import os

def get_all_file_in_folder(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".jpg") or file.endswith(".png"):
                print(os.path.join(root, file).replace('\\', '/')+','+ root.split('\\')[-1])

def get_all_file_in_folder_more_than(path, num=4):
    for root, dirs, files in os.walk(path):
        if len(files) < num:
            continue
        for file in files:
            if file.endswith(".jpg") or file.endswith(".png"):
                print(os.path.join(root, file).replace('\\', '/')+','+ root.split('/')[-1])

if __name__ == '__main__':
    get_all_file_in_folder_morethan("image/lfw_onlya")
