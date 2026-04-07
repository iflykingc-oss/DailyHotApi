import requests
import json
from datetime import datetime
import os

# 创建输出目录
os.makedirs("dist/api", exist_ok=True)

# 抓取所有平台热榜
all_data = []
platforms = [
    {"name": "知乎热榜", "url": "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50"},
    {"name": "微博热搜", "url": "https://weibo.com/ajax/side/hotSearch"},
    {"name": "抖音热榜", "url": "https://www.douyin.com/aweme/v1/web/hot/search/list/"},
    {"name": "番茄短篇", "url": "https://fanqienovel.com/api/top/short?page=1&size=50"}
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
}

for platform in platforms:
    try:
        res = requests.get(platform["url"], headers=headers, timeout=15)
        data = res.json()
        items = []
        
        if platform["name"] == "知乎热榜":
            for item in data["data"]:
                items.append({
                    "title": item["target"]["title"],
                    "hot": item["detail_text"].replace("万热度", "") + "万",
                    "desc": item["target"].get("excerpt", "")
                })
        elif platform["name"] == "微博热搜":
            for item in data["data"]["realtime"]:
                items.append({
                    "title": item["note"],
                    "hot": str(item.get("num", 50000)),
                    "desc": ""
                })
        elif platform["name"] == "抖音热榜":
            for item in data["data"]["word_list"]:
                items.append({
                    "title": item["word"],
                    "hot": str(item.get("hot_value", 50000)),
                    "desc": ""
                })
        elif platform["name"] == "番茄短篇":
            for item in data["data"]["list"]:
                items.append({
                    "title": item["title"],
                    "hot": str(item.get("read_count", 80000)),
                    "desc": item.get("intro", "")
                })
        
        all_data.append({
            "name": platform["name"],
            "data": items[:30] # 只取前30条
        })
        print(f"✅ {platform['name']} 抓取成功，共 {len(items)} 条")
    except Exception as e:
        print(f"❌ {platform['name']} 抓取失败: {str(e)}")

# 生成最终JSON
result = {
    "updateTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "data": all_data
}

# 保存文件
with open("dist/api/all.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"\n✅ 全部完成！共获取 {sum(len(p['data']) for p in all_data)} 条热榜数据")
