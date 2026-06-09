# HTML动画展示片创建指南

用于创建律师形象展示片、产品演示、服务介绍等动画HTML文件。

## 适用场景

- 律师个人形象展示片
- 服务领域介绍动画
- 成功案例展示视频
- 社交媒体短视频素材
- 网站首页背景动画

## 技术架构

### 核心技术栈
- **HTML5**：结构层
- **CSS3**：动画层（关键帧、过渡、变换）
- **JavaScript**：交互层（播放控制、场景切换）

### 文件结构
```
showcase.html
├── <style>        # CSS动画样式
├── <body>         # HTML场景结构
└── <script>       # JavaScript交互逻辑
```

## 标准分镜结构（6幕）

### 第1幕：开场（5-10秒）
- **视觉元素**：品牌标识、主题动画
- **文案**：一句话定位（如"跨境法律，专业护航"）
- **动画**：渐显、缩放、旋转

### 第2幕：专业资质（10-15秒）
- **视觉元素**：律师照片、简介
- **文案**：姓名、头衔、核心优势
- **动画**：滑入、淡入

### 第3幕：服务领域（15-20秒）
- **视觉元素**：服务卡片（3-4个）
- **文案**：服务名称、简要描述
- **动画**：卡片依次出现

### 第4幕：团队优势（10-15秒）
- **视觉元素**：图标+文字
- **文案**：核心优势（3个）
- **动画**：图标弹跳、文字渐显

### 第5幕：成功案例/数据（10-15秒）
- **视觉元素**：数据可视化
- **文案**：关键数据（客户数、交易额、胜诉率）
- **动画**：数字滚动、进度条增长

### 第6幕：结尾（10-15秒）
- **视觉元素**：联系方式、二维码
- **文案**：行动号召（CTA）
- **动画**：渐隐、聚焦

## CSS动画模板

### 关键帧动画
```css
/* 淡入上移 */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* 缩放弹跳 */
@keyframes scaleBounce {
    0% { transform: scale(0); }
    50% { transform: scale(1.1); }
    100% { transform: scale(1); }
}

/* 旋转 */
@keyframes rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}
```

### 场景过渡
```css
.scene {
    position: absolute;
    opacity: 0;
    transition: opacity 1s ease;
}

.scene.active {
    opacity: 1;
}
```

## JavaScript交互控制

### 播放控制
```javascript
let currentScene = 1;
const totalScenes = 6;
let autoPlayInterval = null;

function showScene(sceneNumber) {
    document.querySelectorAll('.scene').forEach(scene => {
        scene.classList.remove('active');
    });
    document.getElementById(`scene${sceneNumber}`).classList.add('active');
    currentScene = sceneNumber;
}

function nextScene() {
    const next = currentScene >= totalScenes ? 1 : currentScene + 1;
    showScene(next);
}

function toggleAutoPlay() {
    if (autoPlayInterval) {
        clearInterval(autoPlayInterval);
        autoPlayInterval = null;
    } else {
        autoPlayInterval = setInterval(nextScene, 5000);
    }
}
```

### 键盘控制
```javascript
document.addEventListener('keydown', (e) => {
    switch(e.key) {
        case 'ArrowRight':
        case ' ':
            nextScene();
            break;
        case 'ArrowLeft':
            prevScene();
            break;
    }
});
```

## 导出为MP4视频

### 方法1：屏幕录制（简单但质量依赖屏幕）
1. 浏览器打开HTML文件
2. 点击"自动播放"
3. 使用录屏软件：
   - **Mac**：QuickTime Player（文件→新建屏幕录制）
   - **Windows**：Xbox Game Bar（Win+G）
   - **跨平台**：OBS Studio（免费，推荐高质量预设）
4. 录制完整时长，导出为MP4

### 方法2：自动化导出 puppeteer-core + ffmpeg ★推荐

无需手动录屏，Chrome无头模式逐帧截图 + ffmpeg编码，全程自动化。

**前置条件**：
```bash
# Google Chrome 已安装（macOS默认路径）
# ffmpeg 已安装
npm install -g puppeteer-core
```

