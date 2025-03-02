import os
import tarfile

def extract_tar_gz_files(dataset_dir, output_dir):
    # 遍历dataset目录及其所有子目录
    for root, dirs, files in os.walk(dataset_dir):
        for file in files:
            if file.endswith(".tar.gz"):  # 只检查.tar.gz文件
                tar_gz_path = os.path.join(root, file)

                # 创建输出目录结构（保留原始目录结构）
                # 去除 .tar.gz 后缀来创建对应的解压目录
                base_name = os.path.splitext(os.path.splitext(file)[0])[0]
                target_dir = os.path.join(output_dir, base_name)

                # 创建目标目录（如果不存在）
                os.makedirs(target_dir, exist_ok=True)

                # 解压文件
                try:
                    with tarfile.open(tar_gz_path, "r:gz") as tar:
                        tar.extractall(path=target_dir)
                    print(f"解压完成: {tar_gz_path} -> {target_dir}")
                except Exception as e:
                    print(f"解压失败: {tar_gz_path} - {str(e)}")


if __name__ == "__main__":
    # 设置路径 BKC数据集
    dataset_dir = "./Backstabbers-Knife-Collection/samples/pypi"
    new_dataset_dir = "./dataset/malicious/pypi"

    # 确保输出目录存在
    os.makedirs(new_dataset_dir, exist_ok=True)

    # 执行解压操作
    extract_tar_gz_files(dataset_dir, new_dataset_dir)