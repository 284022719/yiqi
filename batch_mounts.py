from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse
import time
import pickle
import logging
import os
from datetime import datetime

# 设置日志记录
def setup_logging():
    """设置日志记录"""
    # 创建logs文件夹（如果不存在）
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # 生成日志文件名（包含时间戳）
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_filename = f'logs/mounts_crawler_{timestamp}.log'
    
    # 配置日志格式
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler()  # 同时输出到控制台
        ]
    )
    
    return log_filename

# 角色名列表
role_names = [
    "久世", "快来骑我吧", "风少爷丶", "白鯨", "狮萨", "雪蒂凯", "月影佑汐", "道别哀歌",
    "Mengsk", "小米大麦粥", "Playerwqhvlt", "华师傅", "月影之力", "圣光拯救",
    "轴种", "陈皮", "丶王祖贤", "夢隊長", "小叨", "妙不可言", "Pro"
]

# 启动日志记录
log_filename = setup_logging()
logging.info("=" * 60)
logging.info("魔兽世界坐骑数量批量爬取系统启动")
logging.info("=" * 60)

# 启动浏览器并加载 Cookie
logging.info("正在启动浏览器...")
try:
    driver = webdriver.Chrome()
    logging.info("浏览器启动成功")
except Exception as e:
    logging.error(f"浏览器启动失败: {e}")
    exit(1)

try:
    driver.get("https://wow.blizzard.cn/")  # 先访问主域名
    logging.info("成功访问魔兽世界官网")
except Exception as e:
    logging.error(f"访问官网失败: {e}")
    driver.quit()
    exit(1)

# 加载 Cookie
logging.info("正在加载Cookie...")
try:
    with open("cookies.pkl", "rb") as f:
        cookies = pickle.load(f)
        for cookie in cookies:
            if 'sameSite' in cookie:
                del cookie['sameSite']
            driver.add_cookie(cookie)
    logging.info(f"成功加载 {len(cookies)} 个Cookie")
except Exception as e:
    logging.error(f"加载Cookie失败: {e}")
    driver.quit()
    exit(1)

# 存储结果
results = []
server = "arthas"

logging.info(f"开始批量爬取 {len(role_names)} 个角色的坐骑数量...")
logging.info("=" * 50)

