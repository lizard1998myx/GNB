import datetime, re, os, send2trash


def str2time(time_str):
    time_lst = re.compile(r'(\d\d\d\d)-(\d\d)-(\d\d).*(\d\d):(\d\d)').search(time_str).groups()
    time = datetime.datetime(year=int(time_lst[0]), month=int(time_lst[1]), day=int(time_lst[2]),
                             hour=int(time_lst[3]), minute=int(time_lst[4]))
    return time


def time2str(time_obj):
    return time_obj.strftime('%Y-%m-%d %a %H:%M')


class Notification(dict):
    def __init__(self, source='', time='', deadline='',
                 category='', description='', abstract='',
                 note='', status=''):
        dict.__init__(self)
        # self['id'] = 0
        self['source'] = source
        self['time'] = time
        self['deadline'] = deadline
        self['category'] = category
        self['description'] = description
        self['abstract'] = abstract
        self['note'] = note
        self['status'] = status
        self.translation = {'source': '发布来源', 'time': '发布时间', 'deadline': '截止时间',
                            'category': '类型', 'description': '描述', 'abstract': '摘要',
                            'note': '笔记', 'status': '状态'}

    def check(self):
        if self['abstract'] == '':
            self['abstract'] = self['description']
        if self['time'] == '':
            self['time'] = time2str(datetime.datetime.now())
        else:
            self['time'] = time2str(str2time(self['time']))
        if self['deadline'] == '':
            self['deadline'] = self['time']
        else:
            self['deadline'] = time2str(str2time(self['deadline']))
        return self

    def editor(self):
        self.check()
        for key in self.keys():
            if key in self.translation.keys():
                key_name = self.translation[key]
            else:
                key_name = key
            value = input(key_name + '[' + self[key] + ']: ').strip()
            if value == "":
                continue
            self[key] = value

    def getmessage(self, keylist, model):
        self.check()
        message = ''
        if len(model) < len(keylist) + 1:
            for i in range(len(keylist) + 1 - len(model)):
                model.append("")
        for i in range(len(keylist)):
            message += model[i] + self[keylist[i]]
        message += model[len(keylist)]
        return message

    def save(self):
        self.check()
        save_message = ""
        for key in self.keys():
            if key in self.translation.keys():
                key_name = self.translation[key]
            else:
                key_name = key
            save_message += key_name + '{' + str(self[key]) + '}\n'
        return save_message


class NotificationCreator():
    def __init__(self):
        self.notification = Notification()

    def by_one(self):
        self.notification.editor()
        return self.notification.check()

    def by_text(self, text):
        for key in self.notification.keys():
            if key in self.notification.translation.keys():
                key_pattern = '((' + key + ')|(' + self.notification.translation[key] + '))'
            else:
                key_pattern = key
            regex = re.compile(key_pattern + r'\{(.*?)\}', re.DOTALL)
            match = regex.search(text)
            if match is None:
                continue
            value = match.groups()[-1]
            self.notification[key] = value
        return self.notification.check()

    def by_msg(self, msg):  # 读取单行输入，由于regex的原因无法换行
        if ('[' in msg or '【' in msg) and (']' in msg or '】' in msg):
            self.notification['category'] = re.compile(r'[\[【](.*)[\]】]').search(msg)[1]
            self.notification['description'] = re.compile(r'[\]】](.*)').search(msg)[1].strip()
        else:
            self.notification['category'] = 'N/A'
            self.notification['description'] = msg
        return self.notification.check()


