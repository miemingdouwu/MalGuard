import os
import json
import csv

def find_issues(directory_path, output_csv):
    # 初始化一个列表来存储有issue的文件名
    issue_files = []

    # 遍历目录中的所有文件
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if data.get('issues', 0) == 0:
                        issue_files.append(file.split('.')[0])
                        print(file.split('.')[0])

    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['软件包名'])
        for filename in issue_files:
            writer.writerow([filename])

    print(f"Files with issues have been recorded in {output_csv}\n")


if __name__ == '__main__':
    # npm
    directory_path_npm = './npm'
    output_csv_npm = 'issue_files_npm.csv'
    find_issues(directory_path_npm, output_csv_npm)
    # pypi
    directory_path_pypi = './pypi'
    output_csv_pypi = 'issue_files_pypi.csv'
    find_issues(directory_path_pypi, output_csv_pypi)

