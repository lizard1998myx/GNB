from nonebot import on_command, CommandSession
import GNB


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
    notq = GNB.NotificationQueue()
    notq.load()
    notq.append(GNB.NotificationCreator().by_msg(msg))
    notq.save()
    await session.send(notq.broadcast_default())
    await session.send(notq.show())
