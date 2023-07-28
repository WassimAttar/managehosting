# coding: utf-8

class DisplayConf :

	__createConfTemplate = """
##########################
accès {0}

{1}
{2}
##########################
"""

	__deleteConfTemplate = """
##########################

Compte {1} et Domaine {0} supprimés

##########################
"""

	def __init__ (self,params) :
		self.__params = params

	def create(self,text) :
		if self.__params["withwww"] :
			domain = "www."+self.__params["domain"]
			url = "http://"+domain
		else :
			domain = self.__params["domain"]
			url = "http://"+domain
		return DisplayConf.__createConfTemplate.format(domain,url,text)

	def delete(self,text) :
		conf = DisplayConf.__deleteConfTemplate.format(self.__params["domain"],self.__params["account"])
		conf += text
		return conf
