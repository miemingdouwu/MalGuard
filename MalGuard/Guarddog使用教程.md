# 命令行使用方式
------------------------------------------------------------------------------------------------------------------------
# 扫描最新版本的 “requests ”软件包
guarddog pypi scan requests
# 扫描特定版本的 “requests ”软件包
guarddog pypi scan requests --version 2.28.1
# 使用 2 种特定启发式方法扫描 “request ”软件包
guarddog pypi scan requests --rules exec-base64 --rules code-execution
# 使用所有规则扫描 “requests ”软件包，只有一条规则除外
guarddog pypi scan requests --exclude-rules exec-base64
# 扫描本地软件包存档
guarddog pypi scan /tmp/triage.tar.gz
# 扫描本地软件包目录
guarddog pypi scan /tmp/triage/
# 扫描本地文件夹的 requirements.txt 文件中引用的每个软件包
guarddog pypi verify workspace/guarddog/requirements.txt
# 扫描 requirements.txt 文件中引用的每个软件包，并输出 sarif 文件 - 仅对 verify 有效
guarddog pypi verify --output-format=sarif workspace/guarddog/requirements.txt
# 输出 JSON 到标准输出 - 对每个命令都有效
guarddog pypi scan requests --output-format=json
# 所有命令也适用于 npm 或 go
guarddog npm scan express
# 在调试模式下运行
guarddog --log-level debug npm scan express
------------------------------------------------------------------------------------------------------------------------


# guarddog文件说明
------------------------------------------------------------------------------------------------------------------------
.github文件夹：GitHub仓库配置文件
docs文件夹：Guarddog图标等资产文件，作为python库使用教程

guarddog文件夹：Guarddog源代码
 --analyzer：
   --metadata：元数据启发式规则
   --sourcecode：源代码启发式规则
 --reporters：生成 SARIF 报告，代码安全检查
 --scanners：guarddog扫描类
 --utils：guarddog工具类，配置文件
 --__init__.py：Guarddog初始化文件
 --__main__.py：Guarddog主函数
 --cli.py：Guarddog命令行工具
 --ecosystems.py：软件包生态列表文件

notebooks文件夹：GitHub仓库中的pypi包完整性验证脚本
scripts文件夹：规则变成文档说明的自动生成脚本
test文件夹：测试文件
------------------------------------------------------------------------------------------------------------------------

# guarddog pycharm 扫描本地软件包
------------------------------------------------------------------------------------------------------------------------
# 解释器：必须使用 Linux 环境

from guarddog import NPMPackageScanner
scanner = NPMPackageScanner()
result = scanner.scan_local(folder_path) # 默认全部规则
result = scanner.scan_local('path', rules={"rule1","rule2"}) # 指定规则
print(result)

# result为json格式，保存为json文件即可
------------------------------------------------------------------------------------------------------------------------

# guarddog pycharm 扫描远程软件包
------------------------------------------------------------------------------------------------------------------------
# 解释器：必须使用 Linux 环境

from guarddog import NPMPackageScanner
scanner = NPMPackageScanner()
result = scanner.scan_local(folder_path) # 默认全部规则
results = scanner.scan_remote('name', version='', rule={"rule1","rule2"})
print(result)

# result为json格式，保存为json文件即可
------------------------------------------------------------------------------------------------------------------------