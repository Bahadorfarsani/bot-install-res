from pyrogram import Client
from pyromod import listen

API_ID = 20885533
API_HASH = "93c1785d9928bfdaaac6321c6fbdbb32"
TOKEN = "7748305001:AAEEsPpqPePhLxeyu22hUOBelLuVm6INu50"
plugins = dict(root="plugins")
app = Client(name="test", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN, plugins=plugins)
app.run()
