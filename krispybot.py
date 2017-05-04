import json
import requests

# set global variables
last_update_id_handle = open("last.update","r+")
last_update_id = last_update_id_handle.read().strip() # use strip to remove endline from number
last_update_id = int(last_update_id.split('\x00')[0])
#last_update_id = float(last_update_id)
print last_update_id
bot_token_handle = open("bot.token","r")
bot_token = bot_token_handle.read().strip() # use strip to remove endline from bot token 
telegram_api_url = "https://api.telegram.org/{}/".format(bot_token)


while (True):
	response = requests.get(telegram_api_url + "getUpdates?offset=" + str(last_update_id) + "&timeout=60")
	response = response.content.decode("utf8")
	response = json.loads(response)
	last_update_id = response["result"][0]["update_id"]
	print response["result"][0]
	
	if "message" not in response["result"][0]:
		last_update_id = last_update_id + 1
		last_update_id_handle.seek(0)
		last_update_id_handle.truncate()
		last_update_id_handle.write(str(last_update_id))
	else:
		last_update_id = last_update_id + 1
		last_update_id_handle.seek(0)
		last_update_id_handle.truncate()
		last_update_id_handle.write(str(last_update_id))
		
#print last_update_id 	



#piecemeal this code.  i want to see what the updates look like first and then parse through them so i can write my own function!  wish i had the cloud srver though =(
