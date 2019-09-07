from nonebot import on_command, CommandSession, permission as perm
from nonebot.message import unescape


@on_command('tester', permission=perm.SUPERUSER)
async def say(session: CommandSession):
    print(session.state.get('message'))
    await session.send(
        unescape(session.state.get('message') or session.current_arg))