#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
杭电印迹 · AI 文创盲盒生成器 (CLI 版)
基于原有 collection_tracker 扩展：交互、图片生成、用户画像持久化
"""

import json
import sys
import os
import random
import re
import time
import requests
import webbrowser
from pathlib import Path
from datetime import datetime

# ==================== 原有配置（保持不变） ====================
STYLES = ["复古胶片风", "赛博朋克风", "水墨国风", "像素游戏风"]
TRACKER_FILE = "/tmp/hdu_collection.json"  # Linux/Mac 临时文件，Windows下会转为用户目录
# 为了跨平台，改为用户目录下的隐藏文件
HOME = Path.home()
TRACKER_FILE = HOME / ".hdu_creative_profile.json"

# ==================== API 配置（可选） ====================
# 如果你有阿里云 DashScope API Key，填写在这里
DASHSCOPE_API_KEY = None  # 例如 "sk-xxxx"
# 降级图片（网络示例图）
FALLBACK_IMAGES = {
    "复古胶片风": "https://picsum.photos/id/20/1024/768",
    "赛博朋克风": "https://picsum.photos/id/4/1024/768",
    "水墨国风": "https://picsum.photos/id/96/1024/768",
    "像素游戏风": "https://picsum.photos/id/179/1024/768",
}
LOCAL_FALLBACK_DIR = HOME / ".hdu_fallback"
LOCAL_FALLBACK_DIR.mkdir(exist_ok=True)


# ==================== 原有函数（修改以适应新数据结构） ====================
def load_tracker(session_id="default"):
    """加载用户画像（兼容旧格式，但扩展了字段）"""
    if not TRACKER_FILE.exists():
        return {
            "collected": [],
            "achievements": [],
            "preferences": {s: 0 for s in STYLES},
            "recent_generations": []
        }
    with open(TRACKER_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # 兼容旧数据：如果没有 preferences 字段则添加
    if "preferences" not in data:
        data["preferences"] = {s: 0 for s in STYLES}
    if "achievements" not in data:
        data["achievements"] = []
    if "recent_generations" not in data:
        data["recent_generations"] = []
    return data


def save_tracker(tracker, session_id="default"):
    """保存用户画像"""
    with open(TRACKER_FILE, 'w', encoding='utf-8') as f:
        json.dump(tracker, f, indent=2, ensure_ascii=False)


def update_collection(tracker, new_style):
    """更新收集列表（原有逻辑增强成就检测）"""
    collected = tracker.get("collected", [])
    achievements = tracker.get("achievements", [])
    if new_style not in collected:
        collected.append(new_style)
        tracker["collected"] = collected
        progress = len(collected)
        if progress == len(STYLES):
            if "文创大师" not in achievements:
                achievements.append("文创大师")
                print(f"\n🎉 隐藏款解锁！集齐了所有风格：{', '.join(collected)}。获得成就【文创大师】")
        else:
            print(f"\n✨ 获得「{new_style}」图鉴！({progress}/{len(STYLES)})")
    else:
        print(f"\n「{new_style}」已集齐，再试试其他风格吧。")
    tracker["achievements"] = achievements
    return tracker


# ==================== 新增：情感与实体识别 ====================
def simple_emotion_analysis(text):
    text = text.lower()
    if any(w in text for w in ["兴奋", "激动", "开心", "high", "excited"]):
        return "兴奋"
    if any(w in text for w in ["疲惫", "累", "困", "tired"]):
        return "疲惫"
    if any(w in text for w in ["怀旧", "回忆", "曾经", "nostalgic"]):
        return "怀旧"
    if any(w in text for w in ["焦虑", "担心", "烦", "anxious"]):
        return "焦虑"
    return "平静"


def extract_scene(text):
    """简单清理，提取场景主体"""
    cleaned = re.sub(r"[嗯啊哦呃嘛啦哈]", "", text)
    return cleaned.strip()


# ==================== 新增：风格选择（加权随机） ====================
def select_style(tracker, emotion):
    collected = tracker.get("collected", [])
    preferences = tracker.get("preferences", {s: 0 for s in STYLES})
    weights = []
    for s in STYLES:
        base = 0.3 if s in collected else 1.0
        pref = preferences.get(s, 0)
        if pref > 0:
            base += 0.5
        elif pref < 0:
            base -= 0.8
        # 情感修正
        if emotion == "兴奋" and s == "赛博朋克风":
            base *= 1.5
        elif emotion == "疲惫" and s == "水墨国风":
            base *= 1.3
        elif emotion == "怀旧" and s == "复古胶片风":
            base *= 1.6
        elif emotion == "焦虑" and s == "像素游戏风":
            base *= 1.2
        weights.append(max(0.1, base))
    return random.choices(STYLES, weights=weights, k=1)[0]


# ==================== 新增：图像生成（API + 降级） ====================
def generate_image(prompt, style):
    """调用通义万相 API，失败则使用本地/网络降级图"""
    if DASHSCOPE_API_KEY:
        url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis"
        headers = {"Authorization": f"Bearer {DASHSCOPE_API_KEY}", "Content-Type": "application/json"}
        data = {"model": "wanx-v1", "input": {"prompt": prompt}, "parameters": {"size": "1024*1024", "n": 1}}
        try:
            resp = requests.post(url, headers=headers, json=data, timeout=30)
            if resp.status_code == 200:
                result = resp.json()
                img_url = result["output"]["results"][0]["url"]
                img_data = requests.get(img_url).content
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                save_path = Path.cwd() / f"hdu_{timestamp}_{style}.png"
                with open(save_path, "wb") as f:
                    f.write(img_data)
                return str(save_path)
            else:
                print(f"⚠️ API 失败 ({resp.status_code})，使用降级图片")
        except Exception as e:
            print(f"⚠️ 生成异常: {e}，使用降级图片")
    # 降级：尝试本地缓存或网络示例
    local_path = LOCAL_FALLBACK_DIR / f"{style}.jpg"
    if not local_path.exists():
        try:
            img_url = FALLBACK_IMAGES.get(style, "https://picsum.photos/id/0/1024/768")
            resp = requests.get(img_url, timeout=5)
            if resp.status_code == 200:
                with open(local_path, "wb") as f:
                    f.write(resp.content)
            else:
                # 生成纯色图（需要 PIL，如果没有则跳过）
                try:
                    from PIL import Image
                    img = Image.new('RGB', (1024, 768), color=(73, 109, 137))
                    img.save(local_path)
                except ImportError:
                    return f"无法生成图片，请检查网络或安装 PIL"
        except:
            return f"无法获取图片: {style}"
    return str(local_path)


# ==================== 新增：文案生成 ====================
def generate_caption(scene, style, emotion):
    templates = {
        "复古胶片风": {"怀旧": f"时光定格在{scene}，每一帧都是杭电的青春。", "默认": f"{scene}，如同老照片里的温度。"},
        "赛博朋克风": {"兴奋": f"bug退散，{scene}！杭电之光永不熄灭。", "默认": f"{scene}的霓虹灯下，代码在呼吸。"},
        "水墨国风": {"疲惫": f"{scene}，让墨色洗去一天的疲惫。", "默认": f"{scene}，水墨晕染，心随山远。"},
        "像素游戏风": {"焦虑": f"{scene}，像游戏一样，总能通关。", "默认": f"{scene}，像素块里的杭电记忆。"}
    }
    tpl = templates.get(style, {}).get(emotion, templates.get(style, {}).get("默认", f"✨ {scene}，杭电印迹为你记录。"))
    return tpl


# ==================== 主交互（整合原有风格收集器） ====================
def main():
    print("\n🎨 杭电印迹 · AI 文创盲盒生成器 (终端版)")
    print("输入校园场景描述，或命令: /stats, /reset, /exit")
    tracker = load_tracker()

    while True:
        user_input = input("\n> ").strip()
        if not user_input:
            continue
        if user_input.lower() in ["/exit", "/quit", "exit"]:
            break
        elif user_input == "/stats":
            col = tracker.get("collected", [])
            ach = tracker.get("achievements", [])
            print(f"📊 已收集风格: {col if col else '无'}")
            print(f"🏅 成就: {ach if ach else '无'}")
            continue
        elif user_input == "/reset":
            tracker = {
                "collected": [],
                "achievements": [],
                "preferences": {s: 0 for s in STYLES},
                "recent_generations": []
            }
            save_tracker(tracker)
            print("✅ 进度已重置")
            continue

        # 正常生成流程
        print("🤖 正在理解场景...")
        scene = extract_scene(user_input)
        emotion = simple_emotion_analysis(user_input)
        print(f"📊 情绪: {emotion} | 场景: {scene}")

        style = select_style(tracker, emotion)
        print(f"🎨 选择风格: {style}")

        # 构建提示词（简单但有效）
        prompt = f"{scene}, {style}, HDU campus, high quality"
        print("🖼️ 生成图像中（可能需要10秒）...")
        image_path = generate_image(prompt, style)

        caption = generate_caption(scene, style, emotion)

        # 更新收集进度（调用原有逻辑）
        tracker = update_collection(tracker, style)
        # 保存偏好（本示例未实现赞/踩，可以后续扩展）
        save_tracker(tracker)

        # 输出结果
        print("\n" + "=" * 50)
        print(f"🎨 风格：{style}")
        print(f"📝 {caption}")
        if image_path and os.path.exists(image_path):
            print(f"🖼️ 图片保存：{image_path}")
            try:
                os.startfile(image_path)  # Windows 打开图片
            except:
                webbrowser.open(f"file://{os.path.abspath(image_path)}")
        else:
            print(f"🖼️ 图片地址：{image_path}")
        # 进度条
        collected = len(tracker["collected"])
        bar = "█" * collected + "░" * (len(STYLES) - collected)
        print(f"📊 集卡进度：{bar} {collected}/{len(STYLES)}")
        if tracker["achievements"]:
            print(f"🏅 成就：{', '.join(tracker['achievements'])}")
        print("=" * 50)


if __name__ == "__main__":
    main()