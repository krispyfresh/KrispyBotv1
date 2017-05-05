import json
import requests
import sys
import random

# open files
try:
	last_update_id_handle = open("last.update","r+")
except:
	sys.exit("Could not open last.update.  Stopping KrispyBot...")
try:
	bot_token_handle = open("bot.token","r")
except:
	sys.exit("Could not open bot.token.  Please paste your bot token into the bot.token file.  Stopping KrispyBot...")
try:
	imgur_api_key_handle = open("imgur.key","r")
except:
	sys.exit("Could not find imgur API key in imgur.key.  Stopping KrispyBot...")

# set global variables	
last_update_id = last_update_id_handle.read().strip()								# use strip to remove endline from number
bot_token = bot_token_handle.read().strip() 										# use strip to remove endline from bot token 
imgur_api_key = imgur_api_key_handle.read().strip()
last_update_id = int(last_update_id.split('\x00')[0])								# remove null characters that are showing up in the file
telegram_api_url = "https://api.telegram.org/{}/".format(bot_token)
imgur_api_url = "https://api.imgur.com/3/"
last_update_id = 0

#  main loop:  keep looping and getting messages as they come in
while (True):
	response = requests.get(telegram_api_url + "getUpdates?offset=" + str(last_update_id) + "&timeout=60")
	response = response.content.decode("utf8")
	response = json.loads(response)

	
	for i in range(0,len(response["result"])):
		last_update_id = response["result"][i]["update_id"] + 1
		#last_update_id_handle.seek(0)
		#last_update_id_handle.truncate()
		#last_update_id_handle.write(str(last_update_id))

		if "message" in response["result"][i]:  									# is there a message?
			message = response["result"][i]["message"]
			if "entities" in message:												# entities key will only exist if this is a bot command (at least, that's all i care about)
				if message["entities"][0]["type"] == "bot_command": 				# is this a bot_command?
					bot_command_length = message["entities"][0]["length"]			# store a bunch of info about the bot command that was received
					bot_offset = message["entities"][0]["offset"]
					bot_command_raw = message["text"]
					
					if bot_command_raw.startswith("/random"):
						query = bot_command_raw[bot_command_length:].strip()
						imgur_header = {"Authorization": "Client-ID " + imgur_api_key}
						imgur_response = requests.get(imgur_api_url + "gallery/r/" + query,headers=imgur_header )
						
						if(imgur_response.status_code == 200):
							response_content = imgur_response.json()
							num_of_responses = len(response_content["data"])
							chat_id = str(message["chat"]["id"])
							if(num_of_responses == 0):
								post_response = requests.post(telegram_api_url + "sendMessage?chat_id=" + chat_id + "&text=We ain't found shit")
							else:
								random_number = random.randint(0,num_of_responses - 1)
								post_response = requests.post(telegram_api_url + "sendMessage?chat_id=" + chat_id + "&text=" + response_content["data"][random_number]["link"])

					if bot_command_raw.startswith("/search"):
						query = bot_command_raw[bot_command_length:].strip()
						imgur_header = {"Authorization": "Client-ID " + imgur_api_key}
						imgur_response = requests.get(imgur_api_url + "gallery/search/?q=" + query,headers=imgur_header )
						
						if(imgur_response.status_code == 200):
							response_content = imgur_response.json()
							num_of_responses = len(response_content["data"])
							chat_id = str(message["chat"]["id"])
							if(num_of_responses == 0):
								post_response = requests.post(telegram_api_url + "sendMessage?chat_id=" + chat_id + "&text=We ain't found shit")
							else:
								random_number = random.randint(0,num_of_responses - 1)
								post_response = requests.post(telegram_api_url + "sendMessage?chat_id=" + chat_id + "&text=" + response_content["data"][random_number]["link"])

					
					
			#print message
		else:
			print "received something other than a message"
			print response["result"][i]


