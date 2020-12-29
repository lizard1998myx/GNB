from nonebot import on_command, CommandSession
from subcovid import run, login
import os, csv, requests


@on_command('subcovid')
async def subcovid_run(session: CommandSession):
    user = session.get('user', prompt='your email for SEP system')
    passwd = session.get('passwd', prompt="your password")
    to_save_cookie = session.get('save_cookie',
                                 prompt="[experimental] save cookie for daily submission? (without saving password)\n[实验功能]保存cookie进行每日填报，不需要保存密码")
    to_save_account = session.get('save_account',
                                  prompt="[stable] save password for daily submission? (your password WILL BE saved)\n[稳定功能]保存账号密码进行每日填报，注意，你的密码会被保存到服务器上！")
    try:
        run(user=user, passwd=passwd)
    except ValueError as e:
        await session.send('== mission failed (%s)==' % e.__str__())
        if e.__str__() == 'failed to login':
            to_save = False
        else:
            to_save = True
    else:
        await session.send('== mission accomplished ==')
        to_save = True
    saved = False
    if to_save:
        if len(to_save_cookie) > 0:
            if to_save_cookie[0].lower() == 'y' or to_save_cookie[0] == '是':
                save_cookie(cookie=login(s=requests.Session(),
                                         username=user, password=passwd))
                await session.send('cookie saved')
                saved = True
        if len(to_save_account) > 0:
            if to_save_account[0].lower() == 'y' or to_save_account[0] == '是':
                save_account(user=user, passwd=passwd)
                await session.send('account saved')
                saved = True
    if not saved:
        await session.send('your cookie or password will not be saved')


@subcovid_run.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    arg_list = stripped_arg.split(' ')

    if session.is_first_run:
        await session.send('Subcovid plugin, based on https://github.com/IanSmith123/ucas-covid19')
        if len(arg_list) >= 2:
            if '@' in arg_list[0]:
                session.state['user'] = arg_list[0]
                session.state['passwd'] = arg_list[1]
            return

    session.state[session.current_key] = stripped_arg


def save_account(user, passwd):
    with open(os.path.join('..', 'subcovid_list.csv'), 'a+', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['user', 'passwd'])
        writer.writerow({'user': user, 'passwd': passwd})


def save_cookie(cookie: dict):
    with open(os.path.join('..', 'subcovid_cookie_list.csv'), 'a+', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=cookie.keys())
        writer.writerow(cookie)
