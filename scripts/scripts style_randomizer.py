#!/usr/bin/env python3
import random

STYLES = ["复古胶片风", "赛博朋克风", "水墨国风", "像素游戏风"]

def get_random_style():
    return random.choice(STYLES)

if __name__ == "__main__":
    print(get_random_style())