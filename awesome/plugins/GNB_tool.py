from nonebot import on_command, CommandSession
import GNB, re


@on_command('GNB_broadcast', aliases=('发布', '公告', '发布公告'))  # OLD plugin, 交互式发布消息
async def GNB_broadcast(session: CommandSession):
    notq = GNB.NotificationQueue()
    notq.load()
    await session.send(notq.broadcast_default())
    await session.send(notq.show())
    index = session.get('index', prompt='你想发布哪个通知呢？')
    await session.bot.send_group_msg(group_id=855360487, message=notq.broadcastor(index))


@on_command('GNB_record', aliases=('记录', ))  # OLD plugin, 交互式记录信息
async def GNB_record(session: CommandSession):
    notq = GNB.NotificationQueue()
    notq.load()
    msg = session.get('msg', prompt='您想记录的通知信息是？')
    notq.append(GNB.NotificationCreator().by_msg(msg))
    notq.save()
    await session.send(notq.broadcast_default())
    await session.send(notq.show())


@on_command(('GNB'), aliases=('通知', '通知工具箱'))  # New plugin, 统一交互窗口
async def GNB_tool(session: CommandSession):
    if session.ctx['user_id'] not in [315887212]:  # 权限设定
        return
    notq = GNB.NotificationQueue()
    notq.load()
    mode = session.get('mode', prompt='请选择模式（显示/广播/编辑/删除/记录）')
    if mode in ['show', 'display', 'list', 'ls', 'view', '显示', '查看']:  # 自定义格式显示完全信息模式
        notq = GNB.NotificationQueue()
        notq.load()
        # await session.send(notq.broadcast_default())  # 显示所有信息，已屏蔽
        if 'format' in session.state.keys():
            await session.send(notq.show(session.state['format']))
        else:
            await session.send(notq.show())
    elif mode in ['broadcast', 'send', '广播', '发布']:  # 自定义格式发布单个通知
        index = session.get('index', prompt='你想发布哪个通知呢？')
        if notq.inrange(index_str=index):
            if 'format' in session.state.keys():
                msg = notq.broadcastor(index, session.state['format'])
            else:
                msg = notq.broadcastor(index)  # 单个通知
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
    elif mode in ['record', 'add', '加入', '记录', '录入']:  # 简单录入模式
        rec_msg = session.get('content', prompt='要输入的内容是？')
        notq.append(GNB.NotificationCreator().by_msg(rec_msg))
        notq.save()
        await session.send('已执行【录入】操作')
    elif mode in ['rec-p', 'recent', '最近发布', '最近']:  # 自定义格式，近七天发布的通知
        if 'format' in session.state.keys():
            msg = '==近七天发布的通知==\n' + notq.recent_public().broadcast(session.state['format'])
        else:
            msg = '==近七天发布的通知==\n' + notq.recent_public().broadcast()
        await session.send('群发内容是：\n' + msg)
        confirm = session.get('confirm', prompt='你确定【发布】吗？')
        if confirm == True or (confirm in ['确定', '是的', '是', 'Yes', 'yes', 'y', 'Y']):
            await session.bot.send_group_msg(group_id=855360487, message=msg)
            await session.send('已执行【群发】操作')
        else:
            await session.send('未确认，操作取消')
    elif mode in ['rec-d', 'DDL', 'soon', '即将截止', '截止', '临近']:  # 自定义格式，近七天截止的通知
        if 'format' in session.state.keys():
            msg = '==七天内截止的通知==\n' + notq.recent_public().broadcast(session.state['format'])
        else:
            msg = '==七天内截止的通知==\n' + notq.recent_public().broadcast()
        await session.send('群发内容是：\n' + msg)
        confirm = session.get('confirm', prompt='你确定【发布】吗？')
        if confirm == True or (confirm in ['确定', '是的', '是', 'Yes', 'yes', 'y', 'Y']):
            await session.bot.send_group_msg(group_id=855360487, message=msg)
            await session.send('已执行【群发】操作')
        else:
            await session.send('未确认，操作取消')
    elif mode in ['help', 'h', '帮助', '说明']:
        help_info = """Group Notification Broadcasting 控制中心 V2.1.1
【使用指南】可以先启用工具箱，按提示逐步操作。也可以在初始命令中输入参数，空格分开。
【可用参数】
1.“--mode”模式设定，可选ls、rm、send、edit、add、recent、soon、help等
2.“纯数字”指标设定，在发布、编辑和删除单个通知时启用
3.“%key”键值设定，在编辑通知时启用，格式串中键值也是这样定义的（但是格式串里可以用中文和缩写）
4.“yes”或“-y”确定值设定，不建议启用，启用时将跳过发布、修改信息的确认环节
5.“##…##”格式串设定，在发布和显示信息使启用（允许中间插入空格）
6.有自定义参数时，不符合上述格式的参数会被视为内容（只保留一个），在修改、录入时启用
【模式说明】
1.查看全部（'show', 'display', 'list', 'ls', 'view', '显示', '查看'），支持自定义格式
2.群发指定信息（'broadcast', 'send', '广播', '发布'），自定义格式发布特定通知
3.编辑信息（'edit', '编辑', '修改'），给定指标、键、值信息，修改通知中的特定信息，注意格式
4.删除信息（'remove', 'rm', 'delete', '删除', '移除'），给定指标，删除指定通知
5.简易录入信息（'record', 'add', '加入', '记录', '录入'），简单地录入信息，只修改类型和描述，无法换行
6.群发最近发布的通知（'rec-p', 'recent', '最近发布', '最近'），群发近七天发布且未截止的通知，支持自定义格式
7.群发即将结束的通知（'rec-d', 'DDL', 'soon', '即将截止', '截止', '临近'），群发近七天截止的通知，支持自定义格式"""
        await session.send(help_info)
    else:
        await session.send('无效模式，尝试输入GNB --help查看帮助')

@GNB_tool.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        await session.send('==GNB控制中心==')
        if stripped_arg:
            # 第一次运行参数不为空，意味着用户直接将一串设置跟在命令名后面，作为参数传入
            # 例如用户可能发送了：通知工具箱 --修改 0 %来源 UCAS
            regex = re.compile(r'##(.*)##')  # 寻找格式说明，贪心匹配模式
            while regex.search(stripped_arg):  # 如果找到格式说明部分
                session.state['format'] = regex.search(stripped_arg)[1]  # 设定格式
                stripped_arg = stripped_arg.replace(regex.search(stripped_arg)[0], '')  # 清除格式设定部分
            for arg in stripped_arg.split(' '):
                if arg == "":
                    continue
                if arg in ['yes', '-y']:
                    session.state['confirm'] = True
                    continue
                if re.match(r'--.*', arg):
                    session.state['mode'] = arg[2:]
                elif arg.isdigit():
                    session.state['index'] = arg
                elif re.match(r'%.*', arg):
                    session.state['key'] = arg[1:]
                else:
                    session.state['content'] = arg
            if list(session.state.keys()) == ['content']:  # 如果仅有内容一项，可能输入有误
                session.state.pop('content')
        return

    if not stripped_arg:
        # 用户没有发送有效的参数（而是发送了空白字符），则提示重新输入
        # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
        session.pause('参数不能为空，请重新输入')

    # 如果当前正在向用户询问更多信息，且用户输入有效，则放入会话状态
    session.state[session.current_key] = stripped_arg
