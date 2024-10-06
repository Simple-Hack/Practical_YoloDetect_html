from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from selenium.webdriver.edge.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import csv

# Read the data from the Excel file
df = pd.read_excel('D:\\onedrive\\电脑桌面\\data.xlsx')

# Create a dictionary of scenic spots and URLs
scenic_spots = {}
for _, row in df.iterrows():
    scenic_spots[row['名称']] = row['网址']

skipped_spots = []

def fun(name, url):
    print(f'This is {name}')
    
    opt = Options()
    opt.add_argument("--headless")
    opt.add_argument("window-size=1920x1080")
    opt.add_argument('--start-maximized')
    driver = webdriver.Edge(options=opt)
    
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    try:
        with open("啊_comment.csv", "a", encoding='utf-8-sig', newline='') as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow(('景点', '日期', '用户评论'))
            total_comments=None

            try:
                # 使用XPath来更精确地定位元素
                module_title_element = wait.until(
                    EC.presence_of_element_located((By.XPATH, "//div[@class='moduleTitle' and contains(text(), '用户点评')]"))
                )
                total_comments_text = module_title_element.text
                
                if '(' in total_comments_text and ')' in total_comments_text:
                    total_comments_str = total_comments_text.split('(')[1].split(')')[0]
                    total_comments = int(total_comments_str)
                    print(f"Total comments: {total_comments}")
                else:
                    print(f"Unexpected format for total comments: {total_comments_text}")
                    total_comments = 0  # 如果格式错误，给total_comments一个默认值0
            except Exception as e:
                print(f"An error occurred while getting total comments: {e}")
                total_comments = 0  # 如果发生异常，也给total_comments一个默认值0
            
            # 计算总页数
            total_pages = (total_comments + 9) // 10

            for y in range(2, min(total_pages + 1,300)):
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

                    # 获取"下一页"按钮
                    next_page_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//ul[@class='ant-pagination']/li[@title='下一页']/span/a")))
                    ActionChains(driver).move_to_element(next_page_button).click().perform()

                except NoSuchElementException:
                    print(f"Element not found for page {y}, skipping...")
                    break
                except TimeoutException:
                    print(f"TimeoutException occurred for page {y}, skipping...")
                    break

                print(y)

    except TimeoutException:
        print(f"TimeoutException occurred for {name}, skipping...")
        skipped_spots.append(name)
    finally:
        driver.quit()

for spot_name, url in scenic_spots.items():
    try:
        fun(spot_name, url)
    except TimeoutException:
        print(f"TimeoutException occurred for {spot_name}, skipping...")
        skipped_spots.append(spot_name)

print("Skipped Spots:")
for spot in skipped_spots:
    print(spot)