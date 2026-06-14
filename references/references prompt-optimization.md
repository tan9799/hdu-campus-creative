# 各风格绘图提示词优化关键词库 v2

## 通用负面提示词
`no text, no watermark, no signature, no low quality, no deformed hands, no extra limbs, no blurry, no distorted faces`

## 通用正面水印规范（v5新增）
- 所有生成图右下角添加半透明 `© HDU Creative Lab` 文字水印，字号为图片宽度的2%。
- 可选添加杭电校徽轮廓（灰度，透明度30%）。

## 复古胶片风
### 正向关键词
`vintage film, warm orange and brown tones, light leaks, analog grain, 35mm photo, shallow depth of field, nostalgic atmosphere, soft focus, Kodak Portra 400, slight vignette`

### 强制杭电元素
- 画面中出现“HDU”手写字体或校徽轮廓（例如在老式笔记本上）。
- 背景包含月雅湖的模糊轮廓或图书馆的剪影。

## 赛博朋克风
### 正向关键词
`cyberpunk, neon glow, blade runner aesthetic, holographic elements, purple and cyan, rain-soaked streets, high contrast, digital art, futuristic city, volumetric lighting, holographic billboards`

### 强制杭电元素
- 背景墙面有“HDU Lab”霓虹灯字样。
- 全息投影显示杭电校训“笃学力行，守正求新”（中文或英文）。

## 水墨国风
### 正向关键词
`ink wash painting, traditional Chinese brush strokes, black ink and light ochre, rice paper texture, misty mountains, minimalist composition, negative space, calligraphy elements, wet ink bleeding`

### 强制杭电元素
- 画面上方题写“月雅湖”或“杭电”小字（毛笔书法）。
- 山石形状隐约呈现杭电体育馆或问鼎广场的剪影。

## 像素游戏风
### 正向关键词
`pixel art, 8-bit, retro game aesthetic, blocky pixels, limited color palette (16 colors), chunky clouds, simple shapes, nostalgic gameboy style, dithering, sprite-based`

### 强制杭电元素
- 像素角色穿着印有“HDU”字样的T恤或帽子。
- 背景像素云朵组成“HDU”字母，或像素风格校训横幅。

## 提示词构造公式（强制顺序）
`[主体] + [动作/状态] + [强制杭电元素] + [光线/天气/时间] + [色彩倾向] + [风格关键词] + [艺术媒介/质感] + [水印约束] + [负面提示词]`

## 风格融合（v5实验性）
当用户要求“混合两种风格”时（如“复古+赛博朋克”），关键词合并，权重各50%，并在末尾添加 `mixed style, eclectic`。示例输出提示词：`"library interior with warm sunset light, neon holographic clock, retro film grain over cyberpunk neon, eclectic art"`。