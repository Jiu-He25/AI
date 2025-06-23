import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from Ui_gui_ui import Ui_Form  # 你生成的 UI 类
from typewriter import Typewriter  # 打字机效果类
#from deepseek_api import call_deepseek_model  # 你自己的大模型调用方法

class ChatForm(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # 设置聊天框只读
        self.ui.textEdit_chat.setReadOnly(True)

        # 连接按钮到槽函数
        self.ui.pushButton_send.clicked.connect(self.handle_send)

        # 回车自动发送
        self.ui.lineEdit_input.returnPressed.connect(self.handle_send)
        
        #打字机效果
        self.typewriter = Typewriter(self.ui.textEdit_chat)

    def handle_send(self):
        """发送按钮点击或回车：获取用户输入，调用大模型，显示回复"""
        user_input = self.ui.lineEdit_input.text().strip()
        if not user_input:
            return

        self.append_message("👤 你", user_input)
        self.ui.lineEdit_input.clear()

        # try:
        #     reply = call_deepseek_model(prompt=user_input)
        # except Exception as e:
        #     reply = f"[模型异常] {e}"
        reply="这是一个模拟回复。请替换为实际调用结果。"

        #self.append_message("🤖 DeepSeek", reply)
        self.typewriter.start(reply)

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ChatForm()
    window.setWindowTitle("DeepSeek 聊天界面")
    window.show()
    sys.exit(app.exec_())
