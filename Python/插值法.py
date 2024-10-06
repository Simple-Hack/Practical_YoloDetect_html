import requests
from bs4 import BeautifulSoup
import csv
import re
def get_page_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.find_all('li', {'class': 'item'})
    data = []
    for item in items:
        name = item.find('span', {'class': 'cn_tit'})
        star_width = item.find('span', {'class': 'cur_star'})
        detail_link = item.find('a', {'class': 'titlink'})
        
        if name:
            name = name.text.strip()
        else:
            name = ""  # 将 name 设置为一个空字符串，而不是 None
        
        if star_width and 'style' in star_width.attrs:
            rating = round(float(star_width['style'].split(':')[1].strip().replace('%', '')) / 20, 1)
        else:
            rating = None
        
        if detail_link:
            detail_url = detail_link['href']
            detail_response = requests.get(detail_url)
            detail_soup = BeautifulSoup(detail_response.text, 'html.parser')
            comments = detail_soup.find_all('div', {'class': 'e_comment_main_inner'})
            
            comment_details = []
            for comment in comments:
                title = comment.find('div', {'class': 'e_comment_title'}).find('a').text.strip()
                content = comment.find('div', {'class': 'e_comment_content'}).text.strip()
                star_box = comment.find('div', {'class': 'e_comment_star_box'})
                if star_box:
                    star_span = star_box.find('span', {'class': 'cur_star'})
                    if star_span and 'style' in star_span.attrs:
                        star_rating = round(float(star_span['style'].split(':')[1].strip().replace('%', '')) / 20, 1)
                    else:
                        star_rating = None
                else:
                    star_rating = None
                
                add_info = comment.find('div', {'class': 'e_comment_add_info'})
                if add_info:
                    date = add_info.find('ul').find('li').text.strip()
                else:
                    date = None
                
                comment_details.append({
                    'title': title,
                    'content': content,
                    'date': date,
                    'rating': star_rating
                })
        else:
            comment_details = []
        
        data.append({
            'name': name,
            'rating': rating,
            'comments': comment_details
        })
    
    return data

def get_all_comments(url):
    comments = get_page_data(url)
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    paging = soup.find('div', {'class': 'b_paging'})
    if not paging:
        return comments
    last_page_match = re.search(r'(\d+)', paging.find_all('a', {'class': 'page'})[-1].text.strip())
    if last_page_match:
        last_page = int(last_page_match.group(1))
    else:
        last_page = 1
    for i in range(2, last_page + 1):
        page_url = f"{url}-1-{i}"
        comments.extend(get_page_data(page_url))
    return comments

def write_to_file(comments, file_name="results.csv"):
    with open(file_name, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["景区名称", "星级评价", "评论标题", "评论内容", "评论日期", "评论评分"])
        for comment in comments:
            # 将景区名称转换为字符串
            name_str = str(comment['name'])
            for c in comment['comments']:
                writer.writerow([
                    comment['name'],
                    comment['rating'],
                    c['title'],
                    c['content'],
                    c['date'],
                    c['rating']
                ])

# 示例URL
url = "https://travel.qunar.com/p-cs299979-chongqing-jingdian"
comments = get_all_comments(url)

for i in range(2, 12):  # 假设总共有9页
    url = f"https://travel.qunar.com/p-cs299979-chongqing-jingdian-1-{i}"
    print(f"\n{url}\n")
    comments += get_all_comments(url)
# 写入数据
write_to_file(comments)

