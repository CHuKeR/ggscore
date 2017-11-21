import SQLighter
import dota_parser_lib
from time import sleep


if __name__ == "__main__":
    sqler = SQLighter.DotaSqlClient()
    dp = dota_parser_lib.dota_parser(sqler)
    dp.update_matches()
    sqler.close()
    print('Update DB from cron')

