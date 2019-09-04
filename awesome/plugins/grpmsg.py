from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from weather_source_bs4 import Beijing_weather


@on_command('send_msg', aliases=('群发',))
async def send_msg(session: CommandSession):
    message_type=session.ctx['message_type']
    user_id=session.ctx['user_id']
    #判断发送的消息是私聊的，并且发送的qq号码是12345678
    if message_type=='private' and user_id==315887212:
        #获取qq群的信息
        group_list = await session.bot.get_group_list()
        # group_list = [{'group_id': 230697355, 'group_name': 'Testing'}]
        for group in group_list:
            # 对某个qq群进行发送信息
            if group['group_id']==230697355:
                await session.bot.send_group_msg(group_id=group['group_id'], message=Beijing_weather())
            elif group['group_id']==625122280:
                continue
                await session.bot.send_group_msg(group_id=group['group_id'], message='hello world')


@on_natural_language(keywords={'发', '说', '讲', '唱', '叫'})
async def _(session: NLPSession):
    # 去掉消息首尾的空白符
    stripped_msg = session.msg_text.strip()
    while stripped_msg[0] in ['发', '唱', '说', '讲', '个', '首']:
        stripped_msg = stripped_msg[1:]

    # 返回意图命令，前两个参数必填，分别表示置信度和意图命令名
    return IntentCommand(70.0, 'echo', current_arg=stripped_msg)
