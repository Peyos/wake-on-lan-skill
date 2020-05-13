from mycroft import MycroftSkill, intent_file_handler
from mycroft.util.parse import match_one
from wakeonlan import send_magic_packet
from .wol_logic import wol_logic

class WakeOnLan(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('wake.on.lan.intent')
    def handle_wake_on_lan(self, message):
        wolLogic = wol_logic()
        rawDeviceSetting = self.settings.get('DeviceList')
        self.log.debug('DeviceList = ' + rawDeviceSetting )
        if ((rawDeviceSetting is None) or (rawDeviceSetting == '')):
            self.speak_dialog('wake.on.lan.no.devices')

        parsedConfig = wolLogic.ParseSettings(rawDeviceSetting)
        if(parsedConfig is None or parsedConfig is {}):
            self.speak_dialog('wake.on.lan.configuration.error')

        requestedDevice = message.data.get('device')
        bestMatchingDeviceFromConfig = match_one(requestedDevice, list(parsedConfig.keys()))

        mac = wolLogic.GetMacAddress(parsedConfig, bestMatchingDeviceFromConfig)
        if(mac is None):
            self.speak_dialog('wake.on.lan.unknown.device', {'device':requestedDevice})
            return
        if(mac is 'invalid'):
            self.speak_dialog('wake.on.lan.invalid.mac', {'device':requestedDevice})
            return

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

