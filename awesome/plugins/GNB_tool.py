from nonebot import on_command, CommandSession
import GNB, re


@on_command('GNB_broadcast', aliases=('发布', '公告', '发布公告'))
async def GNB_broadcast(session: CommandSession):
    notq = GNB.NotificationQueue()
    notq.load()
    await session.send(notq.broadcast_default())
    await session.send(notq.show())
    index = session.get('index', prompt='你想发布哪个通知呢？')
    await session.bot.send_group_msg(group_id=855360487, message=notq.broadcastor(index))


@on_command('GNB_record', aliases=('记录', ))
async def GNB_record(session: CommandSession):
    notq = GNB.NotificationQueue()
    notq.load()
    msg = session.get('msg', prompt='您想记录的通知信息是？')
    notq.append(GNB.NotificationCreator().by_msg(msg))
    notq.save()
    await session.send(notq.broadcast_default())
    await session.send(notq.show())


@on_command(('GNB'), aliases=('通知','通知工具箱'))
async def GNB_tool(session: CommandSession):
    if session.ctx['user_id'] not in [315887212]:
        return
    notq = GNB.NotificationQueue()
    notq.load()
    mode = session.get('mode', prompt='请选择模式（显示/广播/编辑/删除/记录）')
    if mode in ['show', 'display', 'list', 'ls', '显示']:  # 显示信息模式（应该可以修改格式、index）
        notq = GNB.NotificationQueue()
        notq.load()
        await session.send(notq.broadcast_default())
        await session.send(notq.show())
    elif mode in ['broadcast', 'send', '广播', '发布']:
        index = session.get('index', prompt='你想发布哪个通知呢？')
        if notq.inrange(index_str=index):
            msg = notq.broadcastor(index)
            await session.send('广播内容是：\n' + msg)
            confirm = session.get('confirm', prompt='你确定【发布】吗？')
            if confirm == True or (confirm in ['确定', '是的', '是', 'Yes', 'yes', 'y', 'Y']):
                await session.bot.send_group_msg(group_id=855360487, message=msg)
                await session.send('已执行【发布】操作')
            else:
                await session.send('未确认，操作取消')
    elif mode in ['edit', '编辑', '修改']:
        index = session.get('index', prompt='你想修改哪个通知呢？')
        if notq.inrange(index_str=index):
            i = int(index)
            key = session.get('key', prompt='要修改的标签是（英文）？')
            if key in notq[i].keys():
                value = session.get('content', prompt='要改成的内容是？')
                await session.send('要将第'+index+'个通知的（'+key+'）改为：\n'+value)
                confirm = session.get('confirm', prompt='你确定【修改】吗？')
                if confirm == True or (confirm in ['确定', '是的', '是', 'Yes', 'yes', 'y', 'Y']):
                    notq[i][key]=value
                    notq.save()
                    await session.send('已执行【修改】操作')
                else:
                    await session.send('未确认，操作取消')
    elif mode in ['remove', 'rm', 'delete', '删除', '移除']:
        index = session.get('index', prompt='你想删除哪个通知呢？')
        if notq.inrange(index_str=index):
            confirm = session.get('confirm', prompt='你确定【删除】吗？')
            if confirm == True or (confirm in ['确定', '是的', '是', 'Yes', 'yes', 'y', 'Y']):
                notq.pop(int(index))
                notq.save()
                await session.send('已执行【删除】操作')
            else:
                await session.send('未确认，操作取消')
    elif mode in ['record', 'add', '加入', '记录', '录入']:
        rec_msg = session.get('content', prompt='要输入的内容是？')
        notq.append(GNB.NotificationCreator().by_msg(rec_msg))
        notq.save()
        await session.send('已执行【录入】操作')
    elif mode in ['rec-p', 'recent', '最近发布', '最近']:
        msg = '==近七天发布的通知==\n' + notq.recent_public().broadcast_default()
        await session.send('群发内容是：\n' + msg)
        confirm = session.get('confirm', prompt='你确定【发布】吗？')
        if confirm == True or (confirm in ['确定', '是的', '是', 'Yes', 'yes', 'y', 'Y']):
            await session.bot.send_group_msg(group_id=855360487, message=msg)
            await session.send('已执行【群发】操作')
        else:
            await session.send('未确认，操作取消')
    elif mode in ['rec-d', 'DDL', 'soon', '即将截止', '截止', '临近']:
        msg = '==七天内截止的通知==\n' + notq.recent_public().broadcast_default()
        await session.send('群发内容是：\n' + msg)
        confirm = session.get('confirm', prompt='你确定【发布】吗？')
        if confirm == True or (confirm in ['确定', '是的', '是', 'Yes', 'yes', 'y', 'Y']):
            await session.bot.send_group_msg(group_id=855360487, message=msg)
            await session.send('已执行【群发】操作')
        else:
            await session.send('未确认，操作取消')


@GNB_tool.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        await session.send('==GNB控制中心==')
        if stripped_arg:
            # 第一次运行参数不为空，意味着用户直接将一串设置跟在命令名后面，作为参数传入
            # 例如用户可能发送了：GNB --edit 0 :来源 UCAS
            for arg in stripped_arg.split(' '):
                if arg in ['yes', '-y']:
                    session.state['confirm'] = True
                if re.match(r'--.*', arg):
                    session.state['mode'] = arg[2:]
                elif arg.isdigit():
                    session.state['index'] = arg
                elif re.match(r':.*', arg):
                    session.state['key'] = arg[1:]
                else:
                    session.state['content'] = arg
        return

    if not stripped_arg:
        # 用户没有发送有效的参数（而是发送了空白字符），则提示重新输入
        # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
        session.pause('参数不能为空，请重新输入')

    # 如果当前正在向用户询问更多信息，且用户输入有效，则放入会话状态
    session.state[session.current_key] = stripped_arg
