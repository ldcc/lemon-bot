from nonebot import on_command
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.message import Message
from nonebot.adapters.cqhttp.event import MessageEvent, GroupMessageEvent
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me
from nonebot.typing import T_State

import src.plugins as cfg

auths = 'allow - 允许管理员权限\ndrop - 撤销管理员权限'
set_auth = on_command('管理员设置', rule=to_me(), permission=SUPERUSER)

features = '- 色图\n- 防撤回\n- 戳一戳\n- 偷闪照'
switch_on = on_command('功能开启', aliases={'功能启动', '启动功能', '开启功能'})
switch_off = on_command('功能关闭', aliases={'关闭功能'})


@set_auth.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.get_message()).strip()
    if msg == '':
        await bot.finish(message=f'格式错误，参考输出\n{auths}')
    pair = msg.split(' ', 1)
    state['instruct'] = pair[0].strip()
    if len(pair) == 2:
        state['uin'] = pair[1]


@set_auth.got('uin', prompt='请输入 uin')
async def _(bot: Bot, state: T_State):
    instruct = state['instruct']
    uin = str(state['uin']).strip()
    ret = await cfg.set_manager(uin, instruct == 'allow')
    await set_auth.finish(message=('设置' + '成功' if ret else '失败'))


@switch_on.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    if str(event.user_id) in cfg.managers:
        key = event.get_message()
        if key:
            state['switch_on'] = key
    else:
        await switch_on.finish('你没有该权限')


@switch_on.got('switch_on', prompt=f'请输入要开启的功能：\n{features}')
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    key = str(state['switch_on']).strip()
    if key in '色图' and str(bot.self_id) in cfg.supersuers:
        await switch_on.finish()
    if key in 'r18' and str(event.user_id) not in cfg.supersuers:
        await switch_on.finish(f'摇了我吧，爷8想蹲局子')
    ret = await cfg.set_switcher(event.group_id, key, True)
    await switch_on.finish(message=Message(ret))


@switch_off.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    key = event.get_message()
    if key:
        state['switch_off'] = key


@switch_off.got('switch_off', prompt=f'请输入要关闭的功能：\n{features}')
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    key = str(state['switch_off']).strip()
    ret = await cfg.set_switcher(event.group_id, key, False)
    await switch_on.finish(message=Message(ret))
