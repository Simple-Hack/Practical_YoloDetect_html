from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.edge.options import Options
import time

# 定义Edge WebDriver的路径
browser_path = r"C:\Users\simple\.conda\envs\D2024-7-9\msedgedriver.exe"

# 创建Service对象
service = Service(browser_path)
opt = Options()
opt.add_argument("--headless")
opt.add_argument("window-size=1920x1080")
opt.add_argument('--start-maximized')

# 启动Edge WebDriver
browser = webdriver.Edge(service=service, options=opt)

# 导航到目标网址
url = 'https://you.ctrip.com/sight/chongqing158.html'
browser.get(url)

# 创建WebDriverWait实例
wait = WebDriverWait(browser, 10)

try:
    while True:
        # 使用XPath来定位所有景区元素
        sight_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="titleModule_box__VMMFM"]/div[@class="titleModule_name__Li4Tv"]')))

        # 遍历每个景区元素
        for i, sight_element in enumerate(sight_elements):
            try:
                # 提取景区名称
                name_element = sight_element.find_element(By.XPATH, './/span[1]/a')
                name = name_element.text
                link = name_element.get_attribute('href')

                # 尝试获取星级
                try:
                    level_element = sight_element.find_element(By.XPATH, './/span[@class="titleModule_level-text-view__40Dbg titleModule_level-text__lxAaP"]')
                    level = level_element.text
                except NoSuchElementException:
                    level = "没有星级"
                if level != "没有星级" and level[0] >= '3':
                    try:
                        browser.get(link)
                        # 在新页面中定位元素
                        try:
                            # 定位平均分数
                            average_score_element = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="averageScoreBox"]/span[@class="averageScore"]')))
                            average_score = average_score_element.text
                            average_score = float(average_score)
                            print(average_score)

                            # 等待评论加载完成
                            # 这里假设评论是通过滚动来加载的
                            # 可以模拟滚动来确保评论加载完成
                            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                            time.sleep(1)  # 给评论加载的时间

                            # 返回到列表页面
                            browser.back()
                            wait.until(EC.url_to_be(url))
                            
                            # 重新获取景区元素列表
                            sight_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="titleModule_box__VMMFM"]/div[@class="titleModule_name__Li4Tv"]')))
                            continue  # 跳过下一次循环的元素列表检查，直接进入下一个景区元素的处理
                        
                        except Exception as e:
                            print(f"访问详情页时发生错误: {e}")

                    except Exception as e:
                        print(f"访问详情页时发生错误: {e}")

                print(f"景区名称: {name}")
                print(f"星级: {level}")
                print(f"详情链接: {link}")
                print("-" * 40)

            except StaleElementReferenceException:
                # 如果元素变得无效，重新获取整个景区元素列表
                break  # 退出当前循环，重新获取元素列表

except NoSuchElementException:
    print("没有找到任何景区元素")

finally:
    # 确保关闭浏览器
    browser.quit()