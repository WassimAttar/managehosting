# coding: utf-8

class Rights :

	__rights = "/root/droits.sh"

	def __init__(self,params,Linux) :
		self.__exist = False
		self.__params = params
		self.__Linux = Linux
		self.__rights = Rights.__rights

	def __del__(self):
		if self.__params["action"] == "create" and not self.__exist :
			self.__Linux.executeShellCommand("sh "+self.__rights)

	def exist(self):
		with open(Rights.__rights, "r") as file:
			content = file.read()
		if content.find(self.__params["account"]) != -1 :
			self.__exist = True
			return "Rights {0} already exists\n".format(self.__params["account"])
		else:
			return ""

	def create(self):
		template = ""
		for command in self.__params["rightsCommands"] :
			cmd = command.format(account=self.__params["account"], openBaseDir=self.__params["openBaseDir"], documentRoot=self.__params["documentRoot"])
			template += cmd+"\n"
		if self.__params["verbose"] :
			print(template)
		if self.__params["execute"] :
			with open(Rights.__rights, "a") as file:
				file.write(template+"\n")
		return ""

	def delete(self):
		content = ""
		with open(Rights.__rights, "r") as file:
			lines = file.readlines()
			for line in lines:
				if line.find(self.__params["account"]) == -1 :
					content += line
		with open(Rights.__rights, "w") as file:
			file.write(content)
		return "Rights {0} deleted\n".format(self.__params["account"])