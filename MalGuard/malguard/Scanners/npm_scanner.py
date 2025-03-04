import os
import json
from guarddog import NPMPackageScanner
from concurrent.futures import ProcessPoolExecutor, as_completed, TimeoutError


class NPMSecurityScanner:
    def __init__(self, max_workers=16, max_chars=100000):
        self.max_workers = max_workers
        self.max_chars = max_chars

    def check_files(self, folder_path):
        """
        检查软件包中的代码的字符数是否超过指定值
        参数：folder_path是具体一个软件包文件夹路径
        """
        # 确保提供的路径是绝对路径
        folder_path = os.path.abspath(folder_path)

        # 检查路径是否存在且是一个目录
        if not os.path.isdir(folder_path):
            return

        # 遍历文件夹中的所有文件和子文件夹
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith(('.js', '.ts')):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            char_count = len(content)
                            if char_count > self.max_chars:
                                return False
                    except:
                        pass
        return True

    def scan_one_package(self, folder_path, output_dir, index=0, total=1, timeout=False):
        """
        扫描软件包文件夹
        参数：
        folder_path是具体一个软件包文件夹路径
        output_dir是扫描结果保存路径
        index是扫描索引
        total是扫描总数
        timeout是进行超时处理一个指标
        """
        scanner = NPMPackageScanner()
        try:
            if os.path.isdir(folder_path):
                folder_name = os.path.basename(folder_path)
                output_file = os.path.join(output_dir, f"{folder_name}.json")
                if os.path.exists(output_file):
                    return

                if timeout == False:
                    print(f"Scanning: {index + 1}/{total} ｜ {folder_name}")
                    result = scanner.scan_local(folder_path)
                    with open(output_file, 'w') as f:
                        json.dump(result, f, indent=4)
                    print(f"Progress: {index + 1}/{total} ｜ {folder_name}")
                else:
                    print(f"Scanning: {index + 1}/{total} ｜ {folder_name}")
                    if self.check_files(folder_path):
                        result = scanner.scan_local(folder_path)
                        with open(output_file, 'w') as f:
                            json.dump(result, f, indent=4)
                        print(f"Progress: {index + 1}/{total} ｜ {folder_name}")
                    else:
                        result = {"issues": 0, "errors": "oversize codes", "path": folder_path}
                        with open(output_file, 'w') as f:
                            json.dump(result, f, indent=4)
                        print(f"Skipped: {index + 1}/{total} ｜ {folder_name}")

        except Exception as e:
            error_file = os.path.join(output_dir, f"{folder_name}_error.json")
            with open(error_file, 'w') as f:
                json.dump({"error": str(e)}, f, indent=4)
            print(f"Progress: {index + 1}/{total} ｜ {folder_name}")

    def scan_packages(self, root_folder, output_dir, timeout):
        """
        批量扫描软件包文件夹
        参数：
        root_folder是软件包合集文件夹路径
        output_dir是扫描结果保存路径
        timeout是进行超时处理一个指标
        """
        subdirs = [os.path.join(root_folder, d) for d in os.listdir(root_folder) if
                   os.path.isdir(os.path.join(root_folder, d))]
        total = len(subdirs)

        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self.scan_one_package, path, output_dir, i, total, timeout): path for
                       i, path in enumerate(subdirs)}
            for future in as_completed(futures):
                try:
                    future.result(timeout=300)  # 适当延长超时时间
                except TimeoutError:
                    print(f"Timeout: {futures[future]} skipped")
                    future.cancel()
                except Exception as e:
                    print(f"Error in {futures[future]}: {str(e)}")

    def scan_main(self, root_folder, output_dir, timeout=False):
        """
        调用函数
        参数：
        root_folder是软件包合集文件夹路径
        output_dir是扫描结果保存路径
        timeout是进行超时处理一个指标，默认为 False
        """
        os.makedirs(root_folder, exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)
        self.scan_packages(root_folder, output_dir, timeout)
