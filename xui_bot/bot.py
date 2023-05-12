import json
import os
import telebot
from telebot import types
from main import *
import random
import base64
import qrcode
from datetime import datetime

bot = telebot.TeleBot("6022384510:AAEWaJ5FIqJaSJltlXBq-n2hdizeb", parse_mode="html")



@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	itembtn1 = types.KeyboardButton('لیست کاربران📖')
	itembtn2 = types.KeyboardButton('افزودن کاربر📝')
	itembtn3 = types.KeyboardButton('حذف کاربر🤺')
	markup.add(itembtn1, itembtn2, itembtn3)
	bot.reply_to(message, "سلام 🫡", reply_markup=markup)


@bot.message_handler(commands=['admin'])
def add_admin(message):
	config_data = json.loads(open("./config.json", "r").read())
	servers = json.loads(open("./servers.json", "r").read())

	if message.chat.id == config_data['main_admin']:
		#======================================
		if message.text.split(" ")[1] == "new":
			if message.text.split(" ")[3] in servers['list']:
				new_admin = message.text.split(" ")[2]
				if not new_admin in config_data['admin_list']:
					config_data['admin_list'].append(new_admin)
				config_data[new_admin] = {
					"server": message.text.split(" ")[3],
					"limit": int(message.text.split(" ")[4]),
					"number": 0
				}
				new_config_data = open("./config.json", "w")
				new_config_data.write(
					json.dumps(config_data)
				)
				new_config_data.close()
				user_list = open(f'./users/{new_admin}.json', "w")
				user_list.write(json.dumps({
					"remarks": [],
					"ports": []
				}))
				user_list.close()
				bot.reply_to(message, "success:)")
			else:
				bot.reply_to(message, "server not fund!")
		#=====================================
		if message.text.split(" ")[1] == "list":
			config_data = json.loads(open("./config.json", "r").read())
			msg = ""
			for user in config_data['admin_list']:
				msg = msg + user + " ====> " + str(config_data[user]) + "\n"
			bot.reply_to(message, msg)
		#=====================================
		if message.text.split(" ")[1] == "del":
			config_data = json.loads(open("./config.json", "r").read())
			username = message.text.split(" ")[2]
			if username in config_data['admin_list']:
				del config_data[username]
				config_data['admin_list'].remove(username)
				new_config_data = open("./config.json", "w")
				new_config_data.write(
					json.dumps(config_data)
				)
				new_config_data.close()
				os.remove(f'./users/{username}.json')
				bot.reply_to(message, "success:)")
			else:
				bot.reply_to(message, "admin not fund.")



def add_new_user(remark):
	chat_id = remark.chat.id
	config_data = json.loads(open("./config.json", "r").read())
	servers = json.loads(open("./servers.json", "r").read())
	username = remark.chat.username
	server_name = config_data[username]["server"]
	servers = servers[server_name]
	remark = remark.text
	res = add(server_name, remark)
	uuid_s = res['random_id']
	timeing = datetime.fromtimestamp(res['time'] / 1000)
	if res == "login error":
		bot.send_message(chat_id, "login error")
	if res["server_res"]['success']:
		user_list = json.loads(open(f'./users/{username}.json', "r").read())
		ir_port = 0
		while True:
			test_port = random.randrange(1000, 50000)
			if not test_port in user_list['ports']:
				ir_port = test_port
				break
		add_tunnel(servers['ir'], servers['eu'], ir_port, res['port'], remark)

		key_data = '''{
    "add": "IPPPPPP",
    "aid": "0",
    "host": "",
    "id": "IDDDDDD",
    "net": "tcp",
    "path": "",
    "port": "PORTTTTTT",
    "ps": "MARKKKKKK",
    "scy": "auto",
    "sni": "",
    "tls": "",
    "type": "none",
    "v": "2"
}'''.replace("IPPPPPP", servers['ir']).replace("IDDDDDD", uuid_s).replace("MARKKKKKK", remark).replace("PORTTTTTT", str(ir_port))
		key = base64.b64encode(str(key_data).encode("utf-8"))
		key = "vmess://" + key.decode("utf-8") 
		user_list['remarks'].append(remark)
		user_list['ports'].append(ir_port)
		user_list[remark] = {
			"ir_port": ir_port,
			"eu_port": res['port'],
			"ir_ip": servers['ir'],
			"eu_ip": servers['eu'],
			"key": key,
			"time": str(timeing)
		}
		new_user_list = open(f'./users/{username}.json', "w")
		new_user_list.write(json.dumps(user_list))
		new_user_list.close()

		config_data[username]["number"] = config_data[username]["number"] + 1
		new_config_data = open("./config.json", "w")
		new_config_data.write(json.dumps(config_data))
		new_config_data.close()

		img = qrcode.make(key)
		img.save(f'{uuid_s}.png')
		image = open(f'{uuid_s}.png', "rb")
		caption = f'name: <b>{remark}</b>\ntime: <b>{timeing}</b>\n\nkey: <code>{key}</code>'
		bot.send_photo(chat_id, image, caption=caption)
		os.remove(f'{uuid_s}.png')
		bot.send_message(config_data['main_admin'], f'new user ==> {remark} ==> {username}')
	else:
		bot.send_message(chat_id, res["server_res"]['msg'])



