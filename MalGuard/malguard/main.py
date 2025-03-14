from Scanners import npm_scanner
from Scanners import pypi_scanner
from Analyzer import npm_analyzer
from Analyzer import pypi_analyzer
from Generator import npm_generator
from Generator import pypi_generator

# 大模型参数
api_key = ""
base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
model = "qwen-max-2025-01-25"


if __name__ == '__main__':
    # Malguard扫描器批量扫描
    npm_scanner = npm_scanner.NPMSecurityScanner()
    pypi_scanner = pypi_scanner.PyPISecurityScanner()

    npm_scanner.scan_main("./detection/npm",
                          "./scan_results/npm")
    pypi_scanner.scan_main("./detection/pypi",
                           "./scan_results/pypi")


    # Malguard分析器批量分析
    npm_analyzer = npm_analyzer.NPMAnalyzer(api_key=api_key, base_url=base_url, model=model)
    npm_analyzer.llm_evaluate_all('./scan_results/npm',
                                  './evaluate_reports/npm')

    pypi_analyzer = pypi_analyzer.PyPIAnalyzer(api_key=api_key, base_url=base_url, model=model)
    pypi_analyzer.llm_evaluate_all('./scan_results/pypi',
                                   './evaluate_reports/pypi')


    # Malguard生成器批量分析
    npm_generator = npm_generator.NPMGenerator(api_key=api_key, base_url=base_url, model=model)
    npm_generator.generate_rules('./evaluate_reports/npm',
                                 './generate_rules/npm')

    pypi_generator = pypi_generator.PyPIGenerator(api_key=api_key, base_url=base_url, model=model)
    pypi_generator.generate_rules('./evaluate_reports/pypi',
                                  './generate_rules/pypi')