class NotificationQueue(list):
    def __init__(self, storage="storage"):
        list.__init__(self)
        self._keylist = ['category', 'abstract']
        self._model = ['【', '】', ""]
        self._storage_dir = storage
        self._info_dir = "GNB_info"
        self._index = 0
        if not os.path.exists(self._info_dir):
            os.makedirs(self._info_dir)
        if not os.path.exists(self._storage_dir):
            os.makedirs(self._storage_dir)
        self.info()

    def broadcast(self, keylist, model):
        msg_total = ''
        for notification in self:
            msg = notification.getmessage(keylist=keylist, model=model)
            print(msg)
            msg_total += msg + '\n'
        return msg_total

    def broadcast_default(self):
        return self.broadcast(self._keylist, self._model)

    def inrange(self, index_str):
        if index_str == "":
            print("未输入内容")
            return False
        if index_str.isdigit():
            i = int(index_str)
            if i in range(0, len(self)):
                self._index = i
                return True
            else:
                print("超出范围(0," + str(len(self)) + ")")
                return False
        else:
            print("输入值不合法")
            return False

    def broadcastor(self, index_str=""):
        self.show()
        if index_str == "":
            index_str = input("输入你想发布通知的数字编号/不发布：")
        if self.inrange(index_str):
            msg = self[self._index].getmessage(self._keylist, self._model)
            print(self[self._index].save())
            print(msg)
            return msg

    def show(self):  # display the index and notifications
        if len(self) == 0:
            print("队列为空")
            return "队列为空"
        msg = ""
        for i in range(len(self)):
            msg += self[i].getmessage(keylist=['category', 'source', 'time'],
                                      model=[str(i).ljust(3) + '-[', ']', '|'])
            msg += '\n'
        print(msg)
        return msg

    def editor(self):  # edit an existing notification
        self.show()
        if self.inrange(input("输入你想修改通知的数字编号/不修改：")):
            print(self[self._index].save())
            self[self._index].editor()

    def remover(self):  # remove a notification
        self.show()
        if self.inrange(input('输入你想删除的通知的数字编号/不删除： ')):
            self.pop(self._index)

    def recent_public(self):  # select notifications published in 7 days
        new_notq = NotificationQueue('rec_p')
        for notification in self:
            if str2time(notification['deadline']) < datetime.datetime.now():
                continue
            elif str2time(notification['time']) > (datetime.datetime.now()-datetime.timedelta(days=7)):  # 如果在七天内
                new_notq.append(notification)
        return new_notq

    def recent_deadline(self):  # select notifications published in 7 days
        new_notq = NotificationQueue('rec_d')
        for notification in self:
            if str2time(notification['deadline']) > datetime.datetime.now():
                if str2time(notification['deadline']) < (datetime.datetime.now()+datetime.timedelta(days=7)):  # 如果在七天内
                    new_notq.append(notification)
        return new_notq

    def empty(self, dir=""):  # 清空目录下的所有文件
        if dir == "":
            dir = self._storage_dir
        for textfile in os.listdir(dir):
            filepath = os.path.join(dir, textfile)
            if '.txt' in filepath:
                send2trash.send2trash(filepath)

    def save(self, dir=""):  # 先清空，再将内容保存到仓库里，以index命名文件
        if dir == "":
            dir = self._storage_dir
        self.empty(dir)
        for i in range(len(self)):
            filepath = os.path.join(dir, str(i) + '.txt')
            with open(filepath, 'w') as savefile:
                savefile.write(self[i].save())

    def load(self, dir=""):  # 读取目录信息，如果从仓库提取，则先清空自己
        if dir == "":
            dir = self._storage_dir
            self.__init__(self._storage_dir)
        for textfile in os.listdir(dir):
            filepath = os.path.join(dir, textfile)
            with open(filepath) as loadfile:
                self.append(NotificationCreator().by_text(loadfile.read()))
        return

    def info(self):
        version = "GNB_V2.0.0_20190902"
        description = """Full name: Group Notification Broadcasting
能够方便地与nonebot进行交互
还要修改存档名
还需要放入帮助信息
by myx"""
        filepath = os.path.join(self._info_dir, version + '.txt')
        with open(filepath, 'w') as infofile:
            infofile.write(description)
        with open(os.path.join(self._info_dir, 'example.txt'), "w") as examplefile:
            examplefile.write("通知信息举例：\n" + Notification().save())


if __name__ == "__main__":
    notq = NotificationQueue()
    notq.load()
    notq.broadcast_default()
    print("读取完毕！")
    while True:
        command = input('Enter command [Edit, Add, addbyMsg, Remove, Load, Show, Broadcast, Quit]:')
        if len(command) == 0 or command[0].lower() == 'q':
            break
        elif command[0].lower() == 'e':
            notq.editor()
        elif command[0].lower() == 'r':
            notq.remover()
        elif command[0].lower() == 'b':
            notq.broadcastor()
        elif command[0].lower() == 'l':
            notq.load()
        elif command[0].lower() == 's':
            notq.show()
        elif command[0].lower() == 'a':
            notq.append(NotificationCreator().by_one())
        elif command[0].lower() == 'm':
            notq.append(NotificationCreator().by_msg(input("输入通知信息：\n")))
    notq.save()

    input("进程结束！")
