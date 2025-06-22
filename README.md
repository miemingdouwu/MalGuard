# MalGuard

MalGuard是一个用于检测和分析恶意软件包的安全工具,主要针对NPM和PyPI包管理系统。

## 项目结构

项目主要包含以下组件:

- Scanners: 用于扫描NPM和PyPI包的安全问题
- Analyzer: 分析扫描结果
- Generator: 生成安全规则

## 主要功能

1. 扫描NPM和PyPI包的安全漏洞
2. 分析扫描结果,评估潜在威胁
3. 生成安全规则,用于未来的检测

## 使用方法

1. 克隆仓库:
git clone https://github.com/your-username/MalGuard.git

2. 安装依赖:
pip install -r requirements.txt

3. 运行主程序:
python malguard/main.py

## 配置

在`main.py`文件中,您需要配置以下参数:

- `api_key`: 用于访问大模型API的密钥
- `base_url`: API的基础URL
- `model`: 使用的模型名称

## 注意事项

- 本工具仅用于安全研究和防御目的,请勿用于非法用途。
- 使用前请确保您有权限扫描目标包。
