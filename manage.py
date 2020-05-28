from src.api.app import create_app
from src.bot.handlers import *

app = create_app()
app.run(host='0.0.0.0')