

import os

def get_all_file_in_folder(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".jpg") or file.endswith(".png"):
                print(os.path.join(root, file).replace('\\', '/')+','+ root.split('\\')[-1])

# def delete_csv_file_in_folder(path):
#     for root, dirs, files in os.walk(path):
#         for file in files:
#             if file.endswith(".csv"):
#                 os.remove(os.path.join(root, file).replace('\\', '/'))

if __name__ == '__main__':
    get_all_file_in_folder("image")
    #delete_csv_file_in_folder('ghega-dataset\\')