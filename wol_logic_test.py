import unittest
from unittest.mock import MagicMock
from wol_logic import wol_logic

class TestWolLogic(unittest.TestCase):

    def test_001_ParseSettings_returns_none_if_rawDeviceList_is_none(self):
        wl = wol_logic()
        retVal = wl.ParseSettings(None)
        self.assertEqual(None, retVal)

    def test_002_ParseSettings_returns_empty_dictionary_if_rawDeviceList_is_empty(self):
        wl = wol_logic()
        retVal = wl.ParseSettings("")
        self.assertEqual({}, retVal)

    def test_003_ParseSettings_returns_empty_dictionary_if_rawDeviceList_is_abc(self):
        wl = wol_logic()
        retVal = wl.ParseSettings("abc")
        self.assertEqual({}, retVal)

    def test_004_ParseSettings_returns_empty_dictionary_if_rawDeviceList_is_abc_semicolon_abc(self):
        wl = wol_logic()
        retVal = wl.ParseSettings("abc;abc")
        self.assertEqual({}, retVal)

    def test_005_ParseSettings_returns_correct_dictionary_in_all_lower_case_if_rawDeviceList_contains_on_or_more_elements(self):
        wl = wol_logic()
        testParameter = [
            ("Computer1(01-23-45-67-89-AB)", {"computer1":"01-23-45-67-89-ab"}),
            ("Computer2(01:23:45:67:89:ab)", {"computer2":"01:23:45:67:89:ab"}),
            ("Computer3(01-23-45-67-89-AB);", {"computer3":"01-23-45-67-89-ab"}),
            ("; Computer4(01-23-45-67-89-AB) ", {"computer4":"01-23-45-67-89-ab"}),
            ("Computer5(01-23-45-67-89-AB);Nas(cd-ef-45-67-89-AB)", {"computer5":"01-23-45-67-89-ab", "nas":"cd-ef-45-67-89-ab"}),
            ("Computer6(01-23-45-67-89-AB) ; Nas(cd-ef-45-67-89-AB)", {"computer6":"01-23-45-67-89-ab", "nas":"cd-ef-45-67-89-ab"}),
            ("  Com pu ter7  (01-23-45-67-89-AB) ; Nas(  cd:ef:45:67:89:AB  ). , Nas 2(cd-ef-45-67-89-AB); df sasd", {"com pu ter7":"01-23-45-67-89-ab", "nas":"cd:ef:45:67:89:ab", "nas 2":"cd-ef-45-67-89-ab"})
        ]
        for configInput, expectedDesult in testParameter:
            with self.subTest():
                retVal = wl.ParseSettings(configInput)
                self.assertEqual(expectedDesult, retVal)

    def test_100_GetMacAddress_returns_none_if_parsedDeviceDictionary_is_none(self):
        wl = wol_logic()
        retVal = wl.GetMacAddress(None,"NAS")
        self.assertEqual(None, retVal)

    def test_101_GetMacAddress_returns_none_if_deviceToBoot_is_none(self):
        wl = wol_logic()
        devices = {("Computer", "01-23-45-67-89-AB")}
        retVal = wl.GetMacAddress(devices,None)
        self.assertEqual(None, retVal)

    def test_102_GetMacAddress_returns_none_if_deviceToBoot_is_not_in_parsedDeviceDictionary(self):
        wl = wol_logic()
        devices = {"Computer": "01-23-45-67-89-AB"}
        retVal = wl.GetMacAddress(devices,"NAS")
        self.assertEqual(None, retVal)
    
    def test_110_GetMacAddress_returns_mac_address_if_deviceToBoot_is_in_parsedDeviceDictionary_case_insensitive(self):
        wl = wol_logic()
        devices = {"computer":"01-23-45-67-89-AB", "nas":"cd-ef-45-67-89-ab"}
        retVal = wl.GetMacAddress(devices,"Nas")
        self.assertEqual("cd-ef-45-67-89-ab", retVal)

    def test_111_GetMacAddress_returns_invalid_if_mac_address_for_deviceToBoot_is_not_in_valid_format(self):
        wl = wol_logic()
        testParameter = [
            ({"nas":"g1-ef-45-67-89-ab"}),
            ({"nas":"d-ef-45-67-89-ab"}),
            ({"nas":"cdef-45-67-89-ab"}),
            ({"nas":"c d-ef-45-67-89-ab"}),
            ({"nas":"cd,ef-45-67-89-ab"}),
            ({"nas":"cd.ef-45-67-89-ab"}),
            ({"nas":" cd-ef-45-67-89-ab"}),
            ({"nas":"acd-ef-45-67-89-ab"}),
            ({"nas":"-cd-ef-45-67-89-ab"}),
            ({"nas":"cd-ef-45-67-89-ab-"}),
        ]
        for devices in testParameter:
            with self.subTest():
                retVal = wl.GetMacAddress(devices,"nas")
                self.assertEqual('invalid', retVal)


if __name__ == '__main__':
    unittest.main()
