from nonebot import on_command, CommandSession
from aiocqhttp import Error as CQHttpError
import datetime, os, pyautogui, time


@on_command('reboot')
async def reboot(session: CommandSession):
    # session.ctx['message_type'] == 'private'
    if session.ctx['user_id'] == 315887212:
        i = 0
        while True:
            i += 1
            filename = os.path.join(os.path.abspath('temp'), 'screenshot.jpg')
            pyautogui.screenshot(imageFilename=filename)
            await session.send('[CQ:image,file=file:///%s]' % filename)
            command = session.get('command%i' % i,
                                  prompt='[reboot] auto/yes/no or click/move(%i, %i)' % pyautogui.position())
            if command[0].lower() == 'a':
                await session.send('[reboot] auto initiate')
                pyautogui.moveTo(600, 800)
                pyautogui.click()
                pyautogui.hotkey('ctrl', 'f5')
                time.sleep(3)
                await session.send('[reboot] failed')
            elif command[0].lower() == 'y':  # rerun via hotkey
                await session.send('[reboot] initiate')
                pyautogui.hotkey('ctrl', 'f5')
                time.sleep(3)
                await session.send('[reboot] failed')
            elif command[0].lower() == 'n':
                await session.send('[reboot] exit')
                return
            elif command[0].lower() == 'c':
                pyautogui.click()
                await session.send('[reboot] clicked')
            else:
                try:
                    pyautogui.moveTo(*eval(command))
                    await session.send('[reboot] moved')
                except BaseException:
                    await session.send('[reboot] move failed')
    else:
        await session.send('permission denied')


@on_command('restart_engine', aliases=('restart',))
async def restart_engine(session: CommandSession):
    # session.ctx['message_type'] == 'private'
    if session.ctx['user_id'] == 315887212:
        await session.send('restart engine')
        await session.bot.set_restart()


@on_command('initiate')
async def initiate(session: CommandSession):
    if session.ctx['user_id'] == 315887212:
        await session.send('[initiate] restart engine')
        await session.bot.set_restart()
        pyautogui.moveTo(600, 800)
        pyautogui.click()
        pyautogui.hotkey('ctrl', 'f5')
        time.sleep(5)
        await session.send('[initiate] failed')



@on_command('python')
async def python_code(session: CommandSession):
    if session.ctx['message_type'] == 'private' and session.ctx['user_id'] == 315887212:
        try:
            python_script = session.get('python_script', prompt='waiting python code')
            if '\n' not in python_script:
                await session.send(eval(python_script))
            else:
                filename = os.path.join('temp',
                                        'python_code_%s.py' % datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
                with open(filename, 'w') as f:
                    f.write(python_script)
                try:
                    os.system('python %s' % filename)
                    await session.send('[completed] code in %s' % filename)
                except BaseException:
                    await session.send('[failed to run] code in %s' % filename)
        except CQHttpError:
            pass
    else:
        try:
            await session.send('permission denied')
        except CQHttpError:
            pass


@on_command('command', aliases=('cmd', 'console', 'terminal'))
async def command_line(session: CommandSession):
    bot = session.bot
    functions = {'get_login_info': bot.get_login_info,
                 'get_friend_list': bot.get_friend_list,
                 'get_group_list': bot.get_group_list,
                 'get_group_info': bot.get_group_info,
                 'get_group_member_list': bot.get_group_member_list,
                 'get_group_member_info': bot.get_group_member_info,
                 'send_msg': bot.send_msg,
                 'send_group_msg': bot.send_group_msg,
                 'send_private_msg': bot.send_private_msg,
                 'delete_msg': bot.delete_msg,
                 'set_friend_add_request': bot.set_friend_add_request,
                 'set_group_add_request': bot.set_group_add_request,
                 'set_group_card': bot.set_group_card,
                 'set_group_special_title': bot.set_group_special_title,
                 'set_group_kick': bot.set_group_kick,
                 'set_group_ban': bot.set_group_ban,
                 'set_group_whole_ban': bot.set_group_whole_ban,
                 'set_group_leave': bot.set_group_leave,
                 'set_group_name': bot.set_group_name,
                 'set_restart': bot.set_restart,
                 'get_image': bot.get_image,
                 'get_msg': bot.get_msg,
                 'can_send_image': bot.can_send_image,
                 'can_send_record': bot.can_send_record,
                 'get_status': bot.get_status,
                 'get_version_info': bot.get_version_info}
    if session.ctx['message_type'] == 'private' and session.ctx['user_id'] == 315887212:
        try:
            function_name = session.get('function_name', prompt='waiting function name')
            if function_name in functions.keys():
                kwargs = eval(session.get('kwargs', prompt='waiting kwargs'))
                output = await functions[function_name](**kwargs)
                await session.send(str(output))
            else:
                await session.send('function name not supported')
        except CQHttpError:
            pass
    else:
        try:
            await session.send('permission denied')
        except CQHttpError:
            pass
