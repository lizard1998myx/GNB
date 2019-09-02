import datetime, re, os


class Notification(dict):
    def __init__(self, source='', time='', deadline='',
                 category='', description='', abstract='',
                 note='', status=''):
        dict.__init__(self)
        self['id'] = 0
        self['source'] = source
        self['time'] = time
        self['deadline'] = deadline
        self['category'] = category
        self['description'] = description
        self['abstract'] = abstract
        self['note'] = note
        self['status'] = status
        self.translation = {'source':'发布来源', 'time':'发布时间', 'deadline':'截止时间',
                            'category':'类型', 'description':'描述', 'abstract':'摘要',
                            'note':'笔记', 'status':'状态'}

    def check(self):
        if self['abstract']=='':
            self['abstract'] = self['description']

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
        if len(model) < len(keylist)+1:
            for i in range(len(keylist)+1-len(model)):
                model.append("")
        for i in range(len(keylist)):
            message += model[i] + self[keylist[i]]
        message += model[len(keylist)]
        return message

    def save(self):
        save_message = ""
        for key in self.keys():
            if key in self.translation.keys():
                key_name = self.translation[key]
            else:
                key_name = key
            save_message += key_name + '{' + self[key] + '}\n'
        return save_message


class NotificationCreator():
    def __init__(self):
        self.notification = Notification()

    def by_one(self):
        self.notification.editor()
        return self.notification

    def by_text(self, text):
        for key in self.notification.keys():
            if key in self.notification.translation.keys():
                key_pattern = '(('+ key + ')|(' + self.notification.translation[key] + '))'
            else:
                key_pattern = key
            regex = re.compile(key_pattern + r'\{(.*?)\}', re.DOTALL)
            match = regex.search(text)
            if match is None:
                continue
            value = match.groups()[-1]
            self.notification[key] = value
        return self.notification
        
    def by_msg(self, msg):
        self.notification['category'] = re.compile(r'[\[【](.*)[\]】]').search(msg)[1]
        self.notification['description'] = re.compile(r'[\]】](.*)').search(msg)[1].strip()
        self.time = datetime.datetime.now().strftime('%m-%d %a %H:%M')


class NotificationQueue(list):
    def __init__(self):
        list.__init__(self)
        self._keylist = ['category','abstract']
        self._model = ['【','】',""]
        self._info_dir = "GNB_info"
        self._save_dir = 'GNB_save'
        self._load_dir = 'GNB_load'
        if not os.path.exists(self._info_dir):
            os.makedirs(self._info_dir)
        if not os.path.exists(self._save_dir):
            os.makedirs(self._save_dir)
        if not os.path.exists(self._load_dir):
            os.makedirs(self._load_dir)
        self.info()

    def enqueue(self, notification):
        self.append(notification)

    def broadcast(self, keylist, model):
        for notification in self:
            print(notification.getmessage(keylist=keylist, model=model))

    def broadcast_default(self):
        self.broadcast(self._keylist, self._model)

    def show(self):  # display the index and notifications
        if len(self) == 0:
            print("队列为空")
            return "队列为空"
        msg = ""
        for i in range(len(self)):
            msg += self[i].getmessage(keylist=['category', 'source', 'time'],
                                      model=[str(i).ljust(3)+'-[' , ']', '|'])
            msg += '\n'
        print(msg)
        return msg

    def editor(self):  # edit an existing notification
        self.show()
        index = input('输入你想修改的通知的数字编号/不修改： ')
        if index == "":
            return
        elif index.isdigit():
            i = int(index)
            if i in range(0, len(self)):
                self[i].editor()
            else:
                print("超出修改范围")
        else:
            print("输入值不合法")
    
    def remover(self):  # remove a notification
        self.show()
        index = input('输入你想delete的通知的数字编号/不修改： ')
        if index == "":
            return
        elif index.isdigit():
            i = int(index)
            if i in range(0, len(self)):
                self.pop(i)
            else:
                print("超出修改范围")
        else:
            print("输入值不合法")
            
    def recent_public(self):  # select notifications published in 7 days
        new_notq = NotificationQueue()
        for notification in self:
            if notification['time'] != "":
                new_notq.enqueue(notification)
        return now_notq

    def save(self, dir=""):  # save files in save_dir, named by index
        if dir == "":
            dir = self._save_dir
        for i in range(len(self)):
            filepath = os.path.join(dir, str(i)+'.txt')
            with open(filepath,'w') as savefile:
                savefile.write(self[i].save())

    def load(self, dir=""):  # read files in load_dir
        if dir == "":
            dir = self._load_dir
        for textfile in os.listdir(dir):
            filepath = os.path.join(dir, textfile)
            with open(filepath) as loadfile:
                self.enqueue(NotificationCreator().by_text(loadfile.read()))

    def info(self):
        version = "GNB_V1.1.1_20190902"
        description = """Full name: Group Notification Broadcasting
修复录入后不会存档的问题
未来需要增加删减功能
put the data in one dir
make another dir for history
change log name
use command to switch mode
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
    input("读取完毕！")
    while True:
        command = input('Enter command [Edit, Add, Remove, Loadall, Show, Quit]:')
        if len(command)==0 or command[0].lower()=='q':
            break
        elif command[0].lower()=='e':
            notq.editor()
        elif command[0].lower()=='r':
            notq.remover()
        elif command[0].lower()=='l':
            notq.load()
            notq.load('GNB_save')
        elif command[0].lower()=='s':
            notq.show()
        elif command[0].lower()=='a':
            notq.enqueue(NotificationCreator().by_one())
    notq.save()

    input("进程结束！")