for i, name in enumerate(role_names, 1):
    logging.info(f"[{i}/{len(role_names)}] 正在处理：{name}")
    
    try:
        # 直接访问角色页面
        role_url = f"https://wow.blizzard.cn/character/#/{server}/{urllib.parse.quote(name)}/"
        logging.info(f"访问角色页面: {role_url}")
        driver.get(role_url)
        time.sleep(5)  # 等待页面加载
        
        # 检查是否成功跳转到角色详情页
        current_url = driver.current_url
        logging.info(f"当前页面URL: {current_url}")
        if "search" in current_url:
            logging.warning(f"页面仍在搜索页面，尝试直接访问...")
            # 直接访问角色页面
            role_url = f"https://wow.blizzard.cn/character/#/{server}/{urllib.parse.quote(name)}/"
            driver.get(role_url)
            time.sleep(5)
        
        # 点击"收藏"标签
        try:
            # 方法1：使用XPATH
            collect_tab = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/div[1]/div[3]/a[3]")
            collect_tab.click()
            logging.info("已点击收藏标签（方法1）")
        except Exception as e:
            try:
                # 方法2：查找包含"收藏"的链接
                collect_tab = driver.find_element(By.XPATH, "//a[contains(text(),'收藏')]")
                collect_tab.click()
                logging.info("已点击收藏标签（方法2）")
            except Exception as e2:
                try:
                    # 方法3：查找包含"收藏"的span
                    collect_tab = driver.find_element(By.XPATH, "//span[contains(text(),'收藏')]")
                    collect_tab.click()
                    logging.info("已点击收藏标签（方法3）")
                except Exception as e3:
                    logging.error(f"无法找到收藏标签: 方法1错误={e}, 方法2错误={e2}, 方法3错误={e3}")
                    raise e3
        
        time.sleep(2)
        
        # 点击"坐骑"子标签
        try:
            # 方法1：使用XPATH
            mount_tab = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/div[2]/div[1]/div/a[2]")
            mount_tab.click()
            logging.info("已点击坐骑标签（方法1）")
        except Exception as e:
            try:
                # 方法2：查找包含"坐骑"的链接
                mount_tab = driver.find_element(By.XPATH, "//a[contains(text(),'坐骑')]")
                mount_tab.click()
                logging.info("已点击坐骑标签（方法2）")
            except Exception as e2:
                try:
                    # 方法3：查找包含"坐骑"的span
                    mount_tab = driver.find_element(By.XPATH, "//span[contains(text(),'坐骑')]")
                    mount_tab.click()
                    logging.info("已点击坐骑标签（方法3）")
                except Exception as e3:
                    logging.error(f"无法找到坐骑标签: 方法1错误={e}, 方法2错误={e2}, 方法3错误={e3}")
                    raise e3
        
        time.sleep(2)
        
        # 获取坐骑数量
        mount_count = "未知"
        try:
            # 方法1：直接查找包含"坐骑"和"个不同的坐骑"的文本
            mount_count_elem = driver.find_element(By.XPATH, "//*[contains(text(),'坐骑') and contains(text(),'个不同的坐骑')]")
            mount_count = mount_count_elem.text
            logging.info(f"坐骑数量：{mount_count}")
        except Exception as e:
            try:
                # 方法2：查找包含数字和"个不同的坐骑"的文本
                mount_count_elem = driver.find_element(By.XPATH, "//*[contains(text(),'个不同的坐骑')]")
                mount_count = mount_count_elem.text
                logging.info(f"坐骑数量：{mount_count}")
            except Exception as e2:
                try:
                    # 方法3：查找包含"坐骑"的文本，然后提取数字
                    mount_elements = driver.find_elements(By.XPATH, "//*[contains(text(),'坐骑')]")
                    for elem in mount_elements:
                        text = elem.text
                        if '个不同的坐骑' in text:
                            mount_count = text
                            logging.info(f"坐骑数量：{mount_count}")
                            break
                except Exception as e3:
                    logging.error(f"无法获取坐骑数量: 方法1错误={e}, 方法2错误={e2}, 方法3错误={e3}")
        
        # 保存结果
        results.append({
            "角色名": name,
            "坐骑数量": mount_count,
            "状态": "成功" if mount_count != "未知" else "失败"
        })
        
        logging.info(f"角色 {name} 处理完成，状态：{'成功' if mount_count != '未知' else '失败'}")
        
    except Exception as e:
        logging.error(f"处理角色 {name} 失败：{e}")
        results.append({
            "角色名": name,
            "坐骑数量": "未知",
            "状态": "失败"
        })
    
    logging.info("-" * 30)

# 关闭浏览器
logging.info("正在关闭浏览器...")
driver.quit()
logging.info("浏览器已关闭")

