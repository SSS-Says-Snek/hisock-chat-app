from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import Qt

from hisock import ThreadedHiSockClient

from src.ui.generated.main_ui import Ui_MainWindow
from src.ui.custom.message import Message


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, client: ThreadedHiSockClient, username: str):
        super().__init__()

        self.setupUi(self)

        self.messageToSend.returnPressed.connect(self.send_message)
        self.sendButton.clicked.connect(self.send_message)

        self.scrollarea_vbar = self.message_scrollarea.verticalScrollBar()
        # This will be changed later so that people can view older messages while other people're talking
        self.scrollarea_vbar.rangeChanged.connect(self.on_scroll_change)

        self.client = client
        self.username = username

        self.messages.setAlignment(Qt.AlignmentFlag.AlignTop)

        # haha_messages = [
        #     "Wowwwww \n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nn\n\n\namogus Wowwwww amogus Wowwwww amogus Wowwwww amogus Wowwwww amogus Wowwwww amogus Wowwwww amogus Wowwwww amogus Wowwwww amogus Wowwwww amogus Wowwwww amogus Wowwwww amogus Wowwwww amogus !!",
        #     "cool",
        #     "cool",
        #     "cool"
        # ]

        # for message in haha_messages:
        #     self.messages.addWidget(Message(self.username, message))

        @self.client.on("recv_everyone_message")
        def on_recv_everyone_message(data: dict):
            if data["username"] == self.username:
                print("wow")



    def on_scroll_change(self):
        self.scrollarea_vbar.setValue(self.scrollarea_vbar.maximum())

    
    def send_message(self):
        text = self.messageToSend.text()

        message = Message(self.username, text)
        self.messages.addWidget(
            message
        )

        self.client.send("send_everyone_message", text)
        
        # x = self.message_scrollarea.verticalScrollBar().maximum()
        # self.message_scrollarea.verticalScrollBar().setValue(
        #     x
        # )
        # scrollarea_vbar.setValue(scrollarea_vbar.maximum())

        self.messageToSend.clear()