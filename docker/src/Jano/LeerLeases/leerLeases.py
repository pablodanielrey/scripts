# -*- coding: utf-8 -*-

import re

""" FUNCIONA ESTE """
#
# patron = re.compile(r"lease ([0-9.]+) {.*?hardware ethernet ([:a-f0-9]+);.*?}", re.DOTALL)
#
# with open("dhcpd.leases") as f:
#     for match in patron.finditer(f.read()):
#         print(match.group(1), match.group(2))

openLeases=open('dhcpd.leases','r')
leases=openLeases.read()
print ('??????')
patronip=re.finditer(r"lease ([0-9.]+) ", leases)
patronmac=re.finditer(r"{.*?hardware ethernet ([:a-f0-9]+);.*?}", leases)

for match in patronip:
    print(match.group(1))
