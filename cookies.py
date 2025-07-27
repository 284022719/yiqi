from selenium import webdriver
import pickle
import time

# 启动浏览器
driver = webdriver.Chrome()
driver.get("https://wow.blizzard.cn/")

print("请在新打开的浏览器窗口中手动登录魔兽世界官网。")
input("登录完成后，回到此窗口并按回车继续...")

# 保存Cookie到文件
with open("cookies.pkl", "wb") as f:
    pickle.dump(driver.get_cookies(), f)
print("Cookie已保存到 cookies.pkl")

driver.quit()