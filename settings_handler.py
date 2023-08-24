from configparser import ConfigParser
import os
appName="askFor"
cpath=os.path.join(os.getenv('appdata'),appName,"settings.ini")
if not os.path.exists(os.path.join(os.getenv('appdata'),appName)):
	os.mkdir(os.path.join(os.getenv('appdata'),appName))
if not os.path.exists(cpath):
	config = ConfigParser() 
	config.add_section("g")
	config["g"]["lang"] = "en"
	config["g"]["qu"] = "https://mesteranas.github.io/mesteranas/askFor/catagories/geography.html"
	with open(cpath, "w",encoding="utf-8") as file:
		config.write(file)

def get(section,key):
	config = ConfigParser()
	config.read(cpath)
	value = config[section][key]
	return value


def set(section,key, value):
		config = ConfigParser()
		config.read(cpath)
		config[section][key] = value
		with open(cpath, "w",encoding="utf-8") as file:
			config.write(file)

