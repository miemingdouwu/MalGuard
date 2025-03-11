from Analyzer import npm_analyzer
from Scanners import npm_scanner
from Scanners import pypi_scanner

if __name__ == '__main__':
    # # Malguard扫描器批量扫描
    # npm_scanner = npm_scanner.NPMSecurityScanner()
    # pypi_scanner = pypi_scanner.PYPISecurityScanner()
    # npm_scanner.scan_main("./detection/npm",
    #                       "./scan_results/npm")
    # pypi_scanner.scan_main("./detection/pypi",
    #                        "./scan_results/pypi")

    # Malguard分析器批量分析
    analyzer = npm_analyzer.NPMAnalyzer(api_key="",
                           base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
    analyzer.llm_evaluate_all('qwen-max-latest', './scan_results/npm/')




