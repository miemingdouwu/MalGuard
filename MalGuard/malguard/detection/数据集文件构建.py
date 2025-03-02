import os
import shutil
import pandas as pd


def find_dataset_folders(csv_file_path, benign_dir, malicious_dir, target_dir, folder_column_name='软件包名'):
    # 读取包含所需文件夹名称的csv文件
    df = pd.read_csv(csv_file_path)

    # 获取需要找的文件夹名列表
    folders_to_find = df[folder_column_name].tolist()

    # 遍历每个待查找的文件夹名
    for folder in folders_to_find:
        source_folder_path_1 = os.path.join(benign_dir, folder)
        source_folder_path_2 = os.path.join(malicious_dir, folder)

        if os.path.exists(source_folder_path_1):
            source_folder_path = source_folder_path_1
        elif os.path.exists(source_folder_path_2):
            source_folder_path = source_folder_path_2
        else:
            print(f"未找到: {folder}")
            continue

        target_folder_path = os.path.join(target_dir, folder)

        # 如果目标位置不存在同名文件夹，则进行复制
        if not os.path.exists(target_folder_path):
            shutil.copytree(source_folder_path, target_folder_path)
            print(f"已复制: {folder}")
        else:
            print(f"已存在: {folder}")

if __name__ == '__main__':
    # npm
    # find_dataset_folders('npm_dataset.csv', '../../dataset/benign/npm',
    #                      '../../dataset/malicious/npm', './npm')
    # pypi
    # find_dataset_folders('pypi_dataset.csv', '../../dataset/benign/pypi',
    #                      '../../dataset/malicious/pypi', './pypi')
    pass