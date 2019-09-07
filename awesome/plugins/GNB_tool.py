from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from jieba import posseg
import GNB, re


@on_command(('GNB'), aliases=('通知', '通知工具箱'))  # New plugin, 统一交互窗口
async def GNB_tool(session: CommandSession):
    if session.ctx['user_id'] not in [315887212]:  # 权限设定
        QQ_groups = [230697355]
        notq = GNB.NotificationQueue(session.ctx['user_id'])
    elif session.ctx['user_id'] == 315887212:
        QQ_groups = [855360487, 230697355]
        notq = GNB.NotificationQueue()
    notq.load()
    mode = session.get('mode', prompt='请选择模式（显示/广播/编辑/删除/记录）')

    if mode in ['show', 'display', 'list', 'ls', 'view', '显示', '查看']:  # 自定义格式显示完全信息模式
        # await session.send(notq.broadcast())  # 显示所有信息，已屏蔽
        print(session.state)
        if 'index' in session.state.keys():
            index = session.state['index']
        else:
            index = '-1'
        if 'format' in session.state.keys():
            await session.send(notq.show(index=index, format_string=session.state['format']))
        else:
            await session.send(notq.show(index=index))

    elif mode in ['broadcast', 'send', 'post', '广播', '发布']:  # 自定义格式发布单个通知
        index = session.get('index', prompt='你想发布哪个通知呢？')
        if notq.inrange(index_str=index):
            if 'format' in session.state.keys():
                msg = notq.broadcastor(index, session.state['format'])
            else:
                msg = notq.broadcastor(index)  # 单个通知
            await session.send('广播内容是：\n' + msg)
            confirm = session.get('confirm', prompt='你确定【发布】吗？')
            if confirm == True or (confirm in ['确定', '是的', '是', 'Yes', 'yes', 'y', 'Y']):
                for QQ_group_id in QQ_groups:
                    await session.bot.send_group_msg(group_id=QQ_group_id, message=msg)
                    await session.send('已执行【发布】操作（' + str(QQ_group_id) + '）')
            else:
                await session.send('未确认，操作取消')

    elif mode in ['edit', '编辑', '修改']:
        index = session.get('index', prompt='你想修改哪个通知呢？')
        if notq.inrange(index_str=index):
            i = int(index)
            key = session.get('key', prompt='要修改的标签（key）是？')
            value = session.get('content', prompt='要改成的内容（value）是？')
            await session.send('要将第'+index+'个通知的（'+key+'）改为：\n'+value)
            confirm = session.get('confirm', prompt='你确定【修改】吗？')
            if confirm == True or (confirm in ['确定', '是的', '是', 'Yes', 'yes', 'y', 'Y']):
                if notq[i].edit(key, value):
                    notq.save()
                    await session.send('已执行【修改】操作')
                else:
                    await session.send('标签不存在，【修改】失败，请检查输入参数')
            else:
                await session.send('未确认，操作取消')

    elif mode in ['remove', 'rm', 'delete', '删除', '移除']:
        index = session.get('index', prompt='你想删除哪个通知呢？')
        if notq.inrange(index_str=index):
            await session.send('即将删除第' + index + '个通知：\n' + notq.broadcastor(index))
            confirm = session.get('confirm', prompt='你确定【删除】吗？')
            if confirm == True or (confirm in ['确定', '是的', '是', 'Yes', 'yes', 'y', 'Y']):
                notq.pop(int(index))
                notq.save()
                await session.send('已执行【删除】操作')
            else:
                await session.send('未确认，操作取消')
        else:
            await session.send('超出范围，未删除')

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
            for QQ_group_id in QQ_groups:
                await session.bot.send_group_msg(group_id=QQ_group_id, message=msg)
                await session.send('已执行【群发】操作（' + str(QQ_group_id) + '）')
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
            for QQ_group_id in QQ_groups:
                await session.bot.send_group_msg(group_id=QQ_group_id, message=msg)
                await session.send('已执行【群发】操作（' + str(QQ_group_id) + '）')
        else:
            await session.send('未确认，操作取消')

    elif mode in ['help', 'h', '帮助', '说明']:
        help_info = """Group Notification Broadcasting 控制中心 V2.4.1
【使用指南】可以先启用工具箱，按提示逐步操作。也可以在初始命令中输入参数，空格分开。
【可用参数】
1.“--mode”模式设定，可选ls、rm、send、edit、add、recent、soon、help等
2.“纯数字”指标设定，在发布、编辑和删除单个通知时启用
3.“%key”键值设定，在编辑通知时启用，格式串中键值也是这样定义的（但是格式串里可以用中文和缩写）
4.“yes”或“-y”确定值设定，不建议启用，启用时将跳过发布、修改信息的确认环节
5.“##…##”格式串设定，在发布和显示信息使启用（允许中间插入空格，\\n表示换行符）
6.有自定义参数时，不符合上述格式的参数会被视为内容（会被空格分开，且只保留一个），在修改、录入时启用
【模式说明】
1.查看全部（'show', 'display', 'list', 'ls', 'view', '显示', '查看'），支持自定义格式
2.群发指定信息（'broadcast', 'send', 'post', '广播', '发布'），自定义格式发布特定通知
3.编辑信息（'edit', '编辑', '修改'），给定指标、键、值信息，修改通知中的特定信息，注意格式
4.删除信息（'remove', 'rm', 'delete', '删除', '移除'），给定指标，删除指定通知
5.简易录入信息（'record', 'add', '加入', '记录', '录入'），简单地录入信息，只修改类型和描述，无法换行
6.群发最近发布的通知（'rec-p', 'recent', '最近发布', '最近'），群发近七天发布且未截止的通知，支持自定义格式
7.群发即将结束的通知（'rec-d', 'DDL', 'soon', '即将截止', '截止', '临近'），群发近七天截止的通知，支持自定义格式

测试用群：230697355
by mengyuxi16@mails.ucas.ac.cn"""
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


