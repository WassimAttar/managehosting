# coding: utf-8

import crypt

class Ssh :

	__hostingPath = "/home/"

	__createConfTemplate = """
ssh :
ip : {0}
login : {1}
pass : {2}
"""

	def __init__ (self,params,Linux) :
		self.__params = params
		self.__Linux = Linux

	@staticmethod
	def getHostingPath(account) :
		return "{0}{1}".format(Ssh.__hostingPath,account)

	def exist(self):
		return ""

	def create(self):
		sshPassword = self.__Linux.generateRandomString(12)
		salt = self.__Linux.generateRandomString(10)
		password = "--password '{0}'".format(crypt.crypt(sshPassword, '$6${0}'.format(salt)))
		self.__Linux.createUser("/bin/bash",password)
		return Ssh.__createConfTemplate.format(self.__params.get('ip'),self.__params.get('account'),sshPassword)

	def delete(self):
		self.__Linux.deleteUser()
		return ""
