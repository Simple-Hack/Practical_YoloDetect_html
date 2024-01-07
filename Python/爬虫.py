import requests
from bs4 import BeautifulSoup
cookies = {
    'BAIDUID': '14168269E9FA769E539EE56C635D99CA:FG=1',
    'BAIDUID_BFESS': '14168269E9FA769E539EE56C635D99CA:FG=1',
    '__bid_n': '1862ae89060f776dd64207',
    'RT': '"z=1&dm=baidu.com&si=9c138088-7b67-48d8-9c29-a3a24c90b668&ss=li8r1mob&sl=2&tt=1m0&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=7w4&ul=16f80&hd=16f9j"',
    'FPTOKEN': 'NTzbiMWWhnTp8ZAypfWKIvarUqVvqiJ/tHHktpEPg8Jwa67zBv0lYHxZZ+Eeu3jtKet1tfc6PeB7Q/2A/HZBfJHylNqPRxdRPPTgx6HgtV0tSNdSI2RivtsNUBl1wOEGY8ENdAJczfSS7KEtqnwU6RXcyJzSXRv1kfxXNEM2T8nJC8Ux+0rEkIF18zoOiRkGoooLkI+l551pSLYPvjiSQCqlgzxDlU1Ay97E6MUVwzDpHl3NCzDuDcmW0m2UaNdWrep8e5xVOJIdbWdkQSz8aFpOYkScJFA54QVLNdpT2mbX8gueLFxAuLdBzZdHIbXZe4F1zbJfiPMOv6NdSmH4WozrGE3VQfkYDBc8kCU5I7ugYY5X7AGI3+RPz9Vj33yFnl/MnmP7IQdK8l0u4XmUwAVpjydBPaWEFaVoZCO8zeqzbbwPJZp8OkCilvXKCHBE|xryUo00IGKxfjOhqBWevpKUSIzpSPgpI5QTAjuvEO8c=|10|8e4651e6e201cc7bd975478946b1ef53',
}
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # 'Cookie': 'BAIDUID=14168269E9FA769E539EE56C635D99CA:FG=1; BAIDUID_BFESS=14168269E9FA769E539EE56C635D99CA:FG=1; __bid_n=1862ae89060f776dd64207; RT="z=1&dm=baidu.com&si=9c138088-7b67-48d8-9c29-a3a24c90b668&ss=li8r1mob&sl=2&tt=1m0&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=7w4&ul=16f80&hd=16f9j"; FPTOKEN=NTzbiMWWhnTp8ZAypfWKIvarUqVvqiJ/tHHktpEPg8Jwa67zBv0lYHxZZ+Eeu3jtKet1tfc6PeB7Q/2A/HZBfJHylNqPRxdRPPTgx6HgtV0tSNdSI2RivtsNUBl1wOEGY8ENdAJczfSS7KEtqnwU6RXcyJzSXRv1kfxXNEM2T8nJC8Ux+0rEkIF18zoOiRkGoooLkI+l551pSLYPvjiSQCqlgzxDlU1Ay97E6MUVwzDpHl3NCzDuDcmW0m2UaNdWrep8e5xVOJIdbWdkQSz8aFpOYkScJFA54QVLNdpT2mbX8gueLFxAuLdBzZdHIbXZe4F1zbJfiPMOv6NdSmH4WozrGE3VQfkYDBc8kCU5I7ugYY5X7AGI3+RPz9Vj33yFnl/MnmP7IQdK8l0u4XmUwAVpjydBPaWEFaVoZCO8zeqzbbwPJZp8OkCilvXKCHBE|xryUo00IGKxfjOhqBWevpKUSIzpSPgpI5QTAjuvEO8c=|10|8e4651e6e201cc7bd975478946b1ef53',
    'Referer': 'https://top.baidu.com/board',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57',
    'sec-ch-ua': '"Microsoft Edge";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}
params = {
    'tab': 'realtime',
}
response = requests.get('https://top.baidu.com/board', params=params, cookies=cookies, headers=headers)
content="#sanRoot > main > div.container.right-container_2EFJr > div > div:nth-child(2) > div > div.content_1YWBm > a > div.c-single-text-ellipsis"
response.encoding='utf-8'
soup=BeautifulSoup(response.text,'html.parser')
f=open("../../百度热搜.txt",'a',encoding='utf-8')
a=soup.select(content)
for i in range(0,len(a)):
    a[i]=a[i].text
    f.write(a[i]+'\n')
f.write('百度热搜榜单')
f.close()
