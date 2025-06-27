# AI基础大作业

# 🤖 大语言模型交互系统（DeepSeek集成）

本项目是一个基于 [DeepSeek](https://deepseek.com/) 大语言模型 API 的交互式文本生成系统，支持命令行（CLI）和图形用户界面（GUI）交互方式，具备参数调节、输入输出校验、测试数据处理等完整功能链，适用于大语言模型效果对比、调试、教学演示等任务。

---

## 📌 项目亮点

- ✅ 支持 DeepSeek API 集成与调用
- ✅ CLI & GUI 双交互模式（基于 PyQt5）
- ✅ 可调节 temperature 等参数，实时对比输出差异
- ✅ 使用 JSON Schema 定义并验证输入格式
- ✅ 支持模拟真实场景测试数据的处理与展示
- ✅ 实现“打字机”式逐字输出效果，增强交互体验

---

## 📁 项目结构

.
├── cli_app.py # 命令行程序入口
├── gui_app.py # 图形界面程序入口（PyQt5）
├── deepseek_api.py # DeepSeek API 调用封装
├── schema.py # JSON Schema 校验逻辑
├── test_data.json # 示例测试数据
├── ui_form.ui # Qt Designer 源文件
├── ui_form.py # UI 转换后的 Python 文件
├── utils/
│ └── typewriter.py # 打字机样式输出实现
├── requirements.txt # Python依赖包
└── README.md # GitHub 仓库说明文档

🧪 测试数据示例
位于 test_data.json：

json
[
  {
    "prompt": "写一段春天的描写",
    "temperature": 0.3
  },
  {
    "prompt": "写一段春天的描写",
    "temperature": 1.5
  }
]
用于演示参数变化对生成结果的影响。

🛠 输入格式校验（JSON Schema）
所有输入都基于 Schema 校验，确保系统安全与稳定：

json
{
  "type": "object",
  "properties": {
    "user_input": { "type": "string" },
    "temperature": { "type": "number", "minimum": 0.0, "maximum": 2.0 }
  },
  "required": ["user_input"]
}

📜 License
本项目仅用于课程教学与非商业研究用途