**完整脚本**（保存为 `/tmp/capture-html-video.js`）：

```javascript
const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');

const FRAME_DIR = '/tmp/html-frames';
const FPS = 24;
const SCENE_DURATION = 5; // 每幕秒数，根据HTML中的setInterval调整
const TOTAL_SCENES = 6;   // 场景总数
const WIDTH = 1920;
const HEIGHT = 1080;

// ★ page.waitForTimeout 已废弃，必须用这个替代
const sleep = ms => new Promise(r => setTimeout(r, ms));

async function main() {
    if (fs.existsSync(FRAME_DIR)) fs.rmSync(FRAME_DIR, { recursive: true });
    fs.mkdirSync(FRAME_DIR, { recursive: true });

    const browser = await puppeteer.launch({
        executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage',
               `--window-size=${WIDTH},${HEIGHT}`]
    });

    const page = await browser.newPage();
    await page.setViewport({ width: WIDTH, height: HEIGHT });

    // 加载HTML文件（修改为实际路径）
    const htmlPath = path.resolve('/Users/yuzhenghong/Desktop/涉外律师形象展示片.html');
    await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle0', timeout: 30000 });
    await sleep(1000);

    // ★ 必须隐藏控制栏，否则会出现在视频中
    await page.evaluate(() => {
        const c = document.querySelector('.controls');
        if (c) c.style.display = 'none';
        const p = document.querySelector('.progress-bar-container');
        if (p) p.style.display = 'none';
    });

    let frameIndex = 0;
    const frameInterval = Math.round(1000 / FPS);

    for (let scene = 1; scene <= TOTAL_SCENES; scene++) {
        // 切换到指定场景
        await page.evaluate((sn) => {
            document.querySelectorAll('.scene').forEach(s => s.classList.remove('active'));
            const t = document.getElementById(`scene${sn}`);
            if (t) t.classList.add('active');
        }, scene);

        // ★ 等待CSS opacity过渡完成（1s + 缓冲）
        await sleep(1200);

        const framesPerScene = SCENE_DURATION * FPS;
        const capturedStart = Math.round(1.2 * FPS); // 跳过过渡期

        for (let f = capturedStart; f < framesPerScene; f++) {
            const framePath = path.join(FRAME_DIR, `frame_${String(frameIndex).padStart(5, '0')}.png`);
            await page.screenshot({ path: framePath, type: 'png' });
            frameIndex++;
            if (f < framesPerScene - 1) await sleep(frameInterval);
        }
        console.log(`Scene ${scene}/${TOTAL_SCENES} done, frames: ${frameIndex}`);
    }

    // ★ 回填过渡期的帧（复制该场景第一帧，保证帧序列连续）
    let fillFrame = 0;
    for (let scene = 1; scene <= TOTAL_SCENES; scene++) {
        const firstCaptured = fillFrame + Math.round(1.2 * FPS);
        const srcPath = path.join(FRAME_DIR, `frame_${String(firstCaptured).padStart(5, '0')}.png`);
        for (let f = fillFrame; f < firstCaptured; f++) {
            const fp = path.join(FRAME_DIR, `frame_${String(f).padStart(5, '0')}.png`);
            if (!fs.existsSync(fp) && fs.existsSync(srcPath)) {
                fs.copyFileSync(srcPath, fp);
            }
        }
        fillFrame += SCENE_DURATION * FPS;
    }

    console.log(`Total frames: ${frameIndex}`);
    await browser.close();
}
main().catch(err => { console.error(err); process.exit(1); });
```

**执行命令**：
```bash
# 1. 运行截图脚本
NODE_PATH=/Users/yuzhenghong/.local/lib/node_modules node /tmp/capture-html-video.js

# 2. 重命名帧文件（确保连续编号）
cd /tmp/html-frames && i=0; for f in $(ls frame_*.png | sort); do
  newname=$(printf "frame_%05d.png" $i)
  [ "$f" != "$newname" ] && mv "$f" "$newname"
  i=$((i+1))
done

# 3. ffmpeg编码为MP4
ffmpeg -y -framerate 24 -i /tmp/html-frames/frame_%05d.png \
  -c:v libx264 -pix_fmt yuv420p -preset medium -crf 18 \
  -vf "scale=1920:1080" ~/Desktop/涉外律师形象展示片.mp4

# 4. 清理临时文件
rm -rf /tmp/html-frames /tmp/capture-html-video.js
```

