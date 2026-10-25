import os
import json
import requests
import datetime
import random

DEEPSEEK_API_KEY = os.environ['DEEPSEEK_API_KEY']

# ========== 全新起点：2026年10月27日 = 第1天 ==========
START_DATE = datetime.date(2026, 10, 27)

# ========== 30天剪辑基础双修大纲 ==========
EDITING_PLAN = {
    1:  {"task": "PR：看岁岁认识界面/建项目；剪映：看陆一舟认识界面/导入素材"},
    2:  {"task": "PR：学剃刀(C)和选择(V)；剪映：练分割、删除"},
    3:  {"task": "PR：学时间轴缩放/波纹删除；剪映：练音频分离/裁剪"},
    4:  {"task": "PR：学基础字幕添加；剪映：实操一键识别字幕"},
    5:  {"task": "PR：学基础导出参数；剪映：学高清导出"},
    6:  {"task": "【实操日】随便拍5段视频，用PR和剪映各剪一个15秒流水账"},
    7:  {"task": "【复盘日】不看教程，盲操切、拖、导出，记下不熟的快捷键"},
    8:  {"task": "PR：看岁岁学关键帧；剪映：看陆一舟学关键帧"},
    9:  {"task": "PR：学线性蒙版；剪映：学蒙版遮罩"},
    10: {"task": "PR：学变速(时间重映射)；剪映：学常规/曲线变速"},
    11: {"task": "PR：学加音效/背景音乐；剪映：学音乐自动踩点"},
    12: {"task": "PR：学画中画/多轨道；剪映：学画中画/图层顺序"},
    13: {"task": "【实操日】用关键帧+变速，剪一个15秒卡点视频"},
    14: {"task": "【复盘日】找3个短视频，看前10秒怎么切的，模仿一下"},
    15: {"task": "PR：看岁岁学文字排版；剪映：学花字和文字动画"},
    16: {"task": "PR：学画面防抖；剪映：学基础防抖/画面裁剪"},
    17: {"task": "PR专项：看【我是阿B】学基础调色(Lumetri面板)"},
    18: {"task": "PR专项：看【我是阿B】学HSL/色温，把素材调通透"},
    19: {"task": "剪映实战：套用滤镜，调一个日常Vlog色调"},
    20: {"task": "【实操日】拿废片，用PR按阿B的方法调出质感"},
    21: {"task": "【复盘日】总结调色参数，对比大佬的差在哪"},
    22: {"task": "PR专项：看【百万剪辑狮】讲视频节奏与镜头组接"},
    23: {"task": "PR专项：看【百万剪辑狮】讲音乐卡点逻辑"},
    24: {"task": "PR实战：找5段素材+音乐，按剪辑狮思路做粗剪"},
    25: {"task": "PR实战：精剪，用学过的调色和字幕包装"},
    26: {"task": "剪映实战：同主题，用手机剪映快速剪竖屏版本"},
    27: {"task": "【实操日】独立完成1分钟Vlog，加音效/字幕/调色"},
    28: {"task": "【修改日】导出看三遍，找毛病，回软件修改"},
    29: {"task": "【复习日】把前三周卡壳的地方，回岁岁/陆一舟课里重看"},
    30: {"task": "【产出日】导出最终成片，发到社交平台，基础通关！"}
}

QUOTES_BACKUP = [
    {"cn": "慢慢来，比较快。", "en": "Slow is smooth, smooth is fast."},
    {"cn": "不要等到完美再开始。", "en": "Don't wait for perfect. Start now."},
    {"cn": "种一棵树最好的时间是十年前，其次是现在。", "en": "The best time to plant a tree was 10 years ago. The second best time is now."}
]

def get_recent_vocab(history, today, days=6):
    vocab_pool = []
    for i in range(1, days + 1):
        date = today - datetime.timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        if date_str in history:
            vocab_list = history[date_str].get('key_vocab', [])
            vocab_pool.extend(vocab_list)
    seen = set()
    unique = []
    for w in vocab_pool:
        w_lower = w.lower()
        if w_lower not in seen:
            seen.add(w_lower)
            unique.append(w)
    return unique

def generate_all_content(day_number, recent_vocab):
    plan = EDITING_PLAN.get(day_number, {"task": "自由复习或练习"})
    today_task = plan["task"]
    recent_vocab_str = "、".join(recent_vocab[:40]) if recent_vocab else "（无）"

    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""请生成今日学习内容，返回 JSON 格式，包含以下字段：
{{
  "dog_quote": "一句小狗对主人的可爱、幽默或鼓励的碎碎念，15字左右，例如：今天剪辑课也要乖乖看汪！",
  "quote_cn": "一句有哲理或有趣的中文名言/金句（15-30字）",
  "quote_en": "对应的英文翻译",
  "politics_hotspot": "考研政治热点（50字内）",
  "news_hotspot": "新闻热点（50字内）",
  "editing_task": "今天的核心任务是：{today_task}。请用鼓励的语气，写一句简短的今日剪辑行动建议（30字内）",
  "memory_essay": "30天趣味记忆第{day_number}篇：英文原文约100-120词 + 中文翻译 + 重点词汇表（15-20个，必须带中文意思，格式：单词 - 中文意思）。并在最后加一句：💡读一读培养语感即可，重点记词汇意思，不用死背全文。",
  "key_vocab": "今天小作文里用到的所有重点词汇，纯英文单词，用JSON数组格式列出，例如：[\\"abandon\\", \\"persistent\\"]",
  "self_test": "每日自测：基于今天小作文的语境，出5道单词测试（3道中译英，2道英译中）+ 1个句子填空，用纯文本格式。"
}}

