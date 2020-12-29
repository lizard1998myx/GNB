from nonebot import on_command, CommandSession
from aiocqhttp.exceptions import Error as CQHttpError


@on_command('testing', aliases=('baba', 'caonimabi'))
async def weather(session: CommandSession):
    # 从会话状态（session.state）中获取城市名称（city），如果当前不存在，则询问用户
    city = session.get('city', prompt='你想查询哪个城市的天气呢？')
    # 获取城市的天气预报
    weather_report = city
    try:
        bot = session.bot
        id = await bot.send_group_msg(group_id=585805134, message='hello')
        await bot.send_private_msg(user_id=315887212, message='你好～')
        await bot.delete_msg(**id)
    except CQHttpError:
        pass
    # 向用户发送天气预报
    await session.send(weather_report)
    print(str(session.event))


    """
    <Event, {'font': 0, 'message': [{'type': 'text', 'data': {'text': 'bj'}}],
             'message_id': 524052666, 'message_type': 'private', 'post_type': 'message', 
             'raw_message': 'bj', 'self_id': 1976787406, 
             'sender': {'age': 0, 'nickname': 'Sgt.Lizard', 'sex': 'unknown', 'user_id': 315887212},
              'sub_type': 'friend', 'time': 1606727123, 'user_id': 315887212, 'to_me': True}>
    """