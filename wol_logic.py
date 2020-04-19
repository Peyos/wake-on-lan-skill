import re

class wol_logic(object):

    def ParseSettings(self, rawDeviceList):
        if(rawDeviceList is None):
            return None
        rawDeviceList.strip(' ;')
        parsedDeviceDictionary = {}
        #deviceRegEx = "(?P<device>.+)"+"\("+"(?P<mac>.+)"+"\)"
        deviceRegEx = r"((?P<device>(\w+(\s+)?)+\w+)(\s+)?\((\s+)?(?P<mac>(\w|-|:)+)(\s+)?\))"
        for match in re.finditer(deviceRegEx, rawDeviceList):
            parsedDeviceDictionary[match.group("device").lower()] = match.group("mac").lower()
        return parsedDeviceDictionary

    def GetMacAddress(self, parsedDeviceDictionary, deviceToBoot):
        if(parsedDeviceDictionary is None):
            return None
        if(deviceToBoot is None):
            return None
        if(deviceToBoot.lower() not in parsedDeviceDictionary):
            return None
        configuredMac = parsedDeviceDictionary[deviceToBoot.lower()]
        if not re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", configuredMac):
            return 'invalid'
        return configuredMac
        