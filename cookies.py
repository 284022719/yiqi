from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pickle

# 启动浏览器并加载 Cookie
driver = webdriver.Chrome()
driver.get("https://wow.blizzard.cn/")  # 先访问主域名

# 加载 Cookie
with open("cookies.pkl", "rb") as f:
    cookies = pickle.load(f)
    for cookie in cookies:
        if 'sameSite' in cookie:
            del cookie['sameSite']
        driver.add_cookie(cookie)

# 直接访问角色页面
url = "https://wow.blizzard.cn/character/#/arthas/快来骑我吧/"
driver.get(url)
time.sleep(5)  # 等待页面加载

# 在搜索框中搜索"久世"
try:
    # 定位搜索框
    search_box = driver.find_element(By.CSS_SELECTOR, "input[placeholder*='搜索角色']")
    search_box.clear()
    search_box.send_keys("久世")
    search_box.send_keys(Keys.ENTER)
    
    print("已在搜索框中输入：久世")
    time.sleep(3)  # 等待搜索结果出现
    
    # 在搜索结果中选择阿尔萨斯服务器的"久世"角色
    # 根据HTML结构，使用更精确的选择器
    try:
        # 方法1：使用CSS选择器定位包含"地心之战-阿尔萨斯"的角色条目
        arthas_jiushi = driver.find_element(By.XPATH, "//a[contains(@class,'roleItems')]//div[contains(@class,'roleDesc2') and contains(text(),'地心之战-阿尔萨斯')]/ancestor::a")
        arthas_jiushi.click()
        print("已选择阿尔萨斯服务器的久世角色")
    except:
        try:
            # 方法2：使用你提供的CSS选择器
            arthas_jiushi = driver.find_element(By.CSS_SELECTOR, "#app > div.container-search > div > div.listCons > div > div > a:nth-child(3)")
            arthas_jiushi.click()
            print("已选择阿尔萨斯服务器的久世角色（方法2）")
        except:
            # 方法3：使用你提供的XPATH
            arthas_jiushi = driver.find_element(By.XPATH, "//*[@id='app']/div[2]/div/div[4]/div/div/a[3]")
            arthas_jiushi.click()
            print("已选择阿尔萨斯服务器的久世角色（方法3）")
    
    print("已选择阿尔萨斯服务器的久世角色")
    time.sleep(5)  # 等待角色页面加载
    
    # 检查是否成功跳转到角色详情页
    current_url = driver.current_url
    print(f"当前页面URL：{current_url}")
    
    # 如果还在搜索页面，尝试直接访问角色页面
    if "search" in current_url:
        print("页面仍在搜索页面，尝试直接访问角色页面...")
        try:
            # 直接访问角色页面
            role_url = "https://wow.blizzard.cn/character/#/arthas/久世/"
            driver.get(role_url)
            time.sleep(5)
            print(f"直接访问角色页面：{driver.current_url}")
        except Exception as e:
            print(f"直接访问角色页面失败：{e}")
            driver.quit()
            exit()
    
    # 现在可以点击"收藏"标签
    try:
        # 等待页面加载完成
        time.sleep(3)
        
        # 点击"收藏"标签 - 使用多种方法
        try:
            # 方法1：使用你提供的XPATH
            collect_tab = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/div[1]/div[3]/a[3]")
            collect_tab.click()
            print("已点击收藏标签（方法1）")
        except:
            try:
                # 方法2：查找包含"收藏"的链接
                collect_tab = driver.find_element(By.XPATH, "//a[contains(text(),'收藏')]")
                collect_tab.click()
                print("已点击收藏标签（方法2）")
            except:
                try:
                    # 方法3：查找包含"收藏"的span
                    collect_tab = driver.find_element(By.XPATH, "//span[contains(text(),'收藏')]")
                    collect_tab.click()
                    print("已点击收藏标签（方法3）")
                except Exception as e:
                    print(f"无法找到收藏标签：{e}")
                    # 打印当前页面URL和部分源码
                    print(f"当前页面URL：{driver.current_url}")
                    print("页面源码片段：")
                    print(driver.page_source[:3000])
                    raise e
        
        time.sleep(2)
        
        # 点击"坐骑"子标签 - 使用多种方法
        try:
            # 方法1：使用你提供的XPATH
            mount_tab = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/div[2]/div[1]/div/a[2]")
            mount_tab.click()
            print("已点击坐骑标签（方法1）")
        except:
            try:
                # 方法2：查找包含"坐骑"的链接
                mount_tab = driver.find_element(By.XPATH, "//a[contains(text(),'坐骑')]")
                mount_tab.click()
                print("已点击坐骑标签（方法2）")
            except:
                try:
                    # 方法3：查找包含"坐骑"的span
                    mount_tab = driver.find_element(By.XPATH, "//span[contains(text(),'坐骑')]")
                    mount_tab.click()
                    print("已点击坐骑标签（方法3）")
                except Exception as e:
                    print(f"无法找到坐骑标签：{e}")
                    raise e
        
        time.sleep(2)
        
        # 获取坐骑数量 - 使用多种方法确保能获取到
        try:
            # 方法1：直接查找包含"坐骑"和"个不同的坐骑"的文本
            mount_count_elem = driver.find_element(By.XPATH, "//*[contains(text(),'坐骑') and contains(text(),'个不同的坐骑')]")
            print(f"久世 坐骑数量：{mount_count_elem.text}")
        except:
            try:
                # 方法2：查找包含数字和"个不同的坐骑"的文本
                mount_count_elem = driver.find_element(By.XPATH, "//*[contains(text(),'个不同的坐骑')]")
                print(f"久世 坐骑数量：{mount_count_elem.text}")
            except:
                try:
                    # 方法3：查找包含"坐骑"的文本，然后提取数字
                    mount_elements = driver.find_elements(By.XPATH, "//*[contains(text(),'坐骑')]")
                    for elem in mount_elements:
                        text = elem.text
                        if '个不同的坐骑' in text:
                            print(f"久世 坐骑数量：{text}")
                            break
                except Exception as e:
                    print(f"无法获取坐骑数量：{e}")
                    # 打印页面源码以便调试
                    print("页面源码片段：")
                    print(driver.page_source[:2000])
        
    except Exception as e:
        print(f"获取坐骑数量失败：{e}")
    
except Exception as e:
    print(f"搜索或选择角色失败：{e}")

input("按回车关闭浏览器...")
driver.quit()