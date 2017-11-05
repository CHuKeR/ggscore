import SQLighter
import dota_parser_lib
from time import time


sqler = SQLighter.DotaSqlClient()
sum_time = 0
for i in range(0,10):
    tic = time()
    dp = dota_parser_lib.dota_parser(sqler)
    toc = time()
    sum_time+=toc-tic

print(sum_time)
