from models import Blackboard

class BlackboardWorker:
    def __init__(self):
        self.blackboards = {}

    def create_bb(self, name, validity):
        if len(name) > 32:
            return 1
        elif name in self.blackboards:
            return 2
        self.blackboards[name] = Blackboard(name, validity)
        return 0

    def delete_bb(self, name):
        if name not in self.blackboards:
            return False
        del self.blackboards[name]
        return True

    def writing_bb(self, name, message):
        if name not in self.blackboards:
            return 2
        if len(message) > 255:
            return 1
        self.blackboards[name].set_current_msg(message)
        return 0

    def clear_bb(self, name):
        if name not in self.blackboards:
            return False
        self.blackboards[name].set_current_msg(None)
        return True

    def read_bb(self, name):
        if name not in self.blackboards:
            return "", 1
        blackboard = self.blackboards[name]
        if len(blackboard.get_current_msg()) == 0:
            return "", 2
        return blackboard.get_current_msg(), 0

    def bb_status(self, name):
        if name not in self.blackboards:
            return False
        return self.blackboards[name].to_dict()

    def get_bbs(self):
        return list(self.blackboards.keys())

    def delete_all_bbs(self):
        self.blackboards.clear()
        return True
