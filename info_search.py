import csv, datetime, difflib


INFO_TABLE = 'GNB_student_info.csv'
# '序号', '培养单位', '姓名', '学号',
# '证件号码', '性别', '出生日期', '民族',
# '楼宇', '房间号', '手机号',
# '专业', '培养层次', '攻读方式', '是否确定导师', '导师姓名'
TOTAL_TABLE = 'GNB_total_info.csv'


def read_csv(filename):
    result = []
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            result.append(row)
    return result


def search_birth(info_list, birth_date_tag='出生日期', name_tag='姓名', split_symble='-', days_pre=2):
    date = datetime.date.today() + datetime.timedelta(days=days_pre)
    result_list = []
    for student in info_list:
        birth_dates = student[birth_date_tag].split(split_symble)
        if date.month == int(birth_dates[1]) and date.day == int(birth_dates[2]):
            result_list.append('%s(%2i-%2i)' % (student[name_tag], date.month, date.day))
    return result_list


def get_info_list(filename=INFO_TABLE):
    return read_csv(filename=filename)


def get_total_list(filename=TOTAL_TABLE):
    return read_csv(filename=filename)


def search_name(infolist, name: str, name_tag='姓名'):
    student_list = []
    max_sim = 0
    for student in infolist:
        sim = cal_sim(name, student[name_tag])
        if sim == 0:
            continue
        elif sim > max_sim:
            max_sim = sim
            student_list = [student]
        elif sim == max_sim:
            student_list.append(student)
    return student_list


def cal_sim(s1, s2):
    if s1 in s2 or s2 in s1:
        return 1.0
    else:
        return difflib.SequenceMatcher(None, s1, s2).quick_ratio()