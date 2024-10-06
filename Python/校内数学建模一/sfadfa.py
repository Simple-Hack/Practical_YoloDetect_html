from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
 
from selenium.webdriver.edge.options import Options
 
def to_the_buttom():
    js = 'document.getElementsByClassName("search-body left_is_mini")[0].scrollTop=10000'
    driver.execute_script(js)
def to_the_top():
    js = "var q=document.documentElement.scrollTop=0"  # 滚动到最上面
    driver.execute_script(js)
def to_deal_question():
    driver.implicitly_wait(10)
    time.sleep(3)
    to_the_buttom()
    time.sleep(3)
def to_view():
    driver.implicitly_wait(10)
    to_the_buttom()
    time.sleep(3)
    button = driver.find_element(By.XPATH, '//*[@id="commentModule"]/div[6]/ul/li[7]/a')
    driver.execute_script("arguments[0].scrollIntoView();", button)
 
opt = Options()
opt.add_argument("--headless")
opt.add_argument("window-size=1920x1080")
opt.add_argument('--start-maximized')
driver = webdriver.Edge(options=opt)
url = 'https://you.ctrip.com/sight/chongqing158/10395.html'
driver.get(url)
# driver.maximize_window()
 
#  add_argument() 方法添加参数
 
print(1)
with open("my_comment.txt", "a", encoding='utf-8') as f:
    for y in range(2,5):
        time.sleep(3)
        # to_deal_question()
        for x in range(10):
            text = driver.find_elements(By.CLASS_NAME, "commentDetail")[x].text
            print(text)
            f.write(text)
            f.write("\n")
        el = driver.find_element(By.XPATH, '//*[@id="commentModule"]/div[6]/ul/li[{}]/a'.format(y))  # 找到元素
        ActionChains(driver).move_to_element(el).click().perform()
        button = driver.find_element(By.XPATH, '//*[@id="commentModule"]/div[6]/ul/li[{}]/a'.format(y))
        button.click()
        print(y)
with open("dao_chen_ya_ding.txt", "a", encoding='utf-8') as f:
    for y in range(5,300):
        time.sleep(3)
        # to_deal_question()
        # to_view()
        for x in range(10):
            text = driver.find_elements(By.CLASS_NAME, "commentDetail")[x].text
            f.write(text)
            print(text)
            f.write("\n")
        el = driver.find_element(By.XPATH, '//*[@id="commentModule"]/div[6]/ul/li[7]/a')  # 找到元素
        ActionChains(driver).move_to_element(el).click().perform()
        button = driver.find_element(By.XPATH, '//*[@id="commentModule"]/div[6]/ul/li[7]/a')
        button.click()
        print(y)
 
 
time.sleep(1000)
driver.close()