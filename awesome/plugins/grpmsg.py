from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from GNB_nonebot.weather_source_bs4 import Beijing_weather, Beijing_weather_Morning, Beijing_weather_Night
import nonebot


@on_command('send_msg', aliases=('群发',))
async def send_msg(session: CommandSession):
    message_type = session.ctx['message_type']
    user_id = session.ctx['user_id']
    #判断发送的消息是私聊的，并且发送的qq号码是12345678
    if message_type == 'private' and user_id == 315887212:
        #获取qq群的信息
        group_list = await session.bot.get_group_list()
        # group_list = [{'group_id': 230697355, 'group_name': 'Testing'}]
        weather = Beijing_weather()
        weather_m = Beijing_weather_Morning()
        weather_n = Beijing_weather_Night()
        #session.get('manual', prompt='是否手动发送天气？')
        #if session.state['manual'] == '是':
        if False:
            bot = nonebot.get_bot()
            msg = '这里为大家准备了晨间的天气预报o(*￣▽￣*)ブ\n'
            print(msg)
            await bot.send_group_msg(group_id=625122280, message='天文系的扛把子们早上好！' + msg)
            await bot.send_group_msg(group_id=625122280, message=weather_m)
            await bot.send_group_msg(group_id=855360487, message='天文和环科的小伙伴们早~ ' + msg)
            await bot.send_group_msg(group_id=855360487, message=weather_m)
            await bot.send_group_msg(group_id=519698575, message='小伙伴们早上好！' + msg)
            await bot.send_group_msg(group_id=519698575, message=weather_m)
        for group in group_list:
            # 对某个qq群进行发送信息
            if group['group_id']==230697355:
                await session.bot.send_group_msg(group_id=group['group_id'], message=weather)
                await session.bot.send_group_msg(group_id=group['group_id'], message=weather_m)
                await session.bot.send_group_msg(group_id=group['group_id'], message=weather_n)
            elif group['group_id']==625122280:
                continue
                await session.bot.send_group_msg(group_id=group['group_id'], message='hello world')


"""
@on_natural_language(keywords={'发', '说', '讲', '唱', '叫'})
async def _(session: NLPSession):
    # 去掉消息首尾的空白符
    stripped_msg = session.msg_text.strip()
    while stripped_msg[0] in ['发', '唱', '说', '讲', '个', '首']:
        stripped_msg = stripped_msg[1:]

    # 返回意图命令，前两个参数必填，分别表示置信度和意图命令名
    return IntentCommand(70.0, 'echo', current_arg=stripped_msg)
"""