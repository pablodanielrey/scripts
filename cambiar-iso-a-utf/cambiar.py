import os
import fnmatch

for root, dir, files in os.walk("sileg"):
	os.system('mkdir {}/{}'.format('sileg2', root))
	for i in fnmatch.filter(files, "*.php"):
		os.system("iconv -f ISO-8859-15 -t UTF-8 {}/{} > {}/{}/{}".format(root, i, 'sileg2', root, i))
	for i in fnmatch.filter(files, "*.html"):
		os.system("iconv -f ISO-8859-15 -t UTF-8 {}/{} > {}/{}/{}".format(root, i, 'sileg2', root, i))
		#print('{}/{}'.format(root,i))
