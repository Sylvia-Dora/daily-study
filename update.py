import os
import json
import requests
import datetime
import random

DEEPSEEK_API_KEY = os.environ['DEEPSEEK_API_KEY']

# ========== 开始日期：2026年10月9日 = 第1天 ==========
START_DATE = datetime.date(2026, 10, 9)

# ========== 30天剪辑学习大纲（PR + 剪映） ==========
EDITING_PLAN = {
    1:  {"pr": "认识PR界面、新建项目、导入素材", "jianying": "认识剪映界面、导入素材"},
    2:  {"pr": "时间线操作、剪辑片段", "jianying": "分割、删除、拖动片段"},
    3:  {"pr": "导出视频、设置参数", "jianying": "导出视频、选择分辨率"},
    4:  {"pr": "添加背景音乐、调整音量", "jianying": "添加音乐、音频淡入淡出"},
    5:  {"pr": "添加字幕、调整样式", "jianying": "自动识别字幕、改字体"},
    6:  {"pr": "转场效果、简单过渡", "jianying": "转场效果、热门转场"},
    7:  {"pr": "复习+做一条15秒小视频", "jianying": "复习+做一条15秒小视频"},
    8:  {"pr": "基础调色：亮度、对比度、饱和度", "jianying": "滤镜、调节参数"},
    9:  {"pr": "色温、色调、HSL", "jianying": "色彩调节、HSL"},
    10: {"pr": "变速：慢动作、快动作", "jianying": "变速、曲线变速"},
    11: {"pr": "关键帧基础：位置、缩放", "jianying": "关键帧：缩放、移动"},
    12: {"pr": "关键帧进阶：透明度、旋转", "jianying": "关键帧进阶：旋转、不透明度"},
    13: {"pr": "蒙版基础：线性、圆形", "jianying": "蒙版：线性、圆形"},
    14: {"pr": "复习+做一条30秒卡点视频", "jianying": "复习+做一条30秒卡点视频"},
    15: {"pr": "绿幕抠像、超级键", "jianying": "智能抠像、色度抠图"},
    16: {"pr": "画中画、多轨道", "jianying": "画中画、多图层"},
    17: {"pr": "文字动画、字幕特效", "jianying": "文字动画、花字"},
    18: {"pr": "音效添加、音频过渡", "jianying": "音效、变声"},
    19: {"pr": "稳定画面、去抖", "jianying": "防抖、画面稳定"},
    20: {"pr": "速度斜坡、时间重映射", "jianying": "曲线变速进阶"},
    21: {"pr": "复习+做一条带特效的短视频", "jianying": "复习+做一条带特效的短视频"},
    22: {"pr": "分镜脚本、素材整理", "jianying": "分镜脚本、素材整理"},
    23: {"pr": "剪辑节奏、叙事结构", "jianying": "剪辑节奏、卡点"},
    24: {"pr": "调色风格化、LUT", "jianying": "滤镜风格化"},
    25: {"pr": "音频混合、降噪", "jianying": "音频降噪、混音"},
    26: {"pr": "字幕排版、标题设计", "jianying": "字幕排版、封面"},
    27: {"pr": "导出设置、多平台适配", "jianying": "导出、多平台适配"},
    28: {"pr": "做一条1分钟完整视频（上）", "jianying": "做一条1分钟完整视频（上）"},
    29: {"pr": "做一条1分钟完整视频（下）", "jianying": "做一条1分钟完整视频（下）"},
    30: {"pr": "复盘+发布作品", "jianying": "复盘+发布作品"},
}

