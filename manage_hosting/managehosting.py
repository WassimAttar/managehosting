# coding: utf-8

import argparse, socket

from servicelinux import Linux
from servicemysql import Mysql
from servicessh import Ssh
from servicesftp import Sftp
from serviceapache2 import Apache2
from rights import Rights
from displayconf import DisplayConf
from update import Update
from version import __version__

parser = argparse.ArgumentParser(description='Create Hosting')
parser.add_argument('-a','--account', type=str, default="", help='linux, mysql, path atc... accounts')
parser.add_argument('-dn', '--domain', type=str, default="", help='Domain name')
parser.add_argument('-v', '--verbose', action='count', default=0, help='Verbosity')
parser.add_argument('-e', '--execute', action='count', default=0, help='Execute command')
parser.add_argument('-c', '--create', action='count', default=0, help='Create Hosting')
parser.add_argument('-d', '--delete', action='count', default=0, help='Delete Hosting')
parser.add_argument('-n', '--withsql', action='count', default=0, help='With Sql')
parser.add_argument('-sp', '--sqlpassword', type=str, default="", help='Sql Password')
parser.add_argument('-sf', '--withsftp', action='count', default=0, help='With Sftp')
parser.add_argument('-sfp', '--sftppassword', type=str, default="", help='Sftp Password')
parser.add_argument('-s', '--withssh', action='count', default=0, help='With Ssh')
parser.add_argument('-ssp', '--sshpassword', type=str, default="", help='Ssh Password')
parser.add_argument('-ht', '--withhttps', action='count', default=0, help='With Https')
parser.add_argument('-w', '--withwww', action='count', default=0, help='Add server alias www')
parser.add_argument('-U', '--update', action='store_true', help='Update')
parser.add_argument('-V', '--version', action='store_true', help='Version')
args = parser.parse_args()

if args.version :
	print(__version__)
	exit()

if (args.domain == "" or args.account == "") and (args.create > 0 or args.delete > 0) :
	print("Please choose --account and --domain")
	exit()

if args.withsftp > 0 and args.withssh > 0 and args.create > 0 :
	print("Please choose --withsftp or --withssh")
	exit()

if args.withsftp == 0 and args.withssh == 0 and args.create > 0 :
	print("Please choose a hosting option. Ex : --withsftp")
	exit()

if args.create == 0 and args.delete == 0 and args.update == False :
	print("Please choose an action. Ex : --create")
	exit()


params = {}
params["version"] = __version__
params["account"] = args.account
params["domain"] = args.domain

if args.verbose == 0 :
	params["verbose"] = False
else :
	params["verbose"] = True
if args.execute == 0 :
	params["execute"] = False
else :
	params["execute"] = True
	params["verbose"] = True

if args.withwww == 0 :
	params["withwww"] = False
else :
	params["withwww"] = True

if args.withhttps == 0 :
	params["withhttps"] = False
else :
	params["withhttps"] = True

if args.sqlpassword == "" :
	params["sqlPassword"] = ""
else :
	params["sqlPassword"] = args.sqlpassword

if args.sshpassword == "" :
	params["sshPassword"] = ""
else :
	params["sshPassword"] = args.sshpassword

if args.sftppassword == "" :
	params["sftpPassword"] = ""
else :
	params["sftpPassword"] = args.sftppassword

if args.withssh > 0 or args.withsftp > 0 or args.delete > 0 :
	params["openBaseDir"] = "/home/"+params["account"]
	params["documentRoot"] = params["openBaseDir"]+"/www"

if args.withssh > 0 :
	params["rightsCommands"] = ["chown {account}:{account} -R {openBaseDir}","chmod -R 700 {openBaseDir}"]
if args.withsftp > 0 :
	params["rightsCommands"] = ["chown -R root:root {openBaseDir}", "chmod 755 -R {openBaseDir}", "chmod 711 -R {documentRoot}",
	             "chown {account}:{account} -R {documentRoot}"]


if args.create > 0 :
	params["action"] = "create"

if args.delete > 0 :
	params["action"] = "delete"

if args.update :
	params["execute"] = True

params["ip"] = [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]


services = []

linuxInstance = Linux(params)
services.append(linuxInstance)

if args.update :
	updateInstance = Update(params)
	updateInstance.update()
	exit()

if args.withsql > 0 or args.delete > 0 :
	mysqlInstance = Mysql(params,linuxInstance)
	services.append(mysqlInstance)

if args.withsftp > 0 or args.delete > 0 :
	sftpInstance = Sftp(params,linuxInstance)
	services.append(sftpInstance)

if args.withssh > 0 or args.delete > 0 :
	sshInstance = Ssh(params,linuxInstance)
	services.append(sshInstance)

rightsInstance = Rights(params,linuxInstance)
apache2Instance = Apache2(params,linuxInstance)
services.append(apache2Instance)
displayInstance = DisplayConf(params)
services.append(rightsInstance)

if args.create > 0 :
	display = ""
	for service in services :
		display += getattr(service,"exist")()
	if display != "" :
		print(display)
		exit()

display = ""
for service in services :
	display += getattr(service,params["action"])()

print(getattr(displayInstance,params["action"])(display))


if args.execute == 0 :
	print("Dry run")