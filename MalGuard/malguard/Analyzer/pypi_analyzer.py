import csv
import json
import os
import logging
import multiprocessing
from functools import partial
from openai import OpenAI

# 文件当前路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 上一级目录
parent_dir = os.path.dirname(current_dir)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(processName)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger()


def init_worker():
    """子进程日志初始化"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(processName)s - %(levelname)s - %(message)s',
    )


def process_single_file(file_path, output_dir, api_key, base_url, model):
    """处理单个文件的包装函数"""
    local_logger = logging.getLogger()
    local_logger.info(f"开始处理文件: {file_path}")
    try:
        analyzer = PyPIAnalyzer(api_key, base_url, model)
        result = analyzer.llm_evaluate(file_path, output_dir)
        if result:
            tag, filename = result
            local_logger.info(f"文件 {file_path} 处理完成")
            return (tag, filename)
        return None
    except Exception as e:
        local_logger.error(f"处理文件 {file_path} 失败: {str(e)}", exc_info=True)
        return None


class PyPIAnalyzer:
    def __init__(self, api_key, base_url, model):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model

    def llm_conversation(self, system_prompt, user_prompt):
        """
        system_prompt：系统提示词
        user_prompt：用户提示词
        return：返回对话结果
        """
        # 生成评估报告
        client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )

        evaluate_completion = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )

        evaluate_report = evaluate_completion.choices[0].message.content

        return evaluate_report

    def read_scan_result(self, scan_result_path):
        """
        scan_result_path：扫描结果文件路径
        return：包名，扫描结果
        """
        scan_result = {}
        if not scan_result_path.endswith('.json'):
            return

        # 获取文件名（不含路径）
        filename = os.path.basename(scan_result_path)
        # 获取文件名（不含扩展名）
        filename = os.path.splitext(filename)[0]

        try:
            with open(scan_result_path, 'r', encoding='utf-8') as file:
                # 将json文件内容加载到字典中
                scan_result = json.load(file)
                return filename, scan_result
        except:
            return

    def analyze_scan_result(self, scan_result_path):
        """
        scan_result_path：扫描结果文件路径
        return：包名，扫描结果，脚本文件，其他文件
        """
        filename, scan_result = self.read_scan_result(scan_result_path)

        if scan_result["issues"] == 0:
            package_path = os.path.join(parent_dir, 'detection/pypi', str(filename))

            # 用于存储所有Python文件内容的字典，键为文件名，值为文件内容字符串
            setup_py_content = {}
            others_content = {}

            # 遍历目录及其子目录
            for root, dirs, files in os.walk(package_path):
                for file in files:
                    if file == 'setup.py':
                        file_path = os.path.join(root, file)
                        try:
                            # 读取文件内容并存储为字符串
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                setup_py_content[file] = str(content)
                        except:
                            continue
                    elif file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        try:
                            # 读取文件内容并存储为字符串
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                others_content[file] = str(content)
                        except:
                            continue
                    else:
                        continue

            return filename, scan_result, setup_py_content, others_content

        else:
            return filename, scan_result, None, None

    def llm_evaluate(self, scan_result_path, output_dir):
        """
        model：使用模型
        scan_result_path：扫描结果文件路径
        return：标签，包名
        """

        tag = None

        filename, scan_result, setup_py_content, others_content = self.analyze_scan_result(scan_result_path)

        system_prompt = ""

        prompt_path = os.path.join(current_dir, 'pypi_prompt.json')
        with open(prompt_path, 'r', encoding='utf-8') as f:
            system_prompt = str(json.load(f)['prompt'])

        user_prompt = ""
        if setup_py_content is not None:
            user_prompt = str(setup_py_content)
            tag = 1
        elif others_content is not None:
            user_prompt = str(others_content)
            tag = 1
        else:
            temp_dict = {}
            temp_dict['guarddog_scan_result'] = str(scan_result)
            user_prompt = str(temp_dict)
            tag = 2

        # print("___________________________________________________________________________________________")
        # print(system_prompt)
        # print("___________________________________________________________________________________________")
        # print(user_prompt)
        # print("___________________________________________________________________________________________")

        report_path = os.path.join(output_dir, str(filename) + '.json')

        if os.path.exists(report_path):
            return tag, filename

        if len(user_prompt) > 20000:
            user_prompt = user_prompt[:20000] + '"' + '}'

        report = self.llm_conversation(system_prompt, user_prompt)

        if report.startswith('```json'):
            report = report[len('```json'):]
        if report.endswith('```'):
            report = report[:-len('```')]

        # print("___________________________________________________________________________________________")
        # print(report)
        # print("___________________________________________________________________________________________")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)

        return tag, filename

    # def llm_evaluate_all(self, model, scan_result_folder_path):
    #     """
    #     model：使用模型
    #     scan_result_path：所以扫描结果文件夹的路径
    #     """
    #     no_issues_list = []
    #     has_issues_list = []
    #
    #     for root, dirs, files in os.walk(scan_result_folder_path):
    #         for file in files:
    #             if file.endswith('.json'):
    #                 file_path = os.path.join(root, file)
    #                 tag, filename = self.llm_evaluate(model, file_path)
    #
    #                 match tag:
    #                     case 1:
    #                         no_issues_list.append(filename)
    #                     case 2:
    #                         has_issues_list.append(filename)
    #
    #     with open('../evaluate_reports/pypi_no_issues_list', 'w', encoding='utf-8') as file:
    #     # 写入到csv文件，每个元素占一行
    #         writer = csv.writer(file)
    #         # 遍历列表并将每个元素作为一行写入
    #         for item in no_issues_list:
    #             writer.writerow([item])
    #
    #     with open('../evaluate_reports/pypi_has_issues_list', 'w', encoding='utf-8') as file:
    #     # 写入到csv文件，每个元素占一行
    #         writer = csv.writer(file)
    #         # 遍历列表并将每个元素作为一行写入
    #         for item in has_issues_list:
    #             writer.writerow([item])

    def llm_evaluate_all(self, scan_result_folder_path, evaluate_report_folder_path):
        """多进程处理所有扫描结果"""
        logger.info(f"开始扫描目录: {scan_result_folder_path}")

        # 收集所有JSON文件路径
        file_paths = []
        for root, _, files in os.walk(scan_result_folder_path):
            for file in files:
                if file.endswith('.json'):
                    file_paths.append(os.path.join(root, file))
        logger.info(f"共发现 {len(file_paths)} 个待处理文件")

        # 创建进程池
        pool = multiprocessing.Pool(
            processes=multiprocessing.cpu_count(),
            initializer=init_worker
        )

        # 使用partial固定参数
        process_func = partial(
            process_single_file,
            output_dir=evaluate_report_folder_path,
            model=self.model,
            api_key=self.api_key,
            base_url=self.base_url
        )

        # 进度跟踪
        results = []
        try:
            for i, result in enumerate(pool.imap_unordered(process_func, file_paths), 1):
                if result:
                    results.append(result)
                logger.info(f"处理进度: {i}/{len(file_paths)} ({(i / len(file_paths)) * 100:.1f}%)")
        except Exception as e:
            logger.error(f"处理过程中发生严重错误: {str(e)}", exc_info=True)
        finally:
            pool.close()
            pool.join()

        # 分类结果
        no_issues_list = []
        has_issues_list = []
        for tag, filename in results:
            if tag == 1:
                no_issues_list.append(filename)
            elif tag == 2:
                has_issues_list.append(filename)

        # 写入结果文件
        pypi_no_issues_list_path = os.path.join(evaluate_report_folder_path, '../pypi_no_issues_list.csv')
        with open(pypi_no_issues_list_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows([[name] for name in no_issues_list])

        pypi_has_issues_list_path = os.path.join(evaluate_report_folder_path, '../pypi_has_issues_list.csv')
        with open(pypi_has_issues_list_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows([[name] for name in has_issues_list])

        logger.info(f"处理完成！零事件包: {len(no_issues_list)} 个，风险包: {len(has_issues_list)} 个")
        return no_issues_list, has_issues_list

    def llm_evaluate_demo(self, package_path, scan_result_path):
        """
        scan_result_path：扫描结果文件路径
        return：标签，包名
        """

        with open(scan_result_path, 'r', encoding='utf-8') as file:
            # 将json文件内容加载到字典中
            scan_result = json.load(file)


        # 用于存储所有Python文件内容的字典，键为文件名，值为文件内容字符串
        setup_py_content = {}
        others_content = {}

        if scan_result["issues"] == 0:
            for root, dirs, files in os.walk(package_path):
                for file in files:
                    if file == 'setup.py':
                        file_path = os.path.join(root, file)
                        try:
                            # 读取文件内容并存储为字符串
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                setup_py_content[file] = str(content)
                        except:
                            continue
                    elif file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        try:
                            # 读取文件内容并存储为字符串
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                others_content[file] = str(content)
                        except:
                            continue
                    else:
                        continue

        system_prompt = ""
        user_prompt = ""

        prompt_path = os.path.join(current_dir, 'pypi_prompt.json')
        with open(prompt_path, 'r', encoding='utf-8') as f:
            system_prompt = str(json.load(f)['prompt'])

        if setup_py_content:
            user_prompt = str(setup_py_content)
        elif others_content:
            user_prompt = str(others_content)
        else:
            temp_dict = {}
            temp_dict['guarddog_scan_result'] = str(scan_result)
            user_prompt = str(temp_dict)

        if len(user_prompt) > 20000:
            user_prompt = user_prompt[:20000] + '"' + '}'

        report = self.llm_conversation(system_prompt, user_prompt)

        if report.startswith('```json'):
            report = report[len('```json'):]
        if report.endswith('```'):
            report = report[:-len('```')]

        report_path = './pypi_analyzer_report.json'

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)

        return report
