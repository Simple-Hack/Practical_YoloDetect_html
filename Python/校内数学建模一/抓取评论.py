import requests
import json
import pandas as pd
from tqdm import tqdm
import os

# 定义景区字典，键为景区名，值为poiId
scenic_areas = {
    '景区A': 81011,
    '重庆大足石刻景区' : 78129,
    # '景区B': 67890,
    # 更多景区...
}

# 文件名
file_name = '所有景区评论.xlsx'

# 遍历景区字典
for scenic_name, poi_id in scenic_areas.items():
    print(f"开始抓取 {scenic_name} 的评论信息...")

    userNames = []
    commentDetails = []
    commentTimes = []

    total_pages = 14

    for page_num in tqdm(range(0, total_pages), desc=f'爬取 {scenic_name} 进度', unit='页'):
        payload = {
            "arg": {
                "channelType": 2,
                "collapseTpte": 0,
                "commentTagId": 0,
                "pageSize": 50,
                "poiId": poi_id,
                "sourseType": 1,
                "sortType": 3,
                "pageIndex": page_num,
                "starType": 0
            },
            "head": {
                "cid": "09031062417234242897",
                "ctok": "",
                "cver": "1.0",
                "lang": "01",
                "sid": "888",
                "syscode": "09",
                "auth": "",
                "xsid": "",
                "extension": []
            }
        }
        postUrl = "https://m.ctrip.com/restapi/soa2/13444/json/getCommentCollapseList"

        response = requests.post(postUrl, data=json.dumps(payload))
        html_1 = response.json()

        # 检查响应中是否存在'items'
        if 'items' in html_1["result"]:
            commentItems = html_1["result"]["items"]

            for item in commentItems:
                if item is not None and 'userInfo' in item and 'userNick' in item['userInfo']:
                    userName = item['userInfo']['userNick']
                    commentDetail = item['content']
                    commentTime = item['publishTypeTag']

                    userNames.append(userName)
                    commentDetails.append(commentDetail)
                    commentTimes.append(commentTime)

    # 创建 DataFrame
    df = pd.DataFrame({
        '用户评论内容': commentDetails,
        '用户名': userNames,
        '用户评论时间': commentTimes
    })

    # 保存到 Excel 文件，每个景区一个工作表
    # 检查文件是否存在
    if not os.path.exists(file_name):
        # 如果文件不存在，创建文件和第一个工作表
        with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=scenic_name, index=False)
    else:
        # 如果文件存在，追加数据到当前景区的工作表
        with pd.ExcelWriter(file_name, engine='openpyxl', mode='a') as writer:
            df.to_excel(writer, sheet_name=scenic_name, index=False)

print("所有景区的评论信息抓取完成！")