### ⚠️ 关键Pitfall

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| `page.waitForTimeout is not a function` | 新版puppeteer-core已废弃此方法 | 用 `const sleep = ms => new Promise(r => setTimeout(r, ms))` 替代 |
| 视频中出现控制按钮 | `.controls` div未隐藏 | 截图前用 `page.evaluate` 设置 `display:none` |
| 场景切换时画面半透明 | CSS opacity过渡1秒，截图抓到中间状态 | 先 `await sleep(1200)` 等过渡完成再截图 |
| ffmpeg报错找不到帧文件 | 帧编号不连续（有跳号） | 回填过渡期帧 + 重新编号为连续序列 |
| `ffprobe: command not found` | ffprobe可能未安装或不在PATH | 用 `ffmpeg -i file.mp4` 代替查看视频信息 |
| NODE_PATH找不到模块 | 全局npm模块路径未设置 | 运行时加 `NODE_PATH=/Users/yuzhenghong/.local/lib/node_modules` |
| 截图太暗/太亮 | 无头模式渲染差异 | 在Chrome args中加 `--force-device-scale-factor=1` |

### 输出规格

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| 分辨率 | 1920×1080 | 与HTML viewport一致 |
| 帧率 | 24fps | 电影标准，文件小 |
| 编码 | H.264 (libx264) | 兼容性最好 |
| 画质 | CRF 18 | 18-23为高质量区间 |
| 预设 | medium | 平衡编码速度和画质 |
| 6幕×5秒 | ~22秒，约900KB | 可调整SCENE_DURATION |

### 如何添加背景音乐到MP4

```bash
# 下载背景音乐（如Pixabay免费音乐）
curl -o /tmp/bgm.mp3 "https://cdn.pixabay.com/audio/2024/11/29/audio_d5470ad553.mp3"

# 合并音视频
ffmpeg -y -i ~/Desktop/output.mp4 -i /tmp/bgm.mp3 \
  -c:v copy -c:a aac -shortest ~/Desktop/output_with_music.mp4
```

## 设计规范

### 颜色方案
```css
:root {
    --primary: #1a365d;      /* 深蓝：专业 */
    --primary-light: #2d3748; /* 浅蓝 */
    --accent: #ffd700;        /* 金色：高端 */
    --text: #ffffff;          /* 白色文字 */
    --bg-dark: #0a1628;       /* 深色背景 */
}
```

### 字体选择
```css
font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
```

### 动画时长
- 场景切换：1秒
- 元素动画：0.5-1秒
- 自动播放间隔：5秒

## 常见问题

### Q1：如何调整动画速度？
修改CSS中的`transition`和`animation`时长，或JavaScript中的`setInterval`间隔。同步修改脚本中的`SCENE_DURATION`。

### Q2：如何添加背景音乐？
HTML中嵌入`<audio>`标签，导出MP4时用ffmpeg合并音视频（见上方命令）。

### Q3：如何修改场景数量？
1. 添加新的`.scene` HTML结构
2. 更新`totalScenes`变量
3. 同步修改脚本中的`TOTAL_SCENES`

### Q4：如何导出高清视频？
- 方法1：录屏时设置分辨率为1920×1080
- 方法2：自动化脚本中`WIDTH`/`HEIGHT`设为1920×1080，CRF设为18

### Q5：视频太大怎么压缩？
```bash
ffmpeg -i input.mp4 -c:v libx264 -crf 28 -preset slow output_small.mp4
```
CRF越大文件越小（28为中等质量）。

## 参考示例

完整示例见：`/Users/yuzhenghong/Desktop/涉外律师形象展示片.html`

该示例包含：
- 6个完整场景（开场→资质→服务→优势→数据→结尾）
- 播放/暂停控制
- 前进/后退按钮
- 进度条显示
- 键盘控制（空格、方向键）
- 响应式布局
- 背景音乐支持
