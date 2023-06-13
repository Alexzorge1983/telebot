from aiogram.utils import executor
from settings.bot_config import dp
from handlers import client, psyholog,admin




client.register_handlers_client(dp)
psyholog.register_handlers_psyholog(dp)
admin.register_handlers_admin(dp)
# post.register_handlers_posts(dp)



# run long-polling
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)