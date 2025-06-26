# import sys
# from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
# from ui.Ui_gui_ui import Ui_Form  # 你生成的 UI 类
# from ui.typewriter import Typewriter  # 打字机效果类
# #from deepseek_api import call_deepseek_model  # 你自己的大模型调用方法

# class ChatForm(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.ui = Ui_Form()
#         self.ui.setupUi(self)

#         # 设置聊天框只读
#         self.ui.textEdit_chat.setReadOnly(True)

#         # 连接按钮到槽函数
#         self.ui.pushButton_send.clicked.connect(self.handle_send)

#         # 回车自动发送
#         self.ui.lineEdit_input.returnPressed.connect(self.handle_send)
        
#         #打字机效果
#         self.typewriter = Typewriter(self.ui.textEdit_chat)

#     def handle_send(self):
#         """发送按钮点击或回车：获取用户输入，调用大模型，显示回复"""
#         user_input = self.ui.lineEdit_input.text().strip()
#         if not user_input:
#             return

#         self.append_message("👤 你", user_input)
#         self.ui.lineEdit_input.clear()

#         # try:
#         #     reply = call_deepseek_model(prompt=user_input)
#         # except Exception as e:
#         #     reply = f"[模型异常] {e}"
#         reply="这是一个模拟回复。请替换为实际调用结果。"

#         #self.append_message("🤖 DeepSeek", reply)
#         self.typewriter.start(reply)

#     def handle_clear(self):
#         """清除聊天记录"""
#         self.ui.textEdit_chat.clear()

#     def handle_exit(self):
#         """退出程序"""
#         self.close()

#     def append_message(self, sender, message):
#         """追加一条聊天信息，并滚动到底部"""
#         self.ui.textEdit_chat.append(f"<b>{sender}：</b> {message}")
#         self.ui.textEdit_chat.verticalScrollBar().setValue(
#             self.ui.textEdit_chat.verticalScrollBar().maximum()
#         )
# import sys
# from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox

# # 本地模块导入（使用相对路径）
# from ui.Ui_gui_ui import Ui_Form  # UI 文件生成的类
# from ui.typewriter import Typewriter
# from llm_service import LLMService  # 核心服务
# from main import run_llm_application  # 复用主逻辑

# class ChatForm(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.ui = Ui_Form()
#         self.ui.setupUi(self)
#         self.ui.textEdit_chat.setReadOnly(True)
#         self.ui.pushButton_send.clicked.connect(self.handle_send)
#         self.ui.lineEdit_input.returnPressed.connect(self.handle_send)
#         self.typewriter = Typewriter(self.ui.textEdit_chat)

#     async def _call_model_async(self, user_input):
#         """异步调用模型"""
#         input_data = {
#             "api_key": "your_api_key",  # 从环境变量获取
#             "prompt": user_input,
#             "modality": "text",
#             "parameters": {"temperature": 0.7}
#         }
#         return await run_llm_application(input_data)

#     def handle_send(self):
#         user_input = self.ui.lineEdit_input.text().strip()
#         if not user_input:
#             return

#         self.append_message("👤 你", user_input)
#         self.ui.lineEdit_input.clear()

#         # 启动异步任务
#         asyncio.create_task(self._get_model_reply(user_input))

#     async def _get_model_reply(self, user_input):
#         """获取模型回复并显示"""
#         try:
#             result = await self._call_model_async(user_input)
#             reply = result["response"]["choices"][0]["message"]["content"]
#             self.typewriter.start(reply)
#         except Exception as e:
#             self.append_message("🤖 DeepSeek", f"[错误] {str(e)}")

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = ChatForm()
#     window.setWindowTitle("DeepSeek 聊天界面")
#     window.show()
#     sys.exit(app.exec_())
# guiFrame.py
import sys
import asyncio
from PyQt5.QtWidgets import QWidget, QApplication
from ui.Ui_gui_ui import Ui_Form
from ui.typewriter import Typewriter
from core import run_llm_application

class ChatForm(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.typewriter = Typewriter(self.ui.textEdit_chat)
        self.ui.pushButton_send.clicked.connect(self.handle_send)

    async def call_model(self, prompt):
        input_data = {
            "prompt": prompt,
            "parameters": {"temperature": 0.7}
        }
        return await run_llm_application(input_data)

    def handle_send(self):
        prompt = self.ui.lineEdit_input.text().strip()
        if not prompt:
            return
            
        self.ui.textEdit_chat.append(f"👤 You: {prompt}")
        self.ui.lineEdit_input.clear()
        
        asyncio.create_task(self.get_reply(prompt))

    async def get_reply(self, prompt):
        try:
            result = await self.call_model(prompt)
            reply = result["response"]["choices"][0]["message"]["content"]
            self.typewriter.start(reply)
        except Exception as e:
            self.ui.textEdit_chat.append(f"🤖 Error: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatForm()
    window.show()
    sys.exit(app.exec_())