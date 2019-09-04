from urllib.request import urlopen
from bs4 import BeautifulSoup


def add_str(main, add, split=' '):
    main = str(main)
    if main != '':
        main += split
    return main + str(add)


def tag_info(tag):
    msg = ''
    msg = add_str(msg, tag.find('h1').text)
    msg = add_str(msg, tag.find('p', {'class': 'wea'}).text)
    msg = add_str(msg, tag.find('p', {'class':'tem'}).text.strip())
    msg = add_str(msg, tag.find('p', {'class': 'win'}).find_next('span')['title'] + tag.find('p', {'class': 'win'}).text.strip())
    msg = add_str(msg, tag.find('p', {'class': 'win'}).find_next('span').find_next('span').text)
    return msg


def Beijing_weather():
    soup = BeautifulSoup(urlopen('http://www.weather.com.cn/weather1d/101010100.shtml'), 'html.parser')
    tag_0 = soup.find('input', {'id': 'fc_24h_internal_update_time'})
    msg_0 = tag_0['value'] + ' (update)\n'  # 更新时间
    tag_1 = soup.find('input', {'id': 'hidden_title'})
    msg_1 = tag_1['value'] + '\n'  # 当前天气
    tag_2 = soup.find('p', {'class': 'wea'}).find_parent()
    msg_2 = tag_info(tag_2) + '\n'  # 下一段时间天气
    tag_3 = tag_2.find_next_sibling()
    msg_3 = tag_info(tag_3)  # 再下一段时间天气
    return '北京天气预报：\n' + msg_0 + msg_1 + msg_2 + msg_3
