import json
import requests
import sys

# open files
try:
	last_update_id_handle = open("last.update","r+")
except:
	sys.exit("Could not open last.update.  Stopping KrispyBot...")
try:
	bot_token_handle = open("bot.token","r")
except:
	sys.exit("Could not open bot.token.  Please paste your bot token into the bot.token file.  Stopping KrispyBot...")

# set global variables	
last_update_id = last_update_id_handle.read().strip() # use strip to remove endline from number
bot_token = bot_token_handle.read().strip() # use strip to remove endline from bot token 
last_update_id = int(last_update_id.split('\x00')[0]) # remove null characters that are showing up in the file
telegram_api_url = "https://api.telegram.org/{}/".format(bot_token)

#  main loop:  keep looping and getting messages as they come in
while (True):
	response = requests.get(telegram_api_url + "getUpdates?offset=" + str(last_update_id) + "&timeout=60")
	response = response.content.decode("utf8")
	response = json.loads(response)
	print response["result"][0]
	
	for i in range(0,len(response["result"])):
		last_update_id = response["result"][i]["update_id"] + 1
		last_update_id_handle.seek(0)
		last_update_id_handle.truncate()
		last_update_id_handle.write(str(last_update_id))

		if response["result"][i]["message"] != None:
			print "received a message!"
		else:
			print "received something other than a message"

	

