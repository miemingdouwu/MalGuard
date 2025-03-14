from MalGuard.malguard.Analyzer.npm_analyzer import NPMAnalyzer
from MalGuard.malguard.Analyzer.pypi_analyzer import PyPIAnalyzer
from MalGuard.malguard.Generator.npm_generator import NPMGenerator
from MalGuard.malguard.Generator.pypi_generator import PyPIGenerator
from MalGuard.malguard.Scanners.npm_scanner import NPMSecurityScanner
from MalGuard.malguard.Scanners.pypi_scanner import PyPISecurityScanner

if __name__ == '__main__':
    # 模型配置
    api_key = ""
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    model = "qwen-max-2025-01-25"

    npm_package_path = '../detection/npm/arm-oep-99.10.9'

    npm_scanner = NPMSecurityScanner()
    npm_scan_result = npm_scanner.scan_demo(npm_package_path)

    npm_analyzer = NPMAnalyzer(api_key=api_key, base_url=base_url, model=model)
    npm_analyzer_report = npm_analyzer.llm_evaluate_demo(npm_package_path, './npm_scan_result.json')

    npm_generator = NPMGenerator(api_key=api_key, base_url=base_url, model=model)
    npm_generator_rule = npm_generator.generate_rule_demo('./npm_analyzer_report.json')

    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(npm_scan_result)
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(npm_analyzer_report)
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(npm_generator_rule)
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    pypi_package_path = '../detection/pypi/1inch-8.6'

    pypi_scanner = PyPISecurityScanner()
    pypi_scan_result = pypi_scanner.scan_demo(pypi_package_path)

    pypi_analyzer = PyPIAnalyzer(api_key=api_key, base_url=base_url, model=model)
    pypi_analyzer_report = pypi_analyzer.llm_evaluate_demo(pypi_package_path, './pypi_scan_result.json')

    pypi_generator = PyPIGenerator(api_key=api_key, base_url=base_url, model=model)
    pypi_generator_rule = pypi_generator.generate_rule_demo('./pypi_analyzer_report.json')

    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(pypi_scan_result)
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(pypi_analyzer_report)
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(pypi_generator_rule)
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")