【强制性要求：更换小作文主题】
请务必为今天的第{day_number}篇小作文选择一个**全新的话题**（如：人工智能、环境保护、职场沟通、旅行见闻、健康饮食等），**绝对禁止**与前几天的故事内容、句式结构雷同！

【滚动复习要求】
昨天及前几天已经学过的词汇：{recent_vocab_str}
请从中挑选 3-5 个词，自然融入今天的故事里复现。其余用考研核心词汇。

【其他要求】
今天是{datetime.date.today().strftime('%Y年%m月%d日')}。
self_test 必须是字符串。
返回纯 JSON。"""

    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.9
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    content = result['choices'][0]['message']['content']
    content = content.strip()
    if content.startswith("```"):
        content = content.split('\n', 1)[1].rsplit('```', 1)[0]
    return json.loads(content)

def html_escape(text):
    if isinstance(text, (dict, list)):
        text = json.dumps(text, ensure_ascii=False)
    elif not isinstance(text, str):
        text = str(text)
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')

def build_html(data, day_number, today_str):
    politics = html_escape(data.get('politics_hotspot', ''))
    news = html_escape(data.get('news_hotspot', ''))
    editing_task = html_escape(data.get('editing_task', ''))
    essay = html_escape(data.get('memory_essay', ''))
    self_test = html_escape(data.get('self_test', ''))
    dog_quote = html_escape(data.get('dog_quote', '今天也要加油汪！'))

    plan = EDITING_PLAN.get(day_number, {"task": "自由练习"})
    today_task_name = plan["task"]

    study_html = f"""
    <div class="content-card">
        <div class="section-title">🔥 考研政治热点</div>
        <div class="content-text">{politics}</div>
    </div>
    <div class="content-card">
        <div class="section-title">📰 新闻热点</div>
        <div class="content-text">{news}</div>
    </div>
    """

    video_html = f"""
    <div class="content-card">
        <div class="section-title">🎬 今日剪辑任务 (第{day_number}天)</div>
        <div class="content-text" style="font-weight: bold; color: #4a6f8c; margin-bottom: 8px;">{today_task_name}</div>
        <div class="content-text">{editing_task}</div>
        <div style="margin-top: 10px; padding-top: 8px; border-top: 1px dashed #ccc; font-size: 12px; color: #888;">
            💡 找课指南：B站搜 UP主 <b>岁岁的剪辑手册</b> (PR) / <b>陆一舟剪辑</b> (剪映) / <b>我是阿B</b> (调色) / <b>百万剪辑狮</b> (节奏)。
        </div>
    </div>
    """

    english_html = f"""
    <div class="content-card">
        <div class="section-title">📌 今日单词任务</div>
        <div class="content-text">
✅ 四级新词：20 个 <b>(奶酪背单词)</b><br>
✅ 考研单词：<b>炭炭40 + 墨墨40</b><br>
✅ 旧词复习：按各自App规划完成<br>
✅ 多邻国：1个小单元打卡<br>
<span style="color: #888; font-size: 12px;">（每日新词总计 100 个，小作文当作语感辅助）</span>
        </div>
    </div>
    <div class="content-card">
        <div class="section-title">📖 30天趣味记忆·第{day_number}篇</div>
        <div class="content-text">{essay}</div>
    </div>
    <div class="content-card">
        <div class="section-title">✅ 每日自测与复习</div>
        <div class="content-text">{self_test}</div>
    </div>
    """

    return study_html, video_html, english_html, dog_quote

def main():
    today = datetime.date.today()
    day_number = (today - START_DATE).days + 1
    if day_number < 1:
        day_number = 1
    if day_number > 30:
        day_number = 30
    today_str = today.strftime("%Y-%m-%d")

    history = {}
    if os.path.exists('data.json'):
        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                old = json.load(f)
                if 'history' in old:
                    history = old['history']
        except Exception as e:
            print(f"读取旧 data.json 失败: {e}")

    recent_vocab = get_recent_vocab(history, today, days=6)

    try:
        data = generate_all_content(day_number, recent_vocab)
    except Exception as e:
        print(f"DeepSeek 调用失败: {e}")
        quote = random.choice(QUOTES_BACKUP)
        plan = EDITING_PLAN.get(day_number, {"task": "复习"})
        data = {
            "dog_quote": "小狗说：今天没网，但我依然陪你汪！",
            "quote_cn": quote["cn"],
            "quote_en": quote["en"],
            "politics_hotspot": "今日热点暂未更新，请稍后再试",
            "news_hotspot": "今日新闻暂未更新，请稍后再试",
            "editing_task": "请按照大纲自己练习哦",
            "memory_essay": f"30天趣味记忆第{day_number}篇暂未更新，请稍后再试",
            "key_vocab": [],
            "self_test": "今日自测暂未更新，请稍后再试"
        }

    study_html, video_html, english_html, dog_quote = build_html(data, day_number, today_str)

    key_vocab = data.get("key_vocab", [])
    if isinstance(key_vocab, str):
        try:
            key_vocab = json.loads(key_vocab)
        except:
            key_vocab = []

    history[today_str] = {
        "dog_quote": dog_quote,
        "quote_cn": data.get("quote_cn", ""),
        "quote_en": data.get("quote_en", ""),
        "study_html": study_html,
        "video_html": video_html,
        "english_html": english_html,
        "key_vocab": key_vocab
    }

    output = {
        "history": history,
        "latest": today_str
    }

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"✅ data.json 更新成功！第 {day_number} 天，历史共 {len(history)} 天")

if __name__ == "__main__":
    main()
