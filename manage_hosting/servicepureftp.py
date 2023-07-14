# coding: utf-8
try:
	import pysodium
except ImportError:
	print("Please install pysodium")
	exit()


class Pureftp() :

	__pureftpDatabase = "pureftpd"

	__createConfTemplate = """
ftp :
ip : {0}
login : {1}
pass : {2}
"""

	def __init__(self,params,Mysql,Linux) :
		self.__params = params
		self.__Linux = Linux
		self.__Mysql = Mysql
		try :
			self.__Mysql.mysqlInstance.select_db(Pureftp.__pureftpDatabase)
		except	:
			print("Unknown database 'pureftpd'")
			exit()
		self.__cursor = self.__Mysql.mysqlInstance.cursor()

	def __pureftpHostingPathExists(self) :
		return self.__Mysql.executeSqlRequest(self.__cursor,"select Dir from users where Dir = '{0}'".format(self.__params["openBaseDir"]))

	def __pureftpUserExists(self) :
		return self.__Mysql.executeSqlRequest(self.__cursor,"select User from users where User = '{0}'".format(self.__params["account"]))

	def exist(self):
		display = ""
		if self.__pureftpHostingPathExists() :
			display +=  "ftp hosting path {0} already exists\n".format(self.__params["openBaseDir"])
		if self.__pureftpUserExists() :
			display +=  "ftp user {0} already exists\n".format(self.__params["account"])
		return display

	def create(self) :
		self.__Linux.createUser("/bin/false","")
		self.__Linux.executeShellCommand("rm {0}/.bash_logout {0}/.bashrc {0}/.profile".format(self.__params["openBaseDir"]))
		try:
			if self.__params["ftpPassword"] == "" :
				pureftpPassword = self.__Linux.generateRandomString(12)
			else :
				pureftpPassword = self.__params["ftpPassword"]

			pureftpPasswordEncrypted = pysodium.crypto_pwhash_scryptsalsa208sha256_str(bytes(pureftpPassword, 'utf-8'), 32768, 16777216).decode('utf-8')[:-1]

			uid = self.__Linux.getUid()
			query = """INSERT INTO `users` ( `User` , `Password` , `Uid` , `Gid` , `Dir` )
									VALUES ('{0}', '{1}' , '{2}', '{2}', '{3}');""".format(self.__params["account"],pureftpPasswordEncrypted,uid,self.__params["openBaseDir"])
			if self.__params["verbose"] :
				print(query)
			if self.__params["execute"] :
				self.__cursor.execute(query)
		except KeyError:
			if self.__params["verbose"] :
				print('Linux user {0} not created, can\'t create ftp user {0} yet\n'.format(self.__params["account"]))
		return Pureftp.__createConfTemplate.format(self.__params["ip"],self.__params["account"],pureftpPassword)

	def delete(self) :
		query = """DELETE FROM `users` WHERE `User`= '{0}' and `Dir`='{1}';
						""".format(self.__params["account"],self.__params["openBaseDir"])
		if self.__params["verbose"] :
			print(query)
		if self.__params["execute"] :
			self.__cursor.execute(query)
		return ""