# on_natural_language 装饰器将函数声明为一个自然语言处理器
# keywords 表示需要响应的关键词，类型为任意可迭代对象，元素类型为 str
# 如果不传入 keywords，则响应所有没有被当作命令处理的消息
@on_natural_language(keywords=['GNB', '通知', '通知工具箱', '工具箱'])
async def _(session: NLPSession):
    # 去掉消息首尾的空白符
    stripped_msg = session.msg_text.strip()
    # 对消息进行分词和词性标注
    words = posseg.lcut(stripped_msg)

    arg = ''
    # 遍历 posseg.lcut 返回的列表
    for word in words:
        # 每个元素是一个 pair 对象，包含 word 和 flag 两个属性，分别表示词和词性
        if word.flag == 'm':
            # m 词性表示量词
            regex = re.compile(r'(\d)+')
            if regex.search(word.word):  # 如果搜到了数字
                arg += ' ' + regex.search(word.word).group()
            elif '零' in word.word and chinese2digits(word.word)==0:
                arg += ' 0'
            elif chinese2digits(word.word)!=0:
                arg += ' ' + str(chinese2digits(word.word))
        if word.flag in ['v', 'n']:
            # n,v分别表示名词和动词
            if word.word in ['显示', '查看']:
                arg += ' --show'
            elif word.word in ['广播', '发布']:
                arg += ' --broadcast'
            elif word.word in ['编辑', '修改']:
                arg += ' --edit'
            elif word.word in ['删除', '移除']:
                arg += ' --remove'
            elif word.word in ['加入', '记录', '录入']:
                arg += ' --record'
            elif word.word in ['最近发布', '最近']:
                arg += ' --rec-p'
            elif word.word in ['即将截止', '截止', '临近']:
                arg += ' --rec-d'
            elif word.word in ['帮助', '说明']:
                arg += ' --help'

    # 返回意图命令，前两个参数必填，分别表示置信度和意图命令名
    return IntentCommand(90.0, 'GNB', current_arg=arg)


def chinese2digits(uchars_chinese):
    common_used_numerals_tmp = {'零': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4,
                                '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
                                '百': 100, '千': 1000, '万': 10000, '亿': 100000000}
    # common_used_numerals= dict(zip(common_used_numerals_tmp.values(), common_used_numerals_tmp.keys())) #反转
    total = 0
    r = 1  # 表示单位：个十百千...
    for i in range(len(uchars_chinese) - 1, -1, -1):
        #print(uchars_chinese[i])
        if uchars_chinese[i] in common_used_numerals_tmp.keys():
            val = common_used_numerals_tmp.get(uchars_chinese[i])
            if val >= 10 and i == 0:  # 应对 十三 十四 十*之类
                if val > r:
                    r = val
                    total = total + val
                else:
                    r = r * val
                    # total =total + r * x
            elif val >= 10:
                if val > r:
                    r = val
                else:
                    r = r * val
            else:
                total = total + r * val
    return total
