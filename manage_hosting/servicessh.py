# coding: utf-8

import crypt

class Ssh :

	__documentRootVar = "/var/www/"

	__createConfTemplate = """
ssh :
ip : {0}
login : {1}
pass : {2}
"""

	def __init__ (self,params,Linux) :
		self.__params = params
		self.__Linux = Linux

	def exist(self):
		return ""

	def create(self):
		if self.__params["sshPassword"] == "" :
			sshPassword = self.__Linux.generateRandomString(12)
		else :
			sshPassword = self.__params["sshPassword"]
		salt = self.__Linux.generateRandomString(10)
		sshPasswordEncrypted = "--password '{0}'".format(crypt.crypt(sshPassword, '$6${0}'.format(salt)))

		self.__Linux.createUser("/bin/bash",sshPasswordEncrypted)
		self.__Linux.executeShellCommand("mkdir "+self.__params["documentRoot"])

		return Ssh.__createConfTemplate.format(self.__params["ip"],self.__params["account"],sshPassword)

	def delete(self):
		self.__Linux.executeShellCommand("pkill -u "+self.__params["account"])
		self.__Linux.deleteUser()
		return ""
