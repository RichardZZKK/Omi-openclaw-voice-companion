# Omi -- OpenClaw Voice Companion 小龙虾语音伙伴模块

## 为什么这个项目值得用

- **本地语音识别，不为日常监听额外消耗 token**
- **支持 ElevenLabs，可实现更自然、生动、角色化的声音体验，也支持基于声音片段素材来自定义和克隆音色**
- **同时提供中文和英文脚本版本，适合不同语言场景**
- **后续可以自行修改伙伴名字、提示词和唤醒词，做成真正属于自己的版本**

这个项目让 **运行在 macOS 上的 OpenClaw** 不再只是一个文字助手，而是真正拥有属于自己的声音。  
你不仅可以和它说话，还可以决定它怎么说话：选择你喜欢的音色、克隆你想要的角色声线，甚至把它塑造成你心目中的声音形象，让它成为一个真正属于你的会说话的伙伴。  
后续你也可以继续自行修改伙伴的名字、提示词和唤醒词，让它逐步变成你最想要的那个语音伙伴。  

注意：
- 如果你使用的是 **Mac mini**，由于设备本身没有内置麦克风，还需要额外连接一个麦克风才能正常使用语音输入功能。

English version: [README_EN.md](./README_EN.md)

## 功能
- 常驻监听唤醒词
- 基于 macOS Speech.framework 的本地语音识别
- 语音活动检测（VAD）自动结束录音
- ElevenLabs TTS 缓存播放，未配置时自动回退到 macOS `say`

## 环境要求
- macOS
- Python 3.11+
- 已安装并可正常使用的 OpenClaw
- Terminal 已获得麦克风权限
- 系统可用 `swiftc`

## 安装
拉到本地并进入目录：

```bash
git clone git@github.com:RichardZZKK/Omi-openclaw-voice-companion.git
cd Omi-openclaw-voice-companion
```

如果你更习惯 HTTPS，也可以用：

```bash
git clone https://github.com/RichardZZKK/Omi-openclaw-voice-companion.git
cd Omi-openclaw-voice-companion
```

安装依赖：

```bash
pip3 install -r requirements.txt
```

如果安装时报权限错误，例如 `Permission denied` 或 `externally-managed-environment`，优先改用：

```bash
python3 -m pip install --user -r requirements.txt
```

如果安装时报某个包失败，可以先升级 `pip` 再重试：

```bash
python3 -m pip install --upgrade pip
python3 -m pip install --user -r requirements.txt
```

第一次运行时，macOS 可能会弹出权限请求。

你需要允许：
- `麦克风`
- `语音识别`（如果系统弹出）

如果没有弹窗，也可以手动检查：
- `系统设置 -> 隐私与安全性 -> 麦克风`
- `系统设置 -> 隐私与安全性 -> 语音识别`

确保 `Terminal` 已被允许。

## 配置
如果你想使用 ElevenLabs 音色：
```bash
export ELEVENLABS_API_KEY="your_key"
export ELEVENLABS_VOICE_ID="your_voice_id"
```

如果没有配置上述变量，项目会自动回退到 macOS `say`，但就无法使用更生动、更自然、可自定义或可克隆的音色。

获取 API key 的方式很简单：
- 登录 ElevenLabs
- 进入你的账户或开发者设置页面
- 创建 API key

你也可以在 ElevenLabs 这里选择、创建，或者克隆你想要的音色：
- [https://elevenlabs.io](https://elevenlabs.io)

## 可选配置
如果你想改伙伴名字、提示词或唤醒词，可以直接编辑脚本文件：

- 中文版：`voice_assistant.py`
- 英文版：`voice_assistant_en.py`

常见需要改的内容包括：
- `WAKE_PHRASES`：修改唤醒词
- `EXIT_PHRASES`：修改退出口令
- 语音提示文本：例如“我在”、“我没有听清”、“让我想想”这些提示语

如果你想把它改成自己的伙伴名字，最常见的做法是：
- 把唤醒词改成你想叫它的名字
- 把脚本里的提示语改成你希望它说的话

## 运行方式
### 中文版
文件：`voice_assistant.py`

默认特性：
- 唤醒词：`hi omi` / `omi` / `欧米`
- 中文优先转写
- 更适合中文对话场景

启动：
```bash
python3 voice_assistant.py --device 1
```

### 英文版
文件：`voice_assistant_en.py`

默认特性：
- Wake phrases: `hi omi` / `hey omi` / `omi`
- English-first transcription
- Better suited for English conversations

启动：
```bash
python3 voice_assistant_en.py --device 1
```

## 查看麦克风设备
中文版：
```bash
python3 voice_assistant.py --list-devices
```

英文版：
```bash
python3 voice_assistant_en.py --list-devices
```

## 作者
- [RichardZZKK](https://github.com/RichardZZKK)
