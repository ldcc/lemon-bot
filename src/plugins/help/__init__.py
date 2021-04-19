from nonebot import on_command
from nonebot.adapters.cqhttp import Event, Bot

help = on_command('help', aliases={'帮助'})


@help.handle()
async def _(bot: Bot, event: Event):
    await help.finish('1.发送 [武器] 查看今日武器材料和武器\n'
                      '2.发送 [天赋] 查看今日天赋材料和人物\n'
                      '3.发送 [周本] 查看周本材料和人物\n'
                      '4.发送 [武器资料<空格>武器名] 查看武器资料\neg. 武器资料 狼末\n'
                      '5.发送 [角色资料<空格>角色名] 查看角色资料\neg. 角色资料 琴\n'
                      '6.发送 [哪有素材名] 查找素材资源在大地图的位置\neg. 哪有甜甜花\n'
                      '7.发送 [丘丘翻译<空格>丘丘语句] 翻译丘丘语\neg. 丘丘翻译 biadam\n'
                      '8.发送 [丘丘词典<空格>丘丘语句] 查询丘丘语的单词含义\neg. 丘丘词典 kucha pupu')
