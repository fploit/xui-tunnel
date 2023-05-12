# xui-tunnel
Bot to add user to xui panel and create tunnel in secondary server in Telegram bot

### Install dependency
```sh
sudo apt install python3
sudo apt install python3-pip

# After installing Python3 and pip in ubuntu, install the following libraries:

pip install Flask
pip install Flask-Cors
pip install pyTelegramBotAPI
pip install qrcode
pip install uuid
pip install requests

# install openssh and screen by apt in ubuntu
sudo apt install openssh screen -y
```

### add ssh key
<p>Set ssh keys for ssh connection from server1 (tunnel server) to server2 (xui panel server) without needing a password</p>

### edit files
1- edit telegram bot token in ```xui_bot/bot.py''' line 11
<br>
2- set admin bot telegram user id, admin username, server name and server limits in ```xui_bot/config.json```
<br>
3- set server1 (ir) ip, port, username, password and server2 (eu) ip, port in servers.json

### run server1
<p>upload xui_tunnel in server1 and:</p>
```sh
cd xui_tunnel

screen flask run --host=IP
```

### run server2
<p>upload xui_bot in server2 and:</p>
```sh
cd xui_bot

screen python3 bot.py
```
