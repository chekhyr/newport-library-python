from ctypes import *
import sys
import os


class CommandError(Exception):
    """The function in the usbdll.dll was not successfully evaluated"""

class NewportConnection:
    def __init__(self, **kwargs):
        """
        :param kwargs:
            **libpath (raw string): path to the USB library
            **product_id (hex int): product ID of the device(s) to connect
        """
        self.status = "Not connected"
        self.num_devices = 0
        self.product_id = kwargs.get("product_id", 0xCEC7)
        default_path = os.path.join("C:", "Program Files", "Newport", "Newport USB Driver", "Bin", "usbdll.dll")
        try:
            self.libpath = kwargs.get("libpath", default_path)
            self.lib = windll.LoadLibrary(self.libpath)
        except OSError as e:
            sys.exit(e.strerror + " usbdll.dll")
        self.open_connections()
        self.keys = self.get_instrument_keys()
        print("DeviceID | Model# Serial#")
        for x in self.keys:
            print("%8d | %14s" % (self.keys.index(x), x.decode("ASCII")))

    def open_connections(self):
        n = c_int()
        try:
            status = self.lib.newp_usb_open_devices(c_int(self.product_id), c_bool(False),
                                                    byref(n))
            if status != 0:
                raise CommandError(
                    "Failed to establish connection\nPlease, make sure all devices are properly connected")
            else:
                self.status = "Connected"
                print("Devices connected: %d" % n.value + '\n')
                self.num_devices = n.value
        except CommandError as e:
            sys.exit(e)

    def get_instrument_keys(self):
        Buffer = [create_string_buffer(24) for i in range(self.num_devices)]
        pBuffer = (c_char_p * self.num_devices)(*map(addressof, Buffer))
        try:
            status = self.lib.newp_usb_get_model_serial_keys(byref(pBuffer))
            if status != 0:
                raise CommandError("Failed to retrieve device keys")
            else:
                return [pBuffer[n] for n in range(0, self.num_devices)]
        except CommandError as e:
            sys.exit(e)

    def write(self, ID, buffer):
        DeviceKey = create_string_buffer(self.keys[ID])
        Command = create_string_buffer(buffer.encode("ASCII"))
        Length = c_ulong(len(buffer.encode("ASCII")))
        return self.lib.newp_usb_write_by_key(byref(DeviceKey), byref(Command), Length)

    def read(self, ID):
        DeviceKey = create_string_buffer(self.keys[ID])
        Buffer = create_string_buffer(1024)
        Length = c_ulong(1024)
        BytesRead = c_ulong()
        try:
            status = self.lib.newp_usb_read_by_key(byref(DeviceKey), byref(Buffer), Length, byref(BytesRead))
            if status != 0:
                raise CommandError("Failed to read device response")
            else:
                return Buffer.value.decode("ASCII")
        except CommandError as e:
            sys.exit(e)

    def query(self, ID, buffer):
        try:
            status = self.write(ID, buffer)
            if status != 0:
                raise CommandError("Failed to read device response")
            else:
                pass
        except CommandError as e:
            sys.exit(e)
        return self.read(ID)

    def close_all(self):
        status = self.lib.newp_usb_uninit_system()
        print("Closed all Newport device connections with code: %d" % status)
