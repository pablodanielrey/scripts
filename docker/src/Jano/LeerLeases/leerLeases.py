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

patron=re.compile(r"lease ([0-9.]+)", leases)

print (patron.match(leases))
