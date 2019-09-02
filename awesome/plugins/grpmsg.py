from nonebot import on_command, CommandSession


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
                await session.bot.send_group_msg(group_id=group['group_id'], message='群发测试')
            elif group['group_id']==625122280:
                await session.bot.send_group_msg(group_id=group['group_id'], message='hello world')