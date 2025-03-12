from openai import api_key, base_url

from Scanners import npm_scanner
from Scanners import pypi_scanner
from Analyzer import npm_analyzer
from Analyzer import pypi_analyzer

if __name__ == '__main__':
    # Malguard扫描器批量扫描
    npm_scanner = npm_scanner.NPMSecurityScanner()
    pypi_scanner = pypi_scanner.PYPISecurityScanner()

    npm_scanner.scan_main("./detection/npm",
                          "./scan_results/npm")
    pypi_scanner.scan_main("./detection/pypi",
                           "./scan_results/pypi")

    # Malguard分析器批量分析
    api_key = ""
    base_url = ""
    model = ""

    npm_analyzer = npm_analyzer.NPMAnalyzer(api_key=api_key, base_url=base_url)
    npm_analyzer.llm_evaluate_all(model, './scan_results/npm/')

    pypi_analyzer = pypi_analyzer.PyPIAnalyzer(api_key=api_key, base_url=base_url)
    pypi_analyzer.llm_evaluate_all(model, './scan_results/pypi/')




