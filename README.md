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

# install openssh by apt in ubuntu
sudo apt install openssh -y
```

### add ssh key
<p>Set ssh keys for ssh connection from server1 (tunnel server) to server2 (xui panel server) without needing a password</p>
