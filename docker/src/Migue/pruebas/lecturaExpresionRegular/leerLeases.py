# -*- coding: utf-8 -*-

import re
openLeases=open('dhcpd.leases','r')
try:
    leases=openLeases.read()
    patronip=re.finditer("lease ([0-9\.]+) .*?hardware ethernet (.*?);", leases, re.S)
    #patronip=re.finditer("lease ([0-9\.]+) .*?hardware ethernet ([:a-f0-9]+)", leases, re.S)
    # patronip=re.finditer("(lease ([0-9\.]+) .*?})", leases, re.S)
finally:
    openLeases.close()

cant=0
for search in patronip:
    print(search.group(1),'   >>>>>>>>>>>>>>  ', search.group(2))
    cant=cant +1

print (cant)




#     patronip=re.finditer("(client-hostname \"\w*.?)", leases, re.S)
#     # patronmac=re.finditer("hardware ethernet ([:a-f0-9]+) ", leases)
# finally:
#     openLeases.close()
#     cant=0
#     for search in patronip:
#         print(search.group(1))
#         cant=cant +1
#     print (cant)
