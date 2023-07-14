# coding: utf-8

import os, subprocess, string, random, pwd

class Linux :

	def __init__(self,params) :
		self.__params = params

	def executeShellCommand(self,command) :
		if self.__params["verbose"] :
			print(command)
		if self.__params["execute"] :
			subprocess.call(command, shell=True)

	def generateRandomString(self,size) :
		return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(size)])

	def getUid(self) :
		return pwd.getpwnam(self.__params["account"]).pw_uid

	def __linuxUserExists(self) :
		try:
			pwd.getpwnam(self.__params["account"])
			return True
		except KeyError:
			return False

	def createUser(self,shell,password) :
		self.executeShellCommand("useradd --home {0} --create-home -s {2} {3} {1}".format(self.__params["openBaseDir"],self.__params["account"],shell,password))
		return True

	def deleteUser(self) :
		self.executeShellCommand("userdel -f -r "+self.__params["account"])
		return True

	def exist(self):
		display = ""
		if os.path.isdir(self.__params["openBaseDir"]) :
			display += "Path {0} already exists\n".format(self.__params["openBaseDir"])
		if self.__linuxUserExists() :
			display += "Linux user {0} already exists\n".format(self.__params["account"])
		return display

	def create(self):
		return ""

	def delete(self):
		return ""