def generate_html_report(results):
    """生成HTML报告"""
    # 过滤出成功的记录并按坐骑数量排序
    successful_results = [r for r in results if r['状态'] == '成功']
    successful_results.sort(key=lambda x: int(x['坐骑数量'].split()[0]) if x['坐骑数量'] != "未知" else 0, reverse=True)
    
    html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>魔兽世界坐骑数量统计报告 - 一起公会</title>
    <link rel="stylesheet" href="css/style.css">
    <link rel="icon" href="img/favicon/favicon.ico" type="image/x-icon">
    <style>
        /* 坐骑统计页面专用样式 */
        .mounts-container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: var(--spacing-large);
        }}
        
        .mounts-header {{
            background: var(--color-bg-card);
            border: var(--border-width) solid var(--color-border);
            border-radius: var(--border-radius);
            padding: var(--spacing-large);
            margin-bottom: var(--spacing-large);
            text-align: center;
            backdrop-filter: blur(8px);
        }}
        
        .mounts-title {{
            color: var(--color-primary);
            font-size: 2.5em;
            margin: 0 0 var(--spacing-medium) 0;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
        }}
        
        .mounts-subtitle {{
            color: var(--color-text-secondary);
            font-size: 1.2em;
            margin: 0;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: var(--spacing-medium);
            margin-bottom: var(--spacing-large);
        }}
        
        .stat-card {{
            background: var(--color-bg-card);
            border: var(--border-width) solid var(--color-border);
            border-radius: var(--border-radius);
            padding: var(--spacing-medium);
            text-align: center;
            backdrop-filter: blur(8px);
        }}
        
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: var(--color-primary);
            margin-bottom: var(--spacing-small);
        }}
        
        .stat-label {{
            color: var(--color-text-secondary);
            font-size: 0.9em;
        }}
        
        .mounts-content {{
            background: var(--color-bg-card);
            border: var(--border-width) solid var(--color-border);
            border-radius: var(--border-radius);
            padding: var(--spacing-large);
            backdrop-filter: blur(8px);
        }}
        
        .content-title {{
            color: var(--color-primary);
            font-size: 1.8em;
            margin: 0 0 var(--spacing-medium) 0;
            text-align: center;
        }}
        
        .mounts-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: var(--spacing-medium);
        }}
        
        .mounts-table th {{
            background: linear-gradient(135deg, var(--color-secondary) 0%, var(--color-dark) 100%);
            color: var(--color-primary);
            padding: var(--spacing-medium);
            text-align: left;
            border-bottom: var(--border-width) solid var(--color-border);
            font-weight: bold;
        }}
        
        .mounts-table td {{
            padding: var(--spacing-medium);
            border-bottom: 1px solid var(--color-border);
            color: var(--color-text);
        }}
        
        .mounts-table tr:nth-child(even) {{
            background: rgba(255, 215, 0, 0.05);
        }}
        
        .mounts-table tr:hover {{
            background: rgba(255, 215, 0, 0.1);
            transition: background-color var(--transition-time);
        }}
        
        .rank-number {{
            color: var(--color-primary);
            font-weight: bold;
            text-align: center;
        }}
        
        .mount-count {{
            color: var(--color-success);
            font-weight: bold;
        }}
        
        .no-data {{
            text-align: center;
            color: var(--color-text-secondary);
            font-style: italic;
            padding: var(--spacing-large);
        }}
        
        .back-button {{
            display: inline-block;
            background: linear-gradient(135deg, var(--color-secondary) 0%, var(--color-dark) 100%);
            color: var(--color-primary);
            padding: var(--spacing-medium) var(--spacing-large);
            border: var(--border-width) solid var(--color-border);
            border-radius: var(--border-radius);
            text-decoration: none;
            font-weight: bold;
            transition: all var(--transition-time);
            margin-top: var(--spacing-large);
        }}
        
        .back-button:hover {{
            background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-secondary) 100%);
            color: var(--color-dark);
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        }}
        
        /* 响应式设计 */
        @media (max-width: 768px) {{
            .stats-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
            
            .mounts-table {{
                font-size: 0.9em;
            }}
            
            .mounts-table th,
            .mounts-table td {{
                padding: var(--spacing-small);
            }}
        }}
        
        @media (max-width: 480px) {{
            .stats-grid {{
                grid-template-columns: 1fr;
            }}
            
            .mounts-title {{
                font-size: 2em;
            }}
        }}
    </style>
