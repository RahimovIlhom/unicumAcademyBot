from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str('TOKEN')
ADMINS = env.list('ADMINS')
BOT_ID = env.int('BOT_ID')
