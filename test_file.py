import SQLighter
import telebot
import config
import time

tic = time.time()
string = '{"ok":false,"error_code":400,"description":"Bad Request: chat not found"}'
lol = eval(string.replace("false","False"))
print(lol["description"])
time.sleep(2)
toc = time.time()
print(toc-tic)
