from nonebot import on_command, CommandSession
from GNB_nonebot.info_search import get_info_list, get_total_list, search_name
from aiocqhttp import Error as CQHttpError
import datetime


@on_command('search', aliases=('搜索',))
async def catch_info(session: CommandSession):
    message_type = session.ctx['message_type']
    user_id = session.ctx['user_id']
    #判断发送的消息是私聊的，并且发送的qq号码是12345678
    if message_type == 'private' and user_id == 315887212:
        name = session.get('name', prompt='想搜索学生的姓名？')
        student_list = search_name(infolist=get_total_list(), name=name)
        student_list += search_name(infolist=get_info_list(), name=name)
        if len(student_list) == 0:
            await session.send('not found')
        for student in student_list:
            await session.send(str(student))
    else:
        try:
            await session.send('permission denied')
        except CQHttpError:
            pass


@on_command('joke', aliases=('录入',))
async def record_joke(session: CommandSession):
    content = '== %s ==\n\n%s\n\n' % (datetime.datetime.now().strftime("%Y-%m-%d | %H:%M:%S"),
                                      session.get('content', prompt='笑话的内容？'))
    with open('joke.txt', 'a+') as f:
        f.write(content)
    await session.send('loaded')
    await session.send(content)