import base64
import os

from nonebot import require, get_bots, get_driver
from nonebot.adapters.cqhttp import Bot, Message

driver = get_driver()

groups = []
running = False
count = 0
FILE_PATH = r'./src/data/cron'


@driver.on_bot_connect
async def _(bot: Bot):
    global groups
    groups = await bot.get_group_list()


scheduler = require('nonebot_plugin_apscheduler').scheduler


@scheduler.scheduled_job('cron', hour='15', minute='*/16', max_instances=10)
async def _():
    global groups
    for bot_id, bot in get_bots().items():
        for g in groups:
            with open(os.path.join(FILE_PATH, '3.j.jpg'), "rb") as j3:
                pic = base64.b64encode(j3.read()).decode()
                message = Message(f'[CQ:image,file=base64://{pic}]')
                await bot.send_group_msg(group_id=g['group_id'], message=message)


@scheduler.scheduled_job('cron', hour='*', max_instances=10)
async def _():
    global groups
    for bot_id, bot in get_bots().items():
        for g in groups:
            await bot.send_group_msg(group_id=g['group_id'], message='整点报时咕咕咕')
