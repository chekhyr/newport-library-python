# Newport USB API for Python

## Introduction

This [Python module](./newp_usb.py) is a wrapper for Newport's official Windows USB DLL. It offers a simple Python API for exchanging SPCI-queries with Newport powermeters inside a pure-Python workflow. For instructions on connecting hardware to a computer, please refer to the official manual for your device.

## Download

This module requires the official Newport USB Driver. To download it follow these steps:
  
1. Go to the [official portal](https://download.newport.com/)
2. Log in using these credentials  
    **Username:** `anonymous`  
    **Password:** (leave empty)
3. Navigate to the **Software > Newport_USB_Driver** folder
4. Download the latest driver `.zip`-file from this folder

## Installation

1.  **Extract** the downloaded ZIP-file
2.  **Navigate** to the subfolder corresponding to your system architecture
    *   **32-bit:** `PowerMeter 3.0.2\win32`
    *   **64-bit:** `PowerMeter 3.0.2\x86Onx64`
3.  **Install** both packages by running the MSI files found in that folder
    *   **32-bit:** `PMSetup32.msi` and `USBDriverSetup32.msi`
    *   **64-bit:** `PMSetup32on64.msi` and `USBDriverSetup32on64.msi`
4.  The software will install to the default location
    *   **32-bit:** `C:\Program Files\Newport\`
    *   **64-bit:** `C:\Program Files (x86)\Newport\`
5.  The required `libpath` argument to initialize the instrument is
    *   **32-bit:** `r'C:\Program Files\Newport\Newport USB Driver\Bin\usbdll.dll'`
    *   **64-bit:** `r'C:\Program Files (x86)\Newport\Newport USB Driver\Bin\usbdll.dll'`

Before you run the Python module, make sure that you can run the "Newport Powermeter" application. That confirms that the driver is installed properly and nothing causes problems with hardware connection.

## Getting the Product ID 

The variable `product_id` is required to intialize the instrument. To construct it follow these steps:
 
1. Open the Windows Device Manager
2. Expand the Human Interface Devices node
3. Double-click the device of interest -- the USB Human Interface Device Properties window appears
4. Click the Details tab
5. In the Property drop-down box, select Hardware Ids. The value will contain "PID_HEXC", then use "0xHEXC" as your `product_id`

For a more detailed explanation [click here](http://thecurlybrace.blogspot.com/2010/07/how-to-find-usb-device-vendor-and.html).

## Additional notes

This module enables communication with Newport powermeters using SPCI-commands. For a complete list of commands supported by your device, please refer to its official manual (eg. the [1918-R series manual](https://www.newport.com/medias/sys_master/images/images/haf/h3d/8797247275038/Rev-A-1918-R-Power-Meter-User-s-Manual.pdf)).
