import csv
import json
import os
import logging
import time
from multiprocessing import Pool
from functools import partial
from openai import OpenAI

# 文件当前路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 上一级目录
parent_dir = os.path.dirname(current_dir)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)


def process_single_report(report_path, output_dir, api_key, base_url, model):
    try:
        generator = NPMGenerator(api_key, base_url, model)
        generator.generate_rule(report_path, output_dir)
        logging.info(f"规则生成成功: {report_path}")
    except Exception as e:
        logging.error(f"处理失败: {report_path} - 错误: {str(e)}")


class NPMGenerator:
    def __init__(self, api_key, base_url, model):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model

    def llm_conversation(self, system_prompt, user_prompt):
        client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
        time.sleep(2)
        evaluate_completion = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        return evaluate_completion.choices[0].message.content

    def generate_rule(self, evaluate_report_path, generator_rules_folder_path):
        if not evaluate_report_path.endswith('.json'):
            return
        filename = os.path.splitext(os.path.basename(evaluate_report_path))[0]
        rule_path = os.path.join(generator_rules_folder_path, f"{filename}.yml")

        if os.path.exists(rule_path):
            return

        prompt_path = os.path.join(current_dir, 'npm_rules_prompt.json')
        with open(prompt_path, 'r') as f:
            prompt = json.load(f)['prompt']

        with open(evaluate_report_path, 'r') as f:
            evaluate_report = json.load(f)

        system_prompt = str(prompt)
        user_prompt = str(json.dumps(evaluate_report))

        rule = self.llm_conversation(system_prompt, user_prompt)

        if rule.startswith('```yml'):
            rule = rule[len('```yml'):]
        if rule.startswith('```yaml'):
            rule = rule[len('```yaml'):]
        if rule.endswith('```'):
            rule = rule[:-len('```')]

        os.makedirs(generator_rules_folder_path, exist_ok=True)

        with open(rule_path, 'w', encoding='utf-8') as f:
            f.write(rule)

    def generate_rules(self, evaluate_report_folder_path, generator_rules_folder_path):
        csv_path = os.path.join(evaluate_report_folder_path, '../npm_no_issues_list.csv')
        if not os.path.exists(csv_path):
            return

        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            package_names = [row[0] for row in reader if row]

        existing_report_paths = []
        for name in package_names:
            report_path = os.path.join(evaluate_report_folder_path, f"{name}.json")
            if os.path.exists(report_path):
                with open(report_path, 'r') as f:
                    data = json.load(f)
                    if data['threat_assessment']['malware_score'] >= 0.5:
                        existing_report_paths.append(report_path)

        if not existing_report_paths:
            logging.info("No reports to process.")
            return

        logging.info(f"Starting processing {len(existing_report_paths)} reports.")

        with Pool(processes=5) as pool:
            process_func = partial(
                process_single_report,
                output_dir=generator_rules_folder_path,
                api_key=self.api_key,
                base_url=self.base_url,
                model=self.model
            )
            pool.map(process_func, existing_report_paths)

        logging.info("All reports processed.")

    def generate_rule_demo(self, evaluate_report_path):
        """
        evaluate_report:
        """
        # 判断文件是否以.json结尾
        if not evaluate_report_path.endswith('.json'):
            return

        # 获取prompt
        prompt_path = os.path.join(current_dir, 'npm_rules_prompt' + '.json')

        with open(prompt_path, 'r') as f:
            prompt = str(json.load(f)['prompt'])

        with open(evaluate_report_path, 'r') as f:
            evaluate_report = str(json.load(f))

        system_prompt = prompt
        user_prompt = evaluate_report
        rule = self.llm_conversation(system_prompt, user_prompt)

        if rule.startswith('```yml'):
            rule = rule[len('```yml'):]
        if rule.startswith('```yaml'):
            rule = rule[len('```yaml'):]
        if rule.endswith('```'):
            rule = rule[:-len('```')]

        rule_path = './npm_generator_rule.yml'

        with open(rule_path, 'w', encoding='utf-8') as f:
            f.write(rule)

        return rule