QUOTES_BACKUP = [
    {"cn": "人生就像一盒巧克力，你永远不知道下一颗是什么味道。", "en": "Life is like a box of chocolates. You never know what you're gonna get."},
    {"cn": "慢慢来，比较快。", "en": "Slow is smooth, smooth is fast."},
    {"cn": "今天不想跑，所以才去跑。", "en": "Run when you don't want to run."},
    {"cn": "种一棵树最好的时间是十年前，其次是现在。", "en": "The best time to plant a tree was 10 years ago. The second best time is now."},
    {"cn": "你比昨天的自己更好了。", "en": "You are better than yesterday's you."},
    {"cn": "所有的伟大都源于一个勇敢的开始。", "en": "All greatness comes from a brave beginning."},
    {"cn": "把每一天都当成最后一天来过。", "en": "Live each day as if it were your last."},
    {"cn": "成功是日复一日的坚持。", "en": "Success is the sum of small efforts repeated daily."},
    {"cn": "不要等到完美再开始。", "en": "Don't wait for perfect. Start now."},
    {"cn": "你走过的每一步都算数。", "en": "Every step you take counts."},
    {"cn": "别怕慢，怕的是站。", "en": "Don't fear being slow, fear standing still."},
    {"cn": "今天的努力是明天的底气。", "en": "Today's effort is tomorrow's confidence."},
    {"cn": "做自己的太阳，不必借谁的光。", "en": "Be your own sun, no need to borrow light."},
    {"cn": "先完成，再完美。", "en": "First done, then perfect."},
    {"cn": "越努力，越幸运。", "en": "The harder you work, the luckier you get."},
    {"cn": "把焦虑变成行动。", "en": "Turn anxiety into action."},
    {"cn": "你只管努力，剩下的交给时间。", "en": "Just keep working hard, leave the rest to time."},
    {"cn": "每一个优秀的人都有一段沉默的时光。", "en": "Every excellent person has a period of silence."},
    {"cn": "心里有光，脚下有路。", "en": "Light in heart, road under feet."},
    {"cn": "不要被明天的烦恼偷走今天的快乐。", "en": "Don't let tomorrow's worries steal today's joy."},
]

def get_recent_vocab(history, today, days=6):
    """获取最近几天用过的重点词汇，用于滚动复习"""
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
    plan = EDITING_PLAN.get(day_number, {"pr": "复习之前内容", "jianying": "复习之前内容"})

    recent_vocab_str = "、".join(recent_vocab[:40]) if recent_vocab else "（无）"

    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    prompt = f"""请生成今日学习内容，返回 JSON 格式，包含以下字段：
{{
  "quote_cn": "一句有哲理或有趣的中文名言/金句（15-30字）",
  "quote_en": "对应的英文翻译",
  "politics_hotspot": "考研政治热点（50字内）",
  "news_hotspot": "新闻热点（50字内）",
  "editing_task_pr": "围绕'{plan['pr']}'这个PR任务，给出具体操作步骤和练习作业，50字内",
  "editing_task_jianying": "围绕'{plan['jianying']}'这个剪映任务，给出具体操作步骤和练习作业，50字内",
  "memory_essay": "30天趣味记忆第{day_number}篇：英文原文约180词 + 中文翻译 + 重点词汇列表（30个），词汇必须来自红宝书考研英语大纲完整词汇库（约5500词），不要只用核心高频词，要涵盖基础词、进阶词、难词",
  "key_vocab": "今天小作文里用到的所有重点词汇，纯英文单词，用JSON数组格式列出，例如：[\\"abandon\\", \\"persistent\\"]",
  "self_test": "每日自测（3个中译英+3个英译中+2个句子填空，基于当天小作文，用纯文本格式）"
}}

【滚动复习要求】
昨天及前几天已经学过的词：{recent_vocab_str}
请从中挑选 5-8 个词，自然融入今天的故事里复现。
其余 22-25 个词用红宝书5500词库里的新词。
总共重点词汇控制在 30 个。

【其他要求】
今天是{datetime.date.today().strftime('%Y年%m月%d日')}，考研政治热点请基于当前时政。
英文小作文必须明确标注"第{day_number}篇"。
self_test 必须是字符串，不要用嵌套对象。
返回纯 JSON，不要有其他文字。"""

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

