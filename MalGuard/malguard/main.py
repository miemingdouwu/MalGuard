from Scanners import npm_scanner
from Scanners import pypi_scanner

if __name__ == '__main__':
    # Guarddog批量扫描
    npm_scanner = npm_scanner.NPMSecurityScanner()
    pypi_scanner = pypi_scanner.PYPISecurityScanner()
    npm_scanner.scan_main("./detection/npm", "./scan_results")
    pypi_scanner.scan_main("./detection/pypi", "./pypi_results")