# coding: utf-8

import crypt

class Sftp :

	__documentRootVar = "/var/www/"

	__createConfTemplate = """
sftp :
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
		if self.__params["sftpPassword"] == "" :
			sftpPassword = self.__Linux.generateRandomString(12)
		else :
			sftpPassword = self.__params["sftpPassword"]
		salt = self.__Linux.generateRandomString(10)
		sftpPasswordEncrypted = "--password '{0}'".format(crypt.crypt(sftpPassword, '$6${0}'.format(salt)))

		self.__Linux.createUser("/bin/false",sftpPasswordEncrypted)
		self.__Linux.executeShellCommand("usermod -a -G sftpjail "+self.__params["account"])
		self.__Linux.executeShellCommand("chown -R root:root "+self.__params["openBaseDir"])
		self.__Linux.executeShellCommand("chmod 755 -R "+self.__params["openBaseDir"])
		self.__Linux.executeShellCommand("mkdir "+self.__params["documentRoot"])
		self.__Linux.executeShellCommand("chmod 711 -R "+self.__params["documentRoot"])

		if self.__params.get("domain") == "" :
			self.__Linux.executeShellCommand("ln -s "+self.__params["documentRoot"]+" "+Sftp.__documentRootVar+self.__params["account"])

		return Sftp.__createConfTemplate.format(self.__params["ip"],self.__params["account"],sftpPassword)

	def delete(self):
		self.__Linux.executeShellCommand("pkill -u "+self.__params["account"])
		self.__Linux.executeShellCommand("unlink "+self.__params["openBaseDir"])
		self.__Linux.deleteUser()
		return ""
