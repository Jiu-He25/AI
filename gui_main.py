import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QTextEdit, QLineEdit, QPushButton
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QTextCursor
from new import run_llm_application
import asyncio
from qasync import QEventLoop, asyncSlot  # 新增导入


class Ui_Form:
    def setupUi(self, Form):
        Form.resize(600, 400)
        self.textEdit_chat = QTextEdit(Form)
        self.textEdit_chat.setGeometry(20, 20, 560, 300)
        self.textEdit_chat.setReadOnly(True)
        
        self.lineEdit_input = QLineEdit(Form)
        self.lineEdit_input.setGeometry(20, 340, 460, 30)
        
        self.pushButton_send = QPushButton("发送", Form)
        self.pushButton_send.setGeometry(500, 340, 80, 30)
        
        # 清除和退出按钮
        self.pushButton_clear = QPushButton("清除", Form)
        self.pushButton_clear.setGeometry(20, 380, 80, 30)
        
        self.pushButton_exit = QPushButton("退出", Form)
        self.pushButton_exit.setGeometry(500, 380, 80, 30)

class Typewriter:
    def __init__(self, text_edit):
        self.text_edit = text_edit
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_text)
        self.full_text = ""
        self.current_index = 0
        
    def start(self, text):
        self.full_text = text
        self.current_index = 0
        self.text_edit.moveCursor(QTextCursor.End)
        self.text_edit.insertPlainText("\n🤖 DeepSeek：")
        self.timer.start(50)  # 每50毫秒显示一个字符
        
    def update_text(self):
        if self.current_index < len(self.full_text):
            self.text_edit.insertPlainText(self.full_text[self.current_index])
            self.current_index += 1
            self.text_edit.verticalScrollBar().setValue(
                self.text_edit.verticalScrollBar().maximum()
            )
        else:
            self.timer.stop()

class ChatForm(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        # 设置聊天框只读
        self.ui.textEdit_chat.setReadOnly(True)
        
        # 连接按钮到槽函数
        self.ui.pushButton_send.clicked.connect(self.handle_send)
        self.ui.pushButton_clear.clicked.connect(self.handle_clear)
        self.ui.pushButton_exit.clicked.connect(self.handle_exit)
        
        # 回车自动发送
        self.ui.lineEdit_input.returnPressed.connect(self.handle_send)
        
        # 打字机效果
        self.typewriter = Typewriter(self.ui.textEdit_chat)
        
    # def handle_send(self):
    #     """发送按钮点击或回车：获取用户输入，调用大模型，显示回复"""
    #     user_input = self.ui.lineEdit_input.text().strip()
    #     if not user_input:
    #         return
            
    #     self.append_message("👤 你", user_input)
    #     self.ui.lineEdit_input.clear()
        
    #     # 保持原有模型调用逻辑不变
    #     try:
    #         # 这里应该调用实际的模型API
    #         # reply = call_deepseek_model(prompt=user_input)
    #         reply = "这是一个模拟回复。请替换为实际调用结果。"
    #         self.typewriter.start(reply)
    #     except Exception as e:
    #         self.append_message("🤖 DeepSeek", f"[模型异常] {e}")
    @asyncSlot()  # 使用qasync的异步槽装饰器
    async def handle_send(self):
        """异步处理用户发送的消息"""
        user_input = self.ui.lineEdit_input.text().strip()
        if not user_input:
            return
            
        self.append_message("👤 你", user_input)
        self.ui.lineEdit_input.clear()
        self.ui.pushButton_send.setEnabled(False)  # 禁用按钮防止重复点击
        
        try:
            # 构造输入数据
            input_data = {
                "api_key": 'sk-32b705ff866949f788a2fde04f9d0fb0',  # 替换为你的API Key
                "prompt": user_input,
                "modality": "text",
                "parameters": {
                    "temperature": 0.7,
                    "max_tokens": 800,
                    "stream": False  # 同步模式更简单
                }
            }
            
            # 调用异步函数获取回复
            reply = await run_llm_application(input_data)
            self.typewriter.start(reply)
            
        except Exception as e:
            self.append_message("🤖 DeepSeek", f"[错误] {str(e)}")
        finally:
            self.ui.pushButton_send.setEnabled(True)  # 重新启用按钮
    
    def handle_clear(self):
        """清除聊天记录"""
        self.ui.textEdit_chat.clear()
    
    def handle_exit(self):
        """退出程序"""
        self.close()
    
    def append_message(self, sender, message):
        """追加一条聊天信息，并滚动到底部"""
        self.ui.textEdit_chat.append(f"<b>{sender}：</b> {message}")
        self.ui.textEdit_chat.verticalScrollBar().setValue(
            self.ui.textEdit_chat.verticalScrollBar().maximum()
        )

# def gui():
#     """启动 GUI 应用"""
#     app = QApplication(sys.argv)
#     window = ChatForm()
#     window.setWindowTitle("DeepSeek 聊天界面")
#     window.show()
#     sys.exit(app.exec_())
def gui():
    """启动 GUI 应用（集成异步事件循环）"""
    app = QApplication(sys.argv)
    
    # 设置异步事件循环
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    
    window = ChatForm()
    window.setWindowTitle("DeepSeek 聊天界面")
    window.show()
    
    with loop:
        sys.exit(loop.run_forever())

if __name__ == '__main__':
    gui()
