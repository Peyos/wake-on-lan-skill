from mycroft import MycroftSkill, intent_file_handler
from wakeonlan import send_magic_packet
import wol_logic

class WakeOnLan(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('wake.on.lan.intent')
    def handle_wake_on_lan(self, message):
        wolLogic = wol_logic.wol_logic()
        rawDeviceSetting = self.settings.get('DeviceList', {})
        if (rawDeviceSetting is None or rawDeviceSetting is {}):
            self.speak_dialog('wake.on.lan.no.devices')

        parsedConfig = wolLogic.ParseSettings(rawDeviceSetting)
        if(parsedConfig is None or parsedConfig is {}):
            self.speak_dialog('wake.on.lan.configuration.error')

        requestedDevice = message.data.get('device')
        mac = wolLogic.GetMacAddress(parsedConfig, requestedDevice)
        if(mac is None):
            self.speak_dialog('wake.on.lan.unknown.device', {'device':requestedDevice})
        if(mac is 'invalid'):
            self.speak_dialog('wake.on.lan.invalid.mac', {'device':requestedDevice})

        confirmation = self.ask_yesno('wake.on.lan.send.package.confirmation', {"device": requestedDevice})
        if confirmation == "yes":
            try:
                send_magic_packet(mac)
                self.speak_dialog('wake.on.lan.success', {"device": requestedDevice})

            except Exception:
                self.speak_dialog('wake.on.lan.send.package.error')
                    

    def stop(self):
        pass

def create_skill():
    return WakeOnLan()

