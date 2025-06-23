from PyQt5.QtCore import QTimer

class Typewriter:
    def __init__(self, text_widget, sender="🤖 DeepSeek"):
        self.text_widget = text_widget
        self.full_text = ""
        self.current_index = 0
        self.timer = QTimer()
        self.sender = sender

        self.timer.timeout.connect(self.append_next_char)

    def start(self, text):
        """开始打字"""
        self.full_text = text
        self.current_index = 0
        self.text_widget.append(f"<b>{self.sender}：</b>")  # 初始化sender
        self.timer.start(30)  # 每30毫秒打印一个字符

    def append_next_char(self):
        """每次追加一个字符"""
        if self.current_index < len(self.full_text):
            cursor = self.text_widget.textCursor()
            cursor.movePosition(cursor.End)
            cursor.insertText(self.full_text[self.current_index])
            self.current_index += 1
            self.text_widget.setTextCursor(cursor)
        else:
            self.timer.stop()
