import os
import json
import requests
import datetime

DEEPSEEK_API_KEY = os.environ['DEEPSEEK_API_KEY']
NOTION_TOKEN = os.environ['NOTION_TOKEN']
NOTION_PAGE_ID = os.environ['NOTION_PAGE_ID']

def generate_content():
    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    prompt = """请生成今日学习内容，返回 JSON 格式，包含以下字段：
{
  "politics_hotspot": "考研政治热点（简短总结，50字内）",
  "news_hotspot": "新闻热点（简短总结，50字内）",
  "editing_task": "剪辑新手任务（今天学习一个技巧，含作业，80字内）",
  "memory_essay": "30天趣味记忆小作文第X篇（英文原文+中文翻译+重点词汇列表，英文约80词）"
}
注意：今天是2026年8月31日，考研政治热点请基于此时政。英文小作文使用红宝书考研词汇，词汇难度适中。返回纯JSON，不要有其他文字。"""

    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    content = result['choices'][0]['message']['content']
    content = content.strip()
    if content.startswith("```"):
        content = content.split('\n', 1)[1].rsplit('```', 1)[0]
    return json.loads(content)

def get_heading_ids():
    url = f"https://api.notion.com/v1/blocks/{NOTION_PAGE_ID}/children?page_size=100"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    blocks = response.json()['results']
    heading_map = {}
    # 关键词列表，用于匹配标题（不区分 emoji 和空格）
    keywords = {
        "考研政治热点": "politics",
        "新闻热点": "news",
        "剪辑任务": "editing",
        "英语任务": "english"
    }
    for block in blocks:
        # 兼容 H1 和 H2
        if block['type'] in ['heading_1', 'heading_2']:
            # 获取标题文本
            text_obj = block[block['type']].get('rich_text', [])
            if not text_obj:
                continue
            text = text_obj[0].get('plain_text', '')
            # 去除 emoji 和空格后匹配关键词
            for key, value in keywords.items():
                # 检查标题文本是否包含关键词
                if key in text:
                    heading_map[key] = block['id']
                    print(f"Found heading: {text} -> {value}")
                    break
    return heading_map

def insert_after_heading(heading_id, blocks):
    url = f"https://api.notion.com/v1/blocks/{heading_id}/children"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    data = {"children": blocks}
    response = requests.patch(url, headers=headers, json=data)
    response.raise_for_status()

def para(text):
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": [{"type": "text", "text": {"content": text}}]}
    }

def main():
    content = generate_content()
    date_str = datetime.date.today().strftime("%Y-%m-%d")
    
    heading_map = get_heading_ids()
    print("Found headings:", heading_map)
    
    blocks_politics = [
        para(f"【{date_str}】"),
        para(content['politics_hotspot'])
    ]
    blocks_news = [
        para(content['news_hotspot'])
    ]
    blocks_editing = [
        para(content['editing_task'])
    ]
    blocks_english = [
        para(content['memory_essay'])
    ]
    
    # 根据关键词插入
    mapping = {
        "考研政治热点": blocks_politics,
        "新闻热点": blocks_news,
        "剪辑任务": blocks_editing,
        "英语任务": blocks_english
    }
    
    inserted_any = False
    for key, blocks in mapping.items():
        if key in heading_map:
            insert_after_heading(heading_map[key], blocks)
            inserted_any = True
            print(f"Inserted under {key}")
    
    if not inserted_any:
        # 如果还是找不到，就追加到页面末尾
        url = f"https://api.notion.com/v1/blocks/{NOTION_PAGE_ID}/children"
        headers = {
            "Authorization": f"Bearer {NOTION_TOKEN}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
        all_blocks = [para(f"===== {date_str} =====")]
        all_blocks += blocks_politics + blocks_news + blocks_editing + blocks_english
        data = {"children": all_blocks}
        response = requests.patch(url, headers=headers, json=data)
        response.raise_for_status()
        print("Appended to page end.")

if __name__ == "__main__":
    main()
