import os
import json
from guarddog import NPMPackageScanner
from concurrent.futures import ProcessPoolExecutor, as_completed, TimeoutError


def check_files(folder_path, max_chars=50000):
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
                        if char_count > max_chars:
                            return False
                except:
                    pass
    return True


def scan_and_save_package(folder_path, output_dir, index, total):
    scanner = NPMPackageScanner()
    try:
        if os.path.isdir(folder_path):
            folder_name = os.path.basename(folder_path)
            output_file = os.path.join(output_dir, f"{folder_name}.json")
            if os.path.exists(output_file):
                # print(f"Exist: {index + 1}/{total}")
                return
            print(f"Scanning: {index + 1}/{total} ｜ {folder_name}")

            result = scanner.scan_local(folder_path)
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=4)
            print(f"Progress: {index + 1}/{total} ｜ {folder_name}")

            # if check_files(folder_path):
            #     result = Scanners.scan_local(folder_path)
            #     with open(output_file, 'w') as f:
            #         json.dump(result, f, indent=4)
            #     print(f"Progress: {index + 1}/{total} ｜ {folder_name}")
            # else:
            #     result = {"issues": 0, "errors": "oversize codes", "path": folder_path}
            #     with open(output_file, 'w') as f:
            #         json.dump(result, f, indent=4)
            #     print(f"Skipped: {index + 1}/{total} ｜ {folder_name}")

    except Exception as e:
        error_file = os.path.join(output_dir, f"{folder_name}_error.json")
        with open(error_file, 'w') as f:
            json.dump({"error": str(e)}, f, indent=4)
        print(f"Progress: {index + 1}/{total} ｜ {folder_name}")


def scan_packages(root_folder, output_dir, max_workers=16):
    subdirs = [os.path.join(root_folder, d) for d in os.listdir(root_folder) if os.path.isdir(os.path.join(root_folder, d))]
    total = len(subdirs)

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(scan_and_save_package, path, output_dir, i, total): path for i, path in enumerate(subdirs)}
        for future in as_completed(futures):
            try:
                future.result(timeout=300)  # 适当延长超时时间
            except TimeoutError:
                print(f"Timeout: {futures[future]} skipped")
                future.cancel()
            except Exception as e:
                print(f"Error in {futures[future]}: {str(e)}")

def scan_malicious():
    root_folder = './dataset/malicious/npm'
    output_dir = './scan_results_malicious/npm'
    os.makedirs(output_dir, exist_ok=True)
    scan_packages(root_folder, output_dir)


def scan_benign():
    root_folder = './dataset/benign/npm'
    output_dir = './scan_results_benign/npm'
    os.makedirs(output_dir, exist_ok=True)
    scan_packages(root_folder, output_dir)


if __name__ == "__main__":
    # scan_malicious()
    # scan_benign()
    pass




