from datetime import datetime
from weather_source_bs4 import Beijing_weather
import nonebot
import pytz
from aiocqhttp.exceptions import Error as CQHttpError


@nonebot.scheduler.scheduled_job('cron', hour='*')
async def _():
    bot = nonebot.get_bot()
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    try:
        await bot.send_group_msg(group_id=230697355,
                                  message=f'现在{now.hour}点整啦！')
        await bot.send_group_msg(group_id=230697355, message='[tester]' + Beijing_weather())
        if now.hour == 23:
            msg = '夜深了。辛苦了一天，大家晚安！:)\n' + Beijing_weather()
            await bot.send_group_msg(group_id=230697355, message=msg)
        if now.hour == 6:
            msg = '又是元气满满的一天，这里为大家准备了近期的天气预报o(*￣▽￣*)ブ\n' + Beijing_weather()
            await bot.send_group_msg(group_id=230697355, message='[tester]'+msg)
            await bot.send_group_msg(group_id=625122280, message='天文系的扛把子们早上好！' + msg)
            await bot.send_group_msg(group_id=855360487, message='天文和环科的小伙伴们早~ ' + msg)
    except CQHttpError:
        pass

# 加入定时报天气功能
