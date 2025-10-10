from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
import os
import logging

# Импортируем из основного файла
from bot import bot, dp, main

async def on_startup(bot):
    await bot.set_webhook(f"https://your-app-name.onrender.com/webhook")

async def on_shutdown(bot):
    await bot.delete_webhook()

def create_app():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    webhook_requests_handler.register(app, path="/webhook")
    setup_application(app, dp, bot=bot)
    
    return app

if __name__ == "__main__":
    app = create_app()
    web.run_app(app, host="0.0.0.0", port=10000)