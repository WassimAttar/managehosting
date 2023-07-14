# coding: utf-8

import os

try:
	import certbot
except ImportError:
	print("Please install certbot")
	exit()

class Apache2() :

	__apacheConfPath = "/etc/apache2/sites-available/"

	__apacheTemplate = """
<VirtualHost  *:80>
    ServerAdmin 132049@free.fr
    DocumentRoot {0}
    ServerName {2}
    ErrorLog /var/log/apache2/{1}_error.log
    CustomLog /var/log/apache2/{1}_access.log combined
    {3}

    AssignUserId {1} {1}
    php_admin_value open_basedir "{4}/:/tmp/"

   <Directory {0}>
     Options -Indexes
     AllowOverride All
     Require all granted
    </Directory>

  <DirectoryMatch "{0}/(cache|upload)/">
    php_flag engine off
  </DirectoryMatch>

</VirtualHost>
"""

	__apacheTemplateNoDomain = """
<Directory {0}>
  AssignUserId {1} {1}
  php_admin_value open_basedir "{2}/:/tmp/"

  Options -Indexes
  AllowOverride All
  Require all granted
</Directory>

<DirectoryMatch "{0}/(cache|upload)/">
  php_flag engine off
</DirectoryMatch>
"""

	def __init__(self,params,Linux):
		self.__exist = False
		self.__params = params
		self.__Linux = Linux
		if self.__params["domain"] == "" :
			self.__confFile = self.__params["account"]
		else :
			self.__confFile = self.__params["domain"]
		self.__apacheConfFile = self.__confFile+".conf"
		self.__apacheConfFileHttps = self.__confFile+"-le-ssl.conf"

	def __del__(self):
		if self.__params["action"] != "" and self.__params["execute"] and not self.__exist :
			self.__reloadApache()

	def __enableVhostApache(self) :
		self.__Linux.executeShellCommand("a2ensite "+self.__apacheConfFile)

	def __disableVhostApache(self) :
		self.__Linux.executeShellCommand("a2dissite "+self.__apacheConfFile)
		self.__Linux.executeShellCommand("a2dissite "+self.__apacheConfFileHttps)

	def __reloadApache(self) :
		self.__Linux.executeShellCommand("systemctl reload apache2")

	def exist(self):
		if os.path.exists(self.__apacheConfPath+self.__apacheConfFile) :
			self.__exist = True
			return "Apache conf file {0} already exists\n".format(self.__apacheConfFile)
		else :
			return ""

	def create(self) :
		if self.__params["withwww"] :
			serverAlias = "ServerAlias www."+self.__params["domain"]
		else :
			serverAlias = ""

		self.__Linux.executeShellCommand("mkdir "+self.__params["documentRoot"])

		if self.__params["domain"] == "" :
			apacheConf = Apache2.__apacheTemplateNoDomain.format(self.__params["documentRoot"],self.__params["account"],self.__params["openBaseDir"])
		else :
			apacheConf = Apache2.__apacheTemplate.format(self.__params["documentRoot"],self.__params["account"],self.__params["domain"],serverAlias,self.__params["openBaseDir"])
		if self.__params["verbose"] :
			print(apacheConf)
		if self.__params["execute"] :
			file = open(self.__apacheConfPath+self.__apacheConfFile, 'w')
			file.write(apacheConf)
			file.close()
		self.__enableVhostApache()

		if self.__params["withhttps"] :
			cmd = "certbot -n --apache -d "+self.__params["domain"]
			if self.__params["withwww"] :
				cmd += "-d www."+self.__params["domain"]
			self.__Linux.executeShellCommand(cmd)

		return ""

	def delete(self) :
		self.__disableVhostApache()
		self.__Linux.executeShellCommand("rm "+self.__apacheConfPath+self.__apacheConfFile)
		self.__Linux.executeShellCommand("rm "+self.__apacheConfPath+self.__apacheConfFileHttps)
		self.__Linux.executeShellCommand("certbot delete -n --cert-name "+self.__params["domain"])
		return ""