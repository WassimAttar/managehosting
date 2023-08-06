# coding: utf-8

import os, subprocess, string, random, pwd, crypt

class Linux :

	__createConfTemplate = """
{3} :
ip : {0}
login : {1}
pass : {2}
"""

	def __init__(self,params) :
		self.__params = params

	def executeShellCommand(self,command) :
		if self.__params["verbose"] :
			print(command)
		if self.__params["execute"] :
			subprocess.call(command, shell=True)

	def generateRandomString(self,size) :
		return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(size)])

	def __linuxUserExists(self) :
		try:
			pwd.getpwnam(self.__params["account"])
			return True
		except KeyError:
			return False

	def __createUser(self,shell,password) :
		self.executeShellCommand("useradd --home {0} --create-home -s {2} {3} {1}".format(self.__params["openBaseDir"],self.__params["account"],shell,password))
		return True

	def __deleteUser(self) :
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
		if self.__params["sshPassword"] == "" :
			password = self.generateRandomString(12)
		else :
			password = self.__params["sshPassword"]
		salt = self.generateRandomString(10)
		passwordEncrypted = "--password '{0}'".format(crypt.crypt(password, '$6${0}'.format(salt)))

		self.__createUser(self.__params["shell"],passwordEncrypted)
		self.executeShellCommand("mkdir "+self.__params["documentRoot"])

		if self.__params["protocol"] == "sftp" :
			self.executeShellCommand("usermod -a -G sftpjail "+self.__params["account"])

		return self.__createConfTemplate.format(self.__params["ip"],self.__params["account"],password,self.__params["protocol"])

	def delete(self):
		self.executeShellCommand("pkill -u "+self.__params["account"])
		self.__deleteUser()
		return ""