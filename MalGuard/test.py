import os
import json
import re

def clean_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 尝试直接解析JSON
    try:
        data = json.loads(content)
        # print(f"'{file_path}' is valid JSON.")
        return  # 如果没有异常，跳过清理步骤
    except json.JSONDecodeError:
        pass  # 如果有异常，继续执行清理代码

    # 假设杂乱字符串导致JSON解析失败，尝试移除末尾杂乱部分
    match = re.search(r'(\{.*\})', content, re.DOTALL)  # 尽量匹配有效的JSON对象
    if match:
        cleaned_content = match.group(1)
        try:
            data = json.loads(cleaned_content)
            # 如果成功解析，则重写文件
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            print(f"Cleaned up '{file_path}'.")
        except json.JSONDecodeError:
            print(f"Failed to cleanup '{file_path}', could not parse JSON even after cleanup attempt.")
    else:
        print(f"Could not find a valid JSON object in '{file_path}'.")

def traverse_and_clean(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                clean_json_file(os.path.join(root, file))

# 设置你的npm文件夹路径
npm_directory = './malguard/evaluate_reports/npm'

if __name__ == '__main__':
    traverse_and_clean(npm_directory)