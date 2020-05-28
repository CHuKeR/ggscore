from src.api.app import create_app
from src.bot.handlers import *

app = create_app(bot)
app.run(host='0.0.0.0')
