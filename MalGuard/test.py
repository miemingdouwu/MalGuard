from guarddog import PypiPackageScanner

scanner = PypiPackageScanner()
result = scanner.scan_local('./malguard/detection/pypi/1inch-8.6')
result  = scanner.scan_remote()
print(result)



