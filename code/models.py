import time

class Message:
    def __init__(self, text):
        self.text = text
        self.time = int(time.time())

    def get_text(self):
        return self.text

    def get_time(self):
        return self.time

    def to_string(self):
        return f"{self.time}:{self.text}"

class Blackboard:
    def __init__(self, name, validity):
        self.name = name
        self.current_msg = Message("")
        self.validity = validity

    def msg_valid(self):
        if self.validity == 0:
            return True
        return (self.current_msg.time + self.validity) > int(time.time())

    def get_current_msg(self):
        return self.current_msg.get_text()

    def set_current_msg(self, message):
        self.current_msg = Message(message)

    def to_string(self):
        return self.name

    def to_dict(self):
        return {
            "bb_empty": self.current_msg is None,
            "msg_time": self.current_msg.get_time(),
            "msg_valid": self.msg_valid()
        }
