import re, os


class Notification(dict):
    def __init__(self, source='', time='', deadline='',
                 category='', description='', abstract='',
                 note='', status=''):
        dict.__init__(self)
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


class NotificationCreater():
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
        self.insert(0, notification)

    def broadcast(self, keylist, model):
        for notification in self:
            print(notification.getmessage(keylist=keylist, model=model))

    def broadcast_default(self):
        self.broadcast(self._keylist, self._model)

    def show(self):
        for i in range(len(self)):
            print(self[i].getmessage(keylist=['category', 'source', 'time'],
                                     model=[str(i).ljust(3)+'-[' , ']', '|']))

    def editor(self):
        self.show()
        while True:
            index = input('输入你想修改的通知的数字编号： ')
            if index == "":
                break
            elif index.isdigit():
                i = int(index)
                if i >= 0 and i < len(self):
                    self[i].editor()
                else:
                    print("超出修改范围")
            else:
                print("输入值不合法")


    def save(self):
        for i in range(len(self)):
            filepath = os.path.join(self._save_dir, str(i)+'.txt')
            with open(filepath,'w') as savefile:
                savefile.write(self[i].save())

    def load(self):
        for textfile in os.listdir(self._load_dir):
            filepath = os.path.join(self._load_dir, textfile)
            with open(filepath) as loadfile:
                loadfile.read()

    def info(self):
        version = "GNB_V1.0_20190831"
        description = "Full name: Group Notification Broadcasting"
        description += "by myx"
        filepath = os.path.join(self._info_dir, version + '.txt')
        with open(filepath, 'w') as infofile:
            infofile.write(description)
        with open(os.path.join(self._info_dir, 'example.txt'), "w") as examplefile:
            examplefile.write(Notification().save())


if __name__ == "__main__":
    notq = NotificationQueue()
    notq = load
