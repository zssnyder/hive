from rssi import RSSI_Scan

interface = 'en0'
rssi_scanner = RSSI_Scan(interface)

ssids = ['dd-wrt','linksys']

# sudo argument automatixally gets set for 'false', if the 'true' is not set manually.
# python file will have to be run with sudo privileges.
ap_info = rssi_scanner.getAPinfo(sudo=True)

print(ap_info)