# AI基础大作业

# 🤖 大语言模型交互系统（DeepSeek集成）

本项目是一个基于 [DeepSeek](https://deepseek.com/) 大语言模型 API 的交互式文本生成系统，支持图形用户界面（GUI）交互方式，具备参数调节、输入输出校验、测试数据处理等完整功能链，适用于大语言模型效果对比、调试、教学演示等任务。

---
#使用方法

直接运行gui_main 文件，需要设置api_key,由于是开源项目，故提交的代码中将其设置为空字符串，也可以再增加.env文件从环境中读入
gui中也可以设置temperature

## 📌 项目亮点

- ✅ 支持 DeepSeek API 集成与调用
- ✅ CLI & GUI 双交互模式（基于 PyQt5）
- ✅ 可调节 temperature 等参数，实时对比输出差异
- ✅ 使用 JSON Schema 定义并验证输入格式
- ✅ 支持模拟真实场景测试数据的处理与展示
- ✅ 实现“打字机”式逐字输出效果，增强交互体验

---

## 📁 项目结构

AI/
├── ui/                            # UI 界面及相关逻辑模块
│   ├── gui_ui.ui                  # Qt Designer 创建的原始 .ui 文件
│   ├── Ui_gui_ui.py               # 由 .ui 文件生成的 Python 界面类
├── exception_handler.py       # 错误处理与弹窗模块
├── input_processor.py         # 处理输入数据（格式化、敏感词过滤）
├── llm_service.py             # 模型服务封装（调用 DeepSeek 等）
├── parameter_tuner.py         # 模型参数调节器（如 temperature）
├── stream_handler.py          # 流式响应处理（用于逐字输出）
└── __pycache__/               # Python 编译缓存文件夹

├── gui_main.py                # GUI 主入口，控制界面与模型联动
├── schema.py                      # 输入 JSON Schema 格式校验器
├── sensitive_words.txt            # 敏感词词库（用于内容筛查）
├── testdata.json                  # 用于测试的 Prompt 和参数样例数据
├── README.md                      # 项目说明文档（当前文件）
├── requirements.txt               # Python 依赖库列表
├── new.py                         # 脚本主流程/调试入口（临时测试或调用模型）
└── docs/                          # 项目技术文档目录（可选）


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