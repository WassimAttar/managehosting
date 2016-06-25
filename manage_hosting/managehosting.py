# coding: utf-8

import argparse, socket

from servicelinux import Linux
from servicemysql import Mysql
from servicepureftp import Pureftp
from servicessh import Ssh
from serviceapache2 import Apache2
from rights import Rights
from displayconf import DisplayConf

parser = argparse.ArgumentParser(description='Create Hosting')
parser.add_argument('account', type=str, help='linux, mysql, path atc... accounts')
parser.add_argument('-dn', '--domain', type=str, default="", help='Domain name')
parser.add_argument('-v', '--verbose', action='count', default=0, help='Verbosity')
parser.add_argument('-e', '--execute', action='count', default=0, help='Execute command')
parser.add_argument('-c', '--create', action='count', default=0, help='Create Hosting')
parser.add_argument('-d', '--delete', action='count', default=0, help='Delete Hosting')
parser.add_argument('-n', '--withsql', action='count', default=0, help='With Sql')
parser.add_argument('-f', '--withftp', action='count', default=0, help='With Ftp')
parser.add_argument('-s', '--withssh', action='count', default=0, help='With Ssh')
parser.add_argument('-w', '--withwww', action='count', default=0, help='Add server alias www')
parser.add_argument('-r', '--documentroot', type=str, default="", help='Document Root')
args = parser.parse_args()

if args.withftp == 0 and args.withssh == 0 and args.create > 0 :
	print("Please choose a hosting option. Ex : --withftp")
	exit()

params = {}
params["account"] = args.account

if args.domain == "" :
	params["domain"] = ""
else :
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
if args.documentroot == "" :
	params["documentRoot"] = ""
else :
	params["documentRoot"] = args.documentroot

if args.withftp > 0 :
	params["hostingPath"] = Pureftp.getHostingPath(params.get("account"))

if args.withssh > 0 :
	params["hostingPath"] = Ssh.getHostingPath(params.get("account"))

if args.create > 0 :
	params["action"] = "create"

if args.delete > 0 :
	params["action"] = "delete"

params["ip"] = [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]


services = []

linuxInstance = Linux(params)
services.append(linuxInstance)

if args.withsql > 0 or args.delete > 0 :
	mysqlInstance = Mysql(params,linuxInstance)
	services.append(mysqlInstance)

if args.withftp > 0 or args.delete > 0 :
	if args.withsql == 0 :
		mysqlInstance = Mysql(params,linuxInstance)
	pureftpInstance = Pureftp(params,mysqlInstance,linuxInstance)
	services.append(pureftpInstance)

if args.withssh > 0 or args.delete > 0 :
	sshInstance = Ssh(params,linuxInstance)
	services.append(sshInstance)

rightsInstance = Rights(params,linuxInstance)
apache2Instance = Apache2(params,linuxInstance)
services.append(apache2Instance)
displayInstance = DisplayConf(params)
services.append(rightsInstance)

# pas service : display
# services : linux rights apache2 mysql pureftp ssh

if args.create > 0 :
	display = ""
	for service in services :
		display += getattr(service,"exist")()
	if display != "" :
		print(display)
		exit()

display = ""
for service in services :
	display += getattr(service,params.get("action"))()

print(getattr(displayInstance,params.get("action"))(display))


if args.execute == 0 :
	print("Dry run")