import os
import json
import csv
import random


def dataset_construct(directory_path, num1, num2, tag1, tag2):
    # 初始化列表来存储有issue的文件名
    issue_files_zero = []
    issue_files_nonzero = []

    # 遍历目录中的所有文件
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    issues = data.get('issues', 0)
                    base_name = file.rsplit('.', 1)[0]
                    if issues > 0:
                        issue_files_nonzero.append((base_name, tag1))
                    elif issues == 0:
                        issue_files_zero.append((base_name, tag2))

    selected_zero = random.sample(issue_files_zero, num2) if len(issue_files_zero) >= num2 else issue_files_zero
    selected_nonzero = random.sample(issue_files_nonzero, num1) if len(issue_files_nonzero) >= num1 else issue_files_nonzero
    selected = selected_zero + selected_nonzero

    return selected


def write_to_csv(filename, items):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['软件包名', '标签'])
        for i, label in items:
            writer.writerow([i, label])

    print(f"{filename}构建成功！")


if __name__ == '__main__':
    # # npm数据集
    # npm_res1 = dataset_construct('../../scan_results_benign/npm', 5, 295, '可疑良性包', '确认良性包')
    # npm_res2 = dataset_construct('../../scan_results_malicious/npm', 90, 10, '确认恶意包', '可疑恶意包')
    # write_to_csv('npm_dataset.csv', npm_res1 + npm_res2)
    #
    # # pypi数据集
    # pypi_res1 = dataset_construct('../../scan_results_benign/pypi', 15, 285, '可疑良性包', '确认良性包')
    # pypi_res2 = dataset_construct('../../scan_results_malicious/pypi', 75, 25, '确认恶意包', '可疑恶意包')
    # write_to_csv('pypi_dataset.csv', pypi_res1 + pypi_res2)
    pass
