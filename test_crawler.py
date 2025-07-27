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
    "久世"
]

# 启动日志记录
log_filename = setup_logging()
logging.info("=" * 60)
logging.info("魔兽世界坐骑数量批量爬取系统启动")
logging.info("=" * 60)

# 启动浏览器并加载 Cookie
logging.info("正在启动浏览器...")
print("准备启动webdriver")  # 新增
try:
    driver = webdriver.Chrome()
    print("webdriver已启动")  # 新增
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
            collect_tab = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/div[1]/div[3]/a[3]")
            collect_tab.click()
            logging.info("已点击收藏标签")
        except Exception as e:
            logging.error(f"无法找到收藏标签: {e}")
            raise e
        
        time.sleep(2)
        
        # 点击"坐骑"子标签
        try:
            mount_tab = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/div[2]/div[1]/div/a[2]")
            mount_tab.click()
            logging.info("已点击坐骑标签")
        except Exception as e:
            logging.error(f"无法找到坐骑标签: {e}")
            raise e
        
        # 点击坐骑标签后
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[2]/div[2]/div[2]/div[2]/div[3]/div/div'))
        )
        
        # 获取坐骑数量
        mount_count = "未知"
        try:
            mount_count_elem = driver.find_element(By.XPATH, "//*[contains(text(),'坐骑') and contains(text(),'个不同的坐骑')]")
            mount_count_text = mount_count_elem.text
            import re
            match = re.search(r'(\d+)', mount_count_text)
            if match:
                mount_count = match.group(1)
            else:
                mount_count = "未知"
            logging.info(f"坐骑数量：{mount_count_text}，提取数字：{mount_count}")
        except Exception as e:
            logging.error(f"无法获取坐骑数量: {e}")

        # 获取最近三个坐骑的名字和图片链接（分别用不同的XPath）
        # 获取所有坐骑卡片div
        mount_cards = driver.find_elements(By.XPATH, '//*[@id="app"]/div[2]/div[2]/div[2]/div[2]/div[3]/div/div')
        recent_mounts = []
        for card in mount_cards[:3]:
            try:
                name_elem = card.find_element(By.XPATH, './/div/div/div[2]/div/div')
                img_elem = card.find_element(By.XPATH, './/div/div/div[1]/div/img')
                mount_name = name_elem.text.strip()
                mount_img = img_elem.get_attribute('src')
                recent_mounts.append({"name": mount_name, "img": mount_img})
            except Exception as e:
                logging.warning(f"单个坐骑信息获取失败: {e}")
        logging.info(f"最近三个坐骑: {recent_mounts}")

        # 保存结果
        results.append({
            "name": name,
            "mounts": mount_count,
            "recent_mounts": recent_mounts,
            "status": "成功" if mount_count != "未知" else "失败"
        })
        
        logging.info(f"角色 {name} 处理完成，状态：{'成功' if mount_count != '未知' else '失败'}")
        
    except Exception as e:
        logging.error(f"处理角色 {name} 失败：{e}")
        results.append({
            "name": name,
            "mounts": "未知",
            "status": "失败"
        })
    
    logging.info("-" * 30)

# 关闭浏览器
logging.info("正在关闭浏览器...")
driver.quit()
logging.info("浏览器已关闭")

import json
json_path = os.path.join('data', 'test.json')
os.makedirs('data', exist_ok=True)
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
logging.info(f"数据已保存到 {json_path}")
print(f"📄 数据已保存到：{json_path}")
# 统计结果
success_count = len([r for r in results if r['status'] == '成功'])
failed_count = len([r for r in results if r['status'] == '失败'])

logging.info("=" * 60)
logging.info("批量爬取完成！")
logging.info(f"总角色数：{len(role_names)}")
logging.info(f"成功获取：{success_count} 个")
logging.info(f"获取失败：{failed_count} 个")
logging.info(f"成功率：{success_count/len(role_names)*100:.1f}%")
logging.info(f"详细日志已保存到：{log_filename}")
logging.info("=" * 60)

print(f"\\n✅ 批量爬取完成！共处理 {len(role_names)} 个角色")
print(f"📊 成功：{success_count} 个")
print(f"❌ 失败：{failed_count} 个")
print(f"📝 详细日志已保存到：{log_filename}")
print(f"📄 数据已保存到：{json_path}")

if __name__ == "__main__":
    # 如果直接运行此脚本，执行批量爬取
    pass 
    pass 