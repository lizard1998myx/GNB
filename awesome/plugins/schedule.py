from datetime import datetime
from GNB_nonebot.weather_source_bs4 import Beijing_weather, Beijing_weather_Morning, Beijing_weather_Night
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
        weather = Beijing_weather()
        weather_m = Beijing_weather_Morning()
        weather_n = Beijing_weather_Night()
        # await bot.send_group_msg(group_id=230697355, message='[tester]' + weather)
        # await bot.send_group_msg(group_id=230697355, message='[tester]' + weather_m)
        # await bot.send_group_msg(group_id=230697355, message='[tester]' + weather_n)
        if now.hour == 23:
            msg = '夜深了。辛苦了一天，大家晚安！:)'
            # await bot.send_group_msg(group_id=855360487, message=msg)
            # await bot.send_group_msg(group_id=855360487, message=weather_n)
            # await bot.send_group_msg(group_id=625122280, message=msg)
            # await bot.send_group_msg(group_id=625122280, message=weather_n)
            await bot.send_group_msg(group_id=865640538, message=msg)
            await bot.send_group_msg(group_id=865640538, message=weather_n)
            # await bot.send_group_msg(group_id=519698575, message=msg)
            # await bot.send_group_msg(group_id=519698575, message=weather_n)
        if now.hour == 6:
            msg = '这里为大家准备了早上的天气预报o(*￣▽￣*)ブ'
            # await bot.send_group_msg(group_id=625122280, message='天文系的扛把子们早上好！' + msg)
            # await bot.send_group_msg(group_id=625122280, message=weather_m)
            await bot.send_group_msg(group_id=865640538, message='国台的扛把子们早上好！' + msg)
            await bot.send_group_msg(group_id=865640538, message=weather_m)
            # await bot.send_group_msg(group_id=855360487, message='天文和环科的小伙伴们早~ ' + msg)
            # await bot.send_group_msg(group_id=855360487, message=weather_m)
            # await bot.send_group_msg(group_id=519698575, message='小伙伴们早上好！' + msg)
            # await bot.send_group_msg(group_id=519698575, message=weather_m)
    except CQHttpError:
        pass

# 加入定时报天气功能
