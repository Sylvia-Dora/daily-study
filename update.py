import os
import json
import requests
import datetime
import random

DEEPSEEK_API_KEY = os.environ['DEEPSEEK_API_KEY']

# ========== 全新起点：2026年11月24日 = 第1天 ==========
START_DATE = datetime.date(2026, 11, 24)

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

def generate_all_content(day_number):
    plan = EDITING_PLAN.get(day_number, {"task": "自由复习或练习"})
    today_task = plan["task"]

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
  "long_sentences": [
    {{
      "sentence": "英文原句",
      "structure": "括号法拆解",
      "vocab": "核心生词",
      "translation": "中文翻译"
    }},
    {{
      "sentence": "英文原句",
      "structure": "括号法拆解",
      "vocab": "核心生词",
      "translation": "中文翻译"
    }}
  ]
}}

【长难句要求 - 重要】
1. 每天必须生成 2 句，难度严格对标考研英语（二）阅读真题，不要四六级太简单，也不要英语一那种多层嵌套的变态难。
2. 借鉴田静、刘晓燕的拆句思路：用括号法标出主干和修饰成分，例如「主语[The researchers] 干了什么[found] 了[that...]」。让人一眼看出谁在干什么。
3. 绝对不要出现「定语从句」「状语从句」「非谓语」「宾语从句」等语法术语，全部用大白话描述。比如不要说「这是定语从句修饰前面的名词」，而要说「这一坨是在补充说明前面那个东西」。
4. 每句挑 1-2 个核心生词，格式：英文 词性 中文，例如「sustainable adj. 可持续的」。
5. 中文翻译用大白话，像老师当面讲课，不要机翻腔。
6. 整体控制在手机一屏能看完，不要长篇大论。
7. 句式要覆盖英语二高频考点（修饰后置、插入语、并列结构等），但描述时不许用术语。

【其他要求】
今天是{datetime.date.today().strftime('%Y年%m月%d日')}。
返回纯 JSON，不要 Markdown 代码块。"""

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

    # ===== 长难句渲染 =====
    long_sentences = data.get('long_sentences', [])
    sentences_html = ""
    if long_sentences:
        for i, item in enumerate(long_sentences, 1):
            sentence = html_escape(item.get('sentence', ''))
            structure = html_escape(item.get('structure', ''))
            vocab = html_escape(item.get('vocab', ''))
            translation = html_escape(item.get('translation', ''))
            sentences_html += f"""
            <div style="margin-bottom: 14px; padding-bottom: 12px; border-bottom: 1px dashed #e0d5e8;">
                <div style="font-weight: bold; color: #4a6f8c; margin-bottom: 6px;">第{i}句</div>
                <div style="margin-bottom: 6px;"><b>原句：</b>{sentence}</div>
                <div style="margin-bottom: 6px;"><b>🔍 拆解：</b>{structure}</div>
                <div style="margin-bottom: 6px;"><b>📚 生词：</b>{vocab}</div>
                <div><b>💬 翻译：</b>{translation}</div>
            </div>
            """
        sentences_html = sentences_html.rstrip()
    else:
        sentences_html = '<div style="color:#999;">今日长难句暂未生成，请稍后再试</div>'

    english_html = f"""
    <div class="content-card">
        <div class="section-title">📌 今日单词任务</div>
        <div class="content-text">
✅ 墨墨背单词：<b>80个新词</b><br>
✅ 旧词复习：按墨墨App规划完成<br>
✅ 多邻国：1个小单元打卡
        </div>
    </div>
    <div class="content-card">
        <div class="section-title">📖 今日长难句（2句）</div>
        <div class="content-text">
            {sentences_html}
        </div>
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

    try:
        data = generate_all_content(day_number)
    except Exception as e:
        print(f"DeepSeek 调用失败: {e}")
        quote = random.choice(QUOTES_BACKUP)
        data = {
            "dog_quote": "小狗说：今天没网，但我依然陪你汪！",
            "quote_cn": quote["cn"],
            "quote_en": quote["en"],
            "politics_hotspot": "今日热点暂未更新，请稍后再试",
            "news_hotspot": "今日新闻暂未更新，请稍后再试",
            "editing_task": "请按照大纲自己练习哦",
            "long_sentences": []
        }

    study_html, video_html, english_html, dog_quote = build_html(data, day_number, today_str)

    history[today_str] = {
        "dog_quote": dog_quote,
        "quote_cn": data.get("quote_cn", ""),
        "quote_en": data.get("quote_en", ""),
        "study_html": study_html,
        "video_html": video_html,
        "english_html": english_html
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
