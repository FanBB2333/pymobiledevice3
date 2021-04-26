import dataclasses

from pymobiledevice3.services.dvt.instruments.device_info import DeviceInfo
from pymobiledevice3.services.dvt.tap import Tap


class Sysmontap(Tap):
    IDENTIFIER = 'com.apple.instruments.server.services.sysmontap'

    def __init__(self, dvt):
        self._device_info = DeviceInfo(dvt)

        process_attributes = list(self._device_info.request_information('sysmonProcessAttributes'))
        system_attributes = list(self._device_info.request_information('sysmonSystemAttributes'))

        self.process_attributes_cls = dataclasses.make_dataclass('SysmonProcessAttributes', process_attributes)
        self.system_attributes_cls = dataclasses.make_dataclass('SysmonSystemAttributes', system_attributes)

        config = {
            'ur': 1000,  # Output frequency ms
            'bm': 0,
            'procAttrs': process_attributes,
            'sysAttrs': system_attributes,
            'cpuUsage': True,
            'sampleInterval': 1000000000
        }

        super().__init__(dvt, self.IDENTIFIER, config)
