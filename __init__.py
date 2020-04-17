from mycroft import MycroftSkill, intent_file_handler


class WakeOnLan(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('lan.on.wake.intent')
    def handle_lan_on_wake(self, message):
        self.speak_dialog('lan.on.wake')


def create_skill():
    return WakeOnLan()