def html_escape(text):
    if isinstance(text, (dict, list)):
        text = json.dumps(text, ensure_ascii=False)
    elif not isinstance(text, str):
        text = str(text)
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')

def build_html(data, day_number, today_str):
    politics = html_escape(data.get('politics_hotspot', ''))
    news = html_escape(data.get('news_hotspot', ''))
    editing_pr = html_escape(data.get('editing_task_pr', ''))
    editing_jianying = html_escape(data.get('editing_task_jianying', ''))
    essay = html_escape(data.get('memory_essay', ''))
    self_test = html_escape(data.get('self_test', ''))

    plan = EDITING_PLAN.get(day_number, {"pr": "复习", "jianying": "复习"})
    pr_topic = plan['pr']
    jy_topic = plan['jianying']

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
        <div class="section-title">🎬 PR 第{day_number}天：{pr_topic}</div>
        <div class="content-text">{editing_pr}</div>
    </div>
    <div class="content-card">
        <div class="section-title">📱 剪映 第{day_number}天：{jy_topic}</div>
        <div class="content-text">{editing_jianying}</div>
    </div>
    """

    english_html = f"""
    <div class="content-card">
        <div class="section-title">📌 今日英语任务</div>
        <div class="content-text">
✅ 四级英语：List {day_number}<br>
✅ 考研单词：新40 + 旧100<br>
✅ 多邻国：1个小单元打卡
        </div>
    </div>
    <div class="content-card">
        <div class="section-title">📖 30天趣味记忆·第{day_number}篇</div>
        <div class="content-text">{essay}</div>
    </div>
    <div class="content-card">
        <div class="section-title">✅ 每日自测</div>
        <div class="content-text">{self_test}</div>
    </div>
    """

    return study_html, video_html, english_html, ""

def main():
    today = datetime.date.today()
    day_number = (today - START_DATE).days + 1
    if day_number < 1:
        day_number = 1
    if day_number > 30:
        day_number = 30
    today_str = today.strftime("%Y-%m-%d")

    # 先读取历史
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
    print(f"最近词汇池大小: {len(recent_vocab)}")

    try:
        data = generate_all_content(day_number, recent_vocab)
    except Exception as e:
        print(f"DeepSeek 调用失败: {e}")
        quote = random.choice(QUOTES_BACKUP)
        plan = EDITING_PLAN.get(day_number, {"pr": "复习", "jianying": "复习"})
        data = {
            "quote_cn": quote["cn"],
            "quote_en": quote["en"],
            "politics_hotspot": "今日热点暂未更新，请稍后再试",
            "news_hotspot": "今日新闻暂未更新，请稍后再试",
            "editing_task_pr": f"今日任务：{plan['pr']}，请打开PR练习",
            "editing_task_jianying": f"今日任务：{plan['jianying']}，请打开剪映练习",
            "memory_essay": f"30天趣味记忆第{day_number}篇暂未更新，请稍后再试",
            "key_vocab": [],
            "self_test": "今日自测暂未更新，请稍后再试"
        }

    study_html, video_html, english_html, body_html = build_html(data, day_number, today_str)

    key_vocab = data.get("key_vocab", [])
    if isinstance(key_vocab, str):
        try:
            key_vocab = json.loads(key_vocab)
        except:
            key_vocab = []

    history[today_str] = {
        "quote_cn": data.get("quote_cn", ""),
        "quote_en": data.get("quote_en", ""),
        "study_html": study_html,
        "video_html": video_html,
        "english_html": english_html,
        "body_html": body_html,
        "key_vocab": key_vocab
    }

    output = {
        "history": history,
        "latest": today_str
    }

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"✅ data.json 更新成功！第 {day_number} 天，历史共 {len(history)} 天，今日词汇 {len(key_vocab)} 个")

if __name__ == "__main__":
    main()
