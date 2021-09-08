@echo OFF
color 70
echo 检测并安装前置文件.....
pip install --upgrade pip
pip install bs4
pip install requests
echo 打开程序
cls
py main.py
pause