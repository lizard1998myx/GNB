from nonebot import on_command, CommandSession
from aiocqhttp import Error as CQHttpError
from aiocqhttp.message import escape
import re
from aip import AipOcr

APP_ID = '20026985'
API_KEY = 'PAP6P0ZW4lE6MQ8W1a9L3Hn2'
SECRET_KEY = 'W2UWoOdotLDVCVGqgwyxUhPBhe075tPy'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


@on_command('image_repeat')
async def image_repeat(session: CommandSession):
    reply = session.get('image', prompt='waiting image transmission')
    if 'CQ:image' in reply and re.search(r'file=(.+?)[,|&#|\]]', reply):
        filename = re.search(r'file=(.+?)[,|&#|\]]', reply)[1]
        get_image_result = await session.bot.get_image(file=filename)
        await session.send('[CQ:image,file=%s]' % get_image_result['url'])
        await session.send('[debug]\n%s' % str(get_image_result))
    else:
        await session.send('[debug] image not received')
        await session.send(escape(reply))
        await session.send(reply)


@on_command('OCR')
async def image_ocr(session: CommandSession):
    reply = session.get('image', prompt='waiting image transmission')
    if 'CQ:image' in reply and re.search(r'file=(.+?)[,|&#|\]]', reply):
        filename = re.search(r'file=(.+?)[,|&#|\]]', reply)[1]
        get_image_result = await session.bot.get_image(file=filename)
        results = client.basicGeneralUrl(url=get_image_result['url'])['words_result']
        string = ''
        for result in results:
            string += result['words']
        await session.send(string)
    else:
        await session.send('[debug] image not received')
        await session.send(escape(reply))
        await session.send(reply)