</head>
<body>
    <div class="guild-header-container">
        <div class="header-content">
            <div class="header-logo">
                <img src="img/header-logo.png" alt="一起公会" class="logo-image">
            </div>
            <div class="header-text">
                <h1 class="guild-title">一起公会</h1>
                <p class="guild-motto">魔兽世界休闲公会</p>
            </div>
        </div>
    </div>

    <div class="mounts-container">
        <div class="mounts-header">
            <h1 class="mounts-title">🐉 坐骑数量统计</h1>
            <p class="mounts-subtitle">阿尔萨斯服务器 - 《一起》公会</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number" id="total-success">{len(successful_results)}</div>
                <div class="stat-label">成功获取</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="total-failed">{len(results) - len(successful_results)}</div>
                <div class="stat-label">获取失败</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="success-rate">{len(successful_results)/len(results)*100:.1f}%</div>
                <div class="stat-label">成功率</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="update-time">{datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
                <div class="stat-label">更新时间</div>
            </div>
        </div>
        
        <div class="mounts-content">
            <h2 class="content-title">🏆 坐骑排行榜</h2>
            <table class="mounts-table">
                <thead>
                    <tr>
                        <th>排名</th>
                        <th>角色名</th>
                        <th>坐骑数量</th>
                    </tr>
                </thead>
                <tbody id="mounts-table-body">
"""
    
    # 添加表格行（只显示成功的记录）
    for i, result in enumerate(successful_results, 1):
        html_content += f"""
                    <tr>
                        <td class="rank-number">{i}</td>
                        <td>{result['角色名']}</td>
                        <td class="mount-count">{result['坐骑数量']}</td>
                    </tr>
"""
    
    html_content += """
                </tbody>
            </table>
        </div>
        
        <div style="text-align: center;">
            <a href="index.html" class="back-button">← 返回主页</a>
        </div>
    </div>

    <script>
        // 动态更新统计数据
        function updateStats() {{
            const successCount = document.querySelectorAll('#mounts-table-body tr').length;
            const totalCount = {len(results)}; // 总角色数
            const failedCount = totalCount - successCount;
            const successRate = ((successCount / totalCount) * 100).toFixed(1);
            
            document.getElementById('total-success').textContent = successCount;
            document.getElementById('total-failed').textContent = failedCount;
            document.getElementById('success-rate').textContent = successRate + '%';
        }}
        
        // 页面加载完成后更新统计
        document.addEventListener('DOMContentLoaded', updateStats);
    </script>
</body>
</html>
"""
    
    # 添加表格行
    for i, result in enumerate(results, 1):
        status_class = "status-success" if result['状态'] == '成功' else "status-failed"
        mount_count_class = "mount-count" if result['坐骑数量'] != "未知" else ""
        
        html_content += f"""
                    <tr>
                        <td>{i}</td>
                        <td>{result['角色名']}</td>
                        <td class="{mount_count_class}">{result['坐骑数量']}</td>
                        <td class="{status_class}">{result['状态']}</td>
                    </tr>
"""
    
    html_content += """
                </tbody>
            </table>
        </div>
        
        <div class="footer">
            <p>© 2024 魔兽世界坐骑统计系统 | 数据来源：暴雪官方英雄榜</p>
        </div>
    </div>
</body>
</html>
"""
    
    # 写入HTML文件
    with open("mounts.html", "w", encoding="utf-8") as f:
        f.write(html_content)

# 生成HTML报告
logging.info("正在生成HTML报告...")
generate_html_report(results)

# 统计结果
success_count = len([r for r in results if r['状态'] == '成功'])
failed_count = len([r for r in results if r['状态'] == '失败'])

logging.info("=" * 60)
logging.info("批量爬取完成！")
logging.info(f"总角色数：{len(role_names)}")
logging.info(f"成功获取：{success_count} 个")
logging.info(f"获取失败：{failed_count} 个")
logging.info(f"成功率：{success_count/len(role_names)*100:.1f}%")
logging.info(f"HTML报告已保存到：mounts.html")
logging.info(f"详细日志已保存到：{log_filename}")
logging.info("=" * 60)

# 同时输出到控制台
print(f"\n✅ 批量爬取完成！共处理 {len(role_names)} 个角色")
print(f"📊 成功：{success_count} 个")
print(f"❌ 失败：{failed_count} 个")
print(f"📄 报告已保存到：mounts.html")
print(f"📝 详细日志已保存到：{log_filename}")

if __name__ == "__main__":
    # 如果直接运行此脚本，执行批量爬取
    pass 
    pass 