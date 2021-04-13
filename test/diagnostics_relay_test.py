# -*- coding:utf-8 -*-
'''diagnostics_relay test case
'''

import unittest
import time

from pymobiledevice3.usbmux import USBMux
from pymobiledevice3.lockdown import LockdownClient
from pymobiledevice3.services.diagnostics_service import DiagnosticsService


class DiagnosticsRelayTest(unittest.TestCase):

    def test_reboot_device(self):
        mux = USBMux()
        if not mux.devices:
            mux.process(0.1)
        if len(mux.devices) == 0:
            print("no real device found")
            return
        udid = mux.devices[0].serial
        lockdown = LockdownClient(udid)
        DiagnosticsService(lockdown).restart()
        time.sleep(10)
        for _ in range(20):
            mux.process(1)
            for dev in mux.devices:
                if udid == dev.serial:
                    print('reboot successfully')
                    return
        else:
            self.fail('reboot error: real device disconect')