def del_user(remark):
	chat_id = remark.chat.id
	config_data = json.loads(open("./config.json", "r").read())
	servers = json.loads(open("./servers.json", "r").read())
	username = remark.chat.username
	server_name = config_data[username]["server"]
	servers = servers[server_name]
	remark = remark.text
	user_list = json.loads(open(f'./users/{username}.json', 'r').read())
	if not remark in user_list['remarks']:
		bot.send_message(chat_id, "user not fund")
		return
	
	eu_port = user_list[remark]["eu_port"]
	del_tunnel(servers['ir'], servers['eu'], eu_port)

	xid = 0
	ulist = list(servers['eu'] + ":" + servers['eu_port'])['obj']
	for user in ulist:
		if remark == user['remark']:
			xid = user['id']
	
	delete(servers['eu'] + ":" + servers['eu_port'], xid)

	user_list['remarks'].remove(remark)
	user_list['ports'].remove(user_list[remark]['ir_port'])
	del user_list[remark]
	new_user_list = open(f'./users/{username}.json', 'w')
	new_user_list.write(json.dumps(user_list))
	new_user_list.close()

	config_data[username]["number"] = config_data[username]["number"] - 1
	new_config_data = open("./config.json", "w")
	new_config_data.write(json.dumps(config_data))
	new_config_data.close()

	bot.send_message(chat_id, "user deleted")
	bot.send_message(config_data['main_admin'], f'del user ==> {remark} ==> {username}')




@bot.message_handler(func=lambda m: True)
def echo_all(message):
	if message.text == "لیست کاربران📖":
		try:
			username = message.chat.username
			config_data = json.loads(open("./config.json", "r").read())
			if username in config_data['admin_list']:
				user_list = json.loads(open(f'./users/{username}.json', 'r').read())
				msg = ''
				for user in user_list['remarks']:
					timeing = user_list[user]['time']
					key = user_list[user]['key']
					msg = msg + f'<b>{user}</b> \ntime: {timeing}\nkey: <code>{key}</code>\n\n=============================\n\n'
				bot.reply_to(message, msg)
		except:
			bot.reply_to(message, "error")

	elif message.text == "افزودن کاربر📝":
		try:
			username = message.chat.username
			config_data = json.loads(open("./config.json", "r").read())
			if username in config_data['admin_list']:
				if not config_data[username]["number"] >= config_data[username]["limit"]:
					sent = bot.reply_to(message, "لطفا نام کانکشن را وارد نمایید🦖")
					bot.register_next_step_handler(sent, add_new_user)
				else:
					bot.reply_to(message, "add user limited")
		except:
			bot.reply_to(message, "error")

	elif message.text == "حذف کاربر🤺":
		try:
			username = message.chat.username
			config_data = json.loads(open("./config.json", "r").read())
			if username in config_data['admin_list']:
				sent = bot.reply_to(message, "لطفا نام کانکشن را وارد نمایید🦖")
				bot.register_next_step_handler(sent, del_user)
		except:
			bot.reply_to(message, "error")



bot.infinity_polling()
