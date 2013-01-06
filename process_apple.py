#!/usr/bin/python2
#
# Copyright (c) 2013 Jordi Mas i Hernandez <jmas@softcatala.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

import os
import fnmatch
import re

class FindFiles:

	def Find(self, directory, pattern):

		filelist = list()

		for root, dirs, files in os.walk(directory):
			for basename in files:
				if fnmatch.fnmatch(basename, pattern):
					filename = os.path.join(root, basename)
					filelist.append(filename)

		filelist.sort()
		return filelist

def main():

	findFiles = FindFiles()

	html_out = open('urls.htm', "w")
	html_wiki = open('urls.wiki', "w")

	html_out.write("<html><body>\n")

	urls = {}
	names = {}
	
	for filename in findFiles.Find('/home/jordi/websites/Apple/', '*'):

		searchfile = open(filename, "r")

		for line in searchfile:
			if 'Catalan' in line:
				searchfile2 = open(filename, "r")
				for h1_line in searchfile2:
					if '<h1>' in h1_line:
						r = re.compile('<h1>(.*?)</h1>')
						m = r.search(h1_line)
						url = filename.replace('/home/jordi/websites/Apple/','https://')
						url = url.replace('mt=','&mt=')
						name = m.group(1)
						if urls.has_key(url) == False and names.has_key(name) == False:
							urls[url] = True;
							names[name] = True;
							html_out.write('"' + name + '" : ' + "<a href=" +url+">" + url + "<a><br/>\n")
							html_wiki.write('* "' + name + '" : ' + "[" +url+ " " + url + "]\n")

				searchfile2.close()

		searchfile.close()

	total = "Total: " + str(len(urls)) + "\n"
	html_out.write(total)
	html_wiki.write(total)
	print total
	html_out.write("</body></html>")


if __name__ == "__main__":
    main()


