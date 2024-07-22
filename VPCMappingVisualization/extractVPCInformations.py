import hid
import pprint

if __name__ == "__main__":
    """
    This code is supposed to look directly on the VPC devices what is the logical > hardware key mapping.
    However this is currently not working, only the initial opening has been coded
    """

    keep = []
    for device_dict in hid.enumerate():
        keys = list(device_dict.keys())
        keys.sort()
        for key in keys:
            if key == 'manufacturer_string' and 'VIRPIL' in device_dict[key]: 
                pprint.pprint(device_dict)
                keep.append(hid)

    print("Opening the device")

    h = keep[1].device()
    keep[1].vendor_id
    #h.open(h, 0x0001)  # TREZOR VendorID/ProductID

    #print("Manufacturer: %s" % h.get_manufacturer_string())
    #print("Product: %s" % h.get_product_string())
    #print("Serial No: %s" % h.get_serial_number_string())