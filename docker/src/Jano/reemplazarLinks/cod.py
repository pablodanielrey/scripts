# -*- coding: utf-8 -*-
import glob
from chardet.universaldetector import UniversalDetector

detector = UniversalDetector()
for filename in glob.glob('*.rdf'):
    print (filename.ljust(60))
    detector.reset()
    for line in file(filename, 'rb'):
        detector.feed(line)
        if detector.done:
            break
    detector.close()
    print (detector.result)
