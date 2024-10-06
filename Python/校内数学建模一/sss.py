from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from selenium.webdriver.edge.options import Options
from selenium.common.exceptions import NoSuchElementException
import csv
# Read the data from the Excel file
df = pd.read_excel('D:\\onedrive\\电脑桌面\\data.xlsx')

# Create a dictionary of scenic spots and URLs
scenic_spots = {}
for _, row in df.iterrows():
    scenic_spots[row['名称']] = row['网址']

def to_the_buttom():
    js = 'document.getElementsByClassName("search-body left_is_mini")[0].scrollTop=10000'
    driver.execute_script(js)
def to_the_top():
    js = "var q=document.documentElement.scrollTop=0"  # 滚动到最上面
    driver.execute_script(js)
def to_view():
    driver.implicitly_wait(10)#隐式等待10s，条件成立则立即结束等待
    to_the_buttom()
    time.sleep(3)
    button = driver.find_element(By.CSS_SELECTOR,'li.ant-pagination-next>span')
    driver.execute_script("arguments[0].scrollIntoView();", button)    

def fun(name, url):  
    print(f'This is {name}')  
    # 注意：对于Edge浏览器，应使用EdgeOptions  
    # opt = Options()  # 这里应该使用EdgeOptions()  
    # opt.add_argument("--headless")  
    # opt.add_argument("window-size=1920x1080")  # 注意：与--start-maximized冲突  
    # opt.add_argument('--start-maximized')  
    # driver = webdriver.Edge(options=opt)  # 确保安装了msedgedriver  
    
    # 假设这里使用Chrome作为示例  
    opt = Options()  
    opt.add_argument("--headless")  
    opt.add_argument("window-size=1920x1080")
    opt.add_argument('--start-maximized')
    driver = webdriver.Edge(options=opt)  
  
    driver.get(url)  
    wait = WebDriverWait(driver, 10)
    try:  
        with open("all_comment.csv", "a", encoding='utf-8-sig', newline='') as f:  
            csvwriter = csv.writer(f)
            csvwriter.writerow(('景点', '日期', '用户评论'))
            for y in range(2, 5):  
                try:  
                    time.sleep(3)  
                    comments = driver.find_elements(By.CLASS_NAME, "commentDetail")  
                    dates = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "commentTime")))
                    if len(comments) < 10:  
                        print(f"Less than 10 comments found for page {y}, skipping...")  
                        break  # 跳过当前循环，继续下一个y  
  
                    for i, comment in enumerate(comments):
                        text = comment.text.strip().replace('\n', '')
                        date = dates[i].text.strip().replace('\n', '')
                        csvwriter.writerow((name, date, text))
                        f.flush()
                        print(text)
  
                    # 使用动态XPath处理不同页码  
                    el_xpath = f'//*[@id="commentModule"]/div[6]/ul/li[{y}]/a'  
                    el = driver.find_element(By.XPATH, el_xpath)  
                    ActionChains(driver).move_to_element(el).click().perform()  
                    # 注意：这里可能不需要再次点击，因为move_to_element().click()已经执行了点击  
  
                except NoSuchElementException:  
                    print(f"Element not found for page {y}, skipping...")  
                    break
                # except IndexError:  
                #     print(f"IndexError occurred for page {y}, skipping...")  
                #     continue  
                print(y)  
  
        with open("all_comment.csv", "a", encoding='utf-8-sig', newline='') as f:  
            csvwriter = csv.writer(f)
            csvwriter.writerow(('景点', '日期', '用户评论'))
            for y in range(5, 40):  
                try:  
                    time.sleep(3)  
                    comments = driver.find_elements(By.CLASS_NAME, "commentDetail")  
                    dates = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "commentTime")))
                    if len(comments) < 10:  
                        print(f"Less than 10 comments found for page {y}, skipping...")  
                        break  
  
                    for i, comment in enumerate(comments):
                        text = comment.text.strip().replace('\n', '')
                        date = dates[i].text.strip().replace('\n', '')
                        csvwriter.writerow((name, date, text))
                        f.flush()
                        print(text)
  
                    # 注意：这里似乎对于所有y值都使用了相同的XPath，可能需要调整  
                    el_xpath = '//*[@id="commentModule"]/div[6]/ul/li[7]/a'  
                    el = driver.find_element(By.XPATH, el_xpath)  
                    ActionChains(driver).move_to_element(el).click().perform()  
  
                except NoSuchElementException:  
                    print(f"Element not found for page {y}, skipping...")  
                    break 
                # except IndexError:  
                #     print(f"IndexError occurred for page {y}, skipping...")  
                #     continue  
                print(y)  
  
    finally:  
        driver.quit()  # 确保最后关闭浏览器 
    

for spot_name, url in scenic_spots.items():
    fun(spot_name, url)
