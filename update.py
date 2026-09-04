import os
import json
import requests
import datetime
import random

DEEPSEEK_API_KEY = os.environ['DEEPSEEK_API_KEY']

# 开始日期：2026年9月3日 = 第1天
START_DATE = datetime.date(2026, 9, 3)

# 备用金句库
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
    {"cn": "做你喜欢的事，并把它做好。", "en": "Do what you love, and do it well."},
    {"cn": "一切都会好的，如果不是，那还没到最后。", "en": "Everything will be okay. If not, it's not the end."},
    {"cn": "生活很苦，但你很甜。", "en": "Life is bitter, but you are sweet."},
    {"cn": "少想，多做。", "en": "Think less, do more."},
    {"cn": "坚持就是胜利。", "en": "Perseverance is victory."},
    {"cn": "今天也是闪闪发光的一天。", "en": "Today is also a shining day."},
    {"cn": "与其羡慕别人，不如成为自己。", "en": "Instead of envying others, become yourself."},
    {"cn": "未来可期。", "en": "The future is promising."},
    {"cn": "别让任何人偷走你的梦想。", "en": "Don't let anyone steal your dreams."},
    {"cn": "把日子过成诗。", "en": "Live your life like a poem."}
]

def generate_all_content(day_number):
    """调用 DeepSeek 生成当天所有内容"""
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
  "editing_task": "剪辑学习任务（30天计划第{day_number}天）：PR+剪映双软件学习，具体任务含操作步骤和练习作业，80字内，难度逐步递进，新手友好",
  "memory_essay": "30天趣味记忆第{day_number}篇（英文原文+中文翻译+重点词汇列表，英文约80词，使用红宝书考研词汇）",
  "self_test": "每日自测（3个中译英+3个英译中+2个句子填空，基于当天小作文，用纯文本格式）"
}}
注意：今天是{datetime.date.today().strftime('%Y年%m月%d日')}，考研政治热点请基于当前时政。英文小作文必须明确标注“第{day_number}篇”。self_test 必须返回字符串，不要用嵌套对象。返回纯JSON，不要有其他文字。"""

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
    """转义 HTML 特殊字符，支持 dict/list"""
    if isinstance(text, (dict, list)):
        text = json.dumps(text, ensure_ascii=False)
    elif not isinstance(text, str):
        text = str(text)
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')

def build_html(data, day_number, today_str):
    """构建各页面的 HTML 内容"""
    politics = html_escape(data.get('politics_hotspot', ''))
    news = html_escape(data.get('news_hotspot', ''))
    editing = html_escape(data.get('editing_task', ''))
    essay = html_escape(data.get('memory_essay', ''))
    self_test = html_escape(data.get('self_test', ''))

    # Study 页面
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

    # Video 页面
    video_html = f"""
  <div class="content-card">
        <div class="section-title">🎬 今日剪辑任务（第{day_number}天）</div>
        <div class="content-text">{editing}</div>
    </div>
    <div class="content-card">
        <div class="section-title">📌 30天剪辑学习计划</div>
        <div class="content-text">
✅ PR：剪辑、调色、转场、字幕、导出全流程<br>
✅ 剪映：手机端快速剪辑、热门转场、特效、卡点<br>
✅ 每天一个知识点，30天系统学完
        </div>
    </div>
    """
    # English 页面（包含所有英语任务）
    english_html = f"""
    <div class="content-card">
        <div class="section-title">📌 今日英语任务</div>
        <div class="content-text">
✅ 四级英语：List {day_number}<br>
✅ 考研单词：新60 + 旧100<br>
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
    today_str = today.strftime("%Y-%m-%d")

    # 尝试调用 DeepSeek，失败则使用备用内容
    try:
        data = generate_all_content(day_number)
    except Exception as e:
        print(f"DeepSeek 调用失败: {e}")
        quote = random.choice(QUOTES_BACKUP)
        data = {
            "quote_cn": quote["cn"],
            "quote_en": quote["en"],
            "politics_hotspot": "今日热点暂未更新，请稍后再试",
            "news_hotspot": "今日新闻暂未更新，请稍后再试",
            "editing_task": "今日剪辑任务暂未更新，请稍后再试",
            "memory_essay": f"30天趣味记忆第{day_number}篇暂未更新，请稍后再试",
            "self_test": "今日自测暂未更新，请稍后再试"
        }

    study_html, video_html, english_html, body_html = build_html(data, day_number, today_str)

    # 读取已有的 data.json（如果存在）
    history = {}
    if os.path.exists('data.json'):
        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                old = json.load(f)
                if 'history' in old:
                    history = old['history']
        except Exception as e:
            print(f"读取旧 data.json 失败: {e}")

    # 更新今天的数据
    history[today_str] = {
        "quote_cn": data.get("quote_cn", ""),
        "quote_en": data.get("quote_en", ""),
        "study_html": study_html,
        "video_html": video_html,
        "english_html": english_html,
        "body_html": body_html  # 留空，前端不用
    }

    # 写入 data.json
    output = {
        "history": history,
        "latest": today_str
    }

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"✅ data.json 更新成功！第 {day_number} 天，历史共 {len(history)} 天")

if __name__ == "__main__":
    main()
