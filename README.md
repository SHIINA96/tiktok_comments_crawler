# TikTok Comments Crawler

[English](#english) | [中文](#中文)

## English

### Description
This is a Python-based TikTok comments crawler that uses Playwright to automatically collect comments from TikTok videos. It supports automatic scrolling to load more comments and exports the results to a CSV file.

### Requirements
- Python 3.x
- Playwright >= 1.38.0

### Installation
1. Clone this repository
2. Install the required packages:
```bash
pip install -r requirements.txt
```
3. Install Playwright browsers:
```bash
playwright install
```

### Usage
1. Put your TikTok video URL in the `url.txt` file (one URL per file)
2. Run the script:
```bash
python tiktok_comments_playwright.py
```

### Features
- Manual comment loading (scroll in Chromium browser to load all comments)
- Human verification support (when required)
- Collects user IDs and comment text
- Exports data to CSV with timestamp
- User-friendly console output

### Usage Notes
⚠️ Important: You need to manually scroll in the Chromium browser window to load all comments before the script can collect them. The automatic scrolling feature is currently not functional.

### Output
- Console display of all collected comments
- CSV file (named with timestamp) containing:
  - Index
  - User ID
  - User Profile URL
  - Comment text

### Notes
- The script runs in visible browser mode by default (can be changed by setting `HEADLESS = True`)
- Maximum scroll attempts can be adjusted via `MAX_SCROLLS` variable
- If human verification is required, the script will wait for you to complete it
- CSV files are saved with UTF-8-sig encoding for proper display in Excel

---

## 中文

### 描述
这是一个基于Python的TikTok评论爬虫，使用Playwright自动收集TikTok视频的评论。支持自动滚动加载更多评论，并将结果导出为CSV文件。

### 环境要求
- Python 3.x
- Playwright >= 1.38.0

### 安装步骤
1. 克隆此仓库
2. 安装所需包：
```bash
pip install -r requirements.txt
```
3. 安装Playwright浏览器：
```bash
playwright install
```

### 使用方法
1. 将TikTok视频URL放入`url.txt`文件中（每个文件一个URL）
2. 运行脚本：
```bash
python tiktok_comments_playwright.py
```

### 功能特点
- 手动加载评论（需在Chromium浏览器中滚动加载所有评论）
- 支持人工验证（当需要时）
- 收集用户ID和评论内容
- 导出数据为带时间戳的CSV文件
- 用户友好的控制台输出

### 使用注意事项
⚠️ 重要：在脚本收集评论之前，您需要在Chromium浏览器窗口中手动滚动加载所有评论。自动滚动功能目前不可用。

### 输出内容
- 控制台显示所有收集到的评论
- CSV文件（使用时间戳命名）包含：
  - 序号
  - 用户ID
  - 用户主页URL
  - 评论内容

### 注意事项
- 脚本默认以可视浏览器模式运行（可通过设置`HEADLESS = True`更改）
- 最大滚动次数可通过`MAX_SCROLLS`变量调整
- 如需人工验证，脚本会等待您完成验证
- CSV文件使用UTF-8-sig编码保存，以确保在Excel中正确显示