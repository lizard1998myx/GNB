from nonebot import on_notice, NoticeSession, on_request, RequestSession, on_command, CommandSession
from nonebot.helpers import render_expression as __
from aiocqhttp import Error as CQHttpError

GROUP_GREETING = (
    '欢迎新同学 {name}[]！[CQ:face,id=63][CQ:face,id=63][CQ:face,id=63]',
    '[CQ:face,id=99]欢迎新成员～',
    '欢迎 {name}👏👏～',
    '[CQ:at,qq={user_id}] 欢迎欢迎👏',
)


@on_notice('group_increase')
async def _(session: NoticeSession):
    if session.ctx['group_id'] not in (230697355, 519698575, 865640538):
        return
    try:
        info = await session.bot.get_group_member_info(**session.ctx,
                                                       no_cache=True)
        name = info['card'] or info['nickname'] or '新成员'
        await session.send(__(GROUP_GREETING, name=name, **session.ctx))
    except CQHttpError:
        pass


@on_request('group')
async def _(session: RequestSession):
    if session.ctx['group_id'] == 230697355:
        await session.approve()


@on_command('一键退群', aliases=('退群', '我要退群'))
async def send_msg(session: CommandSession):
    if session.ctx['message_type'] == 'group' and session.ctx['group_id'] in [230697355]:
        try:
            bot = session.bot
            await bot.set_group_kick(group_id=session.ctx['group_id'], user_id=session.ctx['user_id'])
        except CQHttpError:
            pass


@on_command('一键禁言', aliases=('禁言', '我要禁言'))
async def send_msg(session: CommandSession):
    if session.ctx['message_type'] == 'group' and session.ctx['group_id'] in [230697355, 865640538]:
        try:
            bot = session.bot
            await bot.set_group_ban(group_id=session.ctx['group_id'], user_id=session.ctx['user_id'],
                                    duration=60)
        except CQHttpError:
            pass
