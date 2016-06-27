# coding: utf-8

import urllib2, json

class Update :

	__API_URL = "https://api.github.com/repos/WassimAttar/managehosting/releases"

	def __init__(self,params,Linux) :
		self.__params = params
		self.__Linux = Linux
		try :
			self.__data = urllib2.urlopen(Update.__API_URL,timeout = 3).read()
		except Exception:
			print('ERROR: can\'t find the current version. Please try again later.')
			exit()
		if len(self.__data) == 2 :
			print('ERROR: No release')
			exit()

	def update(self) :
		parsedjson = json.loads(self.__data)
		newversion = parsedjson[0]["tag_name"]
		if newversion == self.__params.get("version") :
			print('managehosting is up-to-date (' + self.__params.get("version") + ')')
			exit()

		if parsedjson[0]["assets"][0]["name"] == "managehosting" :
			latesturl = parsedjson[0]["assets"][0]["browser_download_url"]
			print('Updating to version ' + newversion + ' ...')
			self.__Linux.executeShellCommand("wget -O managehosting "+latesturl)
			print('Updated managehosting. Restart managehosting to use the new version.')