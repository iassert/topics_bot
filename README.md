# topics_bot

It is a telegram bot for receiving and replying to private messages 

if you have any questions, write to me in telegram
[@static_assert](https://t.me/static_assert)

## Table of Contents
- [Installation](#installation)
- [Setting](#setting)
- [Run](#run)

<a name="installation"></a>
## Installation
* instruction for Ubuntu20

- Download Python3.10
```sh
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.10
python3.10 --version
```

- Download Docker
```sh
sudo apt update
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
sudo apt update
apt-cache policy docker-ce
sudo apt install docker-ce
sudo systemctl status docker
```

- Download [telegram-bot-api](https://github.com/tdlib/telegram-bot-api#dependencies)
```sh
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install make git zlib1g-dev libssl-dev gperf cmake clang-10 libc++-dev libc++abi-dev
git clone --recursive https://github.com/tdlib/telegram-bot-api.git
cd telegram-bot-api
rm -rf build
mkdir build
cd build
CXXFLAGS="-stdlib=libc++" CC=/usr/bin/clang-10 CXX=/usr/bin/clang++-10 cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX:PATH=.. ..
cmake --build . --target install
cd ../..
ls -l telegram-bot-api/bin/telegram-bot-api*
```

- Download a project
```sh
git clone --recursive https://github.com/iassert/topics_bot.git
```

- Install python lib
```sh
pip install -r requirements.txt
```

<a name="setting"></a>
## Setting

- in [@BotFather](https://t.me/BotFather) get a token
- write your token in ./config.py

- move service
```
sudo mv telegram-bot-api.service /etc/systemd/system/
sudo mv topics_bot.service /etc/systemd/system/

sudo systemctl daemon-reload

sudo systemctl enable telegram-bot-api
sudo systemctl enable topics_bot
```

- run docker-compose
```
docker-compose up -d
```

- write WSL host in ./config.py
```sh
ifconfig
```

<a name="run"></a>
## Run

```sh
sudo systemctl start telegram-bot-api
sudo systemctl start topics_bot
```

