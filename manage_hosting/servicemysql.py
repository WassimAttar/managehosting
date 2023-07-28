# coding: utf-8

import re

try:
	import MySQLdb
except ImportError:
	print("Please install MySQLdb")
	exit()

class Mysql() :

	__mysqlConfFile = "/root/.my.cnf"

	__createConfTemplate = """
Base de données :
http://{0}/phpmyadmin/
login : {1}
pass : {2}
"""

	def __init__ (self,params,Linux) :
		self.__params = params
		self.__Linux = Linux
		self.__createMysqlInstance()

	def __del__(self):
		try :
			self.mysqlInstance.close()
		except :
			pass

	def __createMysqlInstance(self) :
		mysqlRootPassword = self.__getMysqlRootPassword()
		self.mysqlInstance = MySQLdb.connect(host="localhost",user="root",password=mysqlRootPassword)

	def __getMysqlRootPassword(self) :
		try :
			file = open(Mysql.__mysqlConfFile, 'r')
		except IOError :
			print("Please create {}".format(Mysql.__mysqlConfFile))
			exit()
		content = file.read()
		file.close()
		try :
			return(re.findall('password=(.*)', content)[0])
		except IndexError :
			print("""Please enter mysql root password in {0} file.
Example :
[client]
password=p4ssw0rD
Protect this file
chmod 600 {0}""".format(Mysql.__mysqlConfFile))
			exit()

	def executeSqlRequest(self,query) :
		if self.__params["verbose"] :
			print(query)
		if self.__params["execute"] :
			try :
				cursor = self.mysqlInstance.cursor()
				cursor.execute(query)
				result = cursor.fetchone()
			except :
				result = None
		if result == None :
			return False
		else :
			return True

	def exist(self):
		query = "select User from mysql.user where User = '{0}'".format(self.__params["account"])
		if self.executeSqlRequest(query) :
			return "mysql user {0} already exists\n".format(self.__params["account"])
		return ""

	def create(self) :
		if self.__params["sqlPassword"] == "" :
			mysqlPassword = self.__Linux.generateRandomString(12)
		else :
			mysqlPassword = self.__params["sqlPassword"]
		queries = ("CREATE USER '{0}'@'localhost' IDENTIFIED BY '{1}'",
                    "GRANT USAGE ON * . * TO '{0}'@'localhost' IDENTIFIED BY '{1}' WITH MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0 MAX_USER_CONNECTIONS 0",
                    "CREATE DATABASE IF NOT EXISTS `{0}`",
                    "GRANT ALL PRIVILEGES ON `{0}` . * TO '{0}'@'localhost'")
		for query in queries :
			query = query.format(self.__params["account"],mysqlPassword)
			self.executeSqlRequest(query)

		return Mysql.__createConfTemplate.format(self.__params["ip"],self.__params["account"],mysqlPassword)

	def delete(self) :
		queries = ("DROP USER '{0}'@'localhost'",
                    "DROP DATABASE IF EXISTS `{0}`")
		for query in queries :
			query = query.format(self.__params["account"])
			self.executeSqlRequest(query)
		return ""
