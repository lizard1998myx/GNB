from nonebot import on_command, CommandSession
from aiocqhttp import Error as CQHttpError
import random


@on_command('at_from_list')
async def at_from_list(session: CommandSession):
    group_id = int(session.get('group_id', prompt='getting group id'))
    namelist = session.get('name_list', prompt='getting name list').split(' ')
    group_member_list = await session.bot.get_group_member_list(group_id=group_id)
    message = ''
    for name in namelist:
        user_not_found = True
        for member in group_member_list:
            if name in member['card']:
                message += '[CQ:at,qq=%i]' % member['user_id']
                user_not_found = False
        if user_not_found:
            message += '%s(not matched)' % name
    message += session.get('notice', prompt='getting further notice')
    await session.bot.send_msg(group_id=group_id, message=message)


@on_command('random')
async def random_member(session: CommandSession):
    if session.ctx['message_type'] == 'group':
        group_id = session.ctx['group_id']
        group_member_list = await session.bot.get_group_member_list(group_id=group_id)
        # self_id = await session.bot.get_login_info()['user_id']
        self_id = 1976787406
        while True:
            member_id = random.choice(group_member_list)['user_id']
            if member_id != self_id:
                break
        await session.bot.send_msg(group_id=group_id, message='[CQ:at,qq=%i]' % member_id)