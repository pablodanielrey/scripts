#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Make it work with Python 2 and Python 3
import sys
PY3 = sys.version > '3'

if not PY3:
    from future.builtins import open

# Specify the encoding while opening it
with open("cedlas0003.rdf", encoding="ISO-8859-1") as f:
    content = f.read()
content = content.encode('UTF-8', 'replace')
print(content)
