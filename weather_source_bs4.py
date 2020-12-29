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


def tag_i_info(tag):
    return tag.find_next('em').text + " (" + tag.text + "): " + tag.find_next('p').text


def tag_i_star_info(tag):
    star = ''
    for t in tag.find_all("em"):
        if 'star' in str(t):
            star += '★'
        else:
            star += '☆'
    return tag.find_next("p").find_previous('em').text + " (" + star + "): " + tag.find_next("p").text


def tag_7d_info(tag):
    msg = ''
    msg += tag.text.strip() + ' '  # 日期='4日（今天）'
    msg += tag.find_next('p').text.strip() + ' '  # 天气='晴'
    msg += tag.find_next('p').find_next('p').text.strip() + ' '  # 温度='32/19℃'
    tag = tag.find_next('p').find_next('p').find_next('p')  # 风力
    wind_1 = tag.find_next('span')['title']
    try:
        wind_2 = tag.find_next('span').find_next('span')['title']
    except KeyError:
        wind_2 = wind_1
    if wind_1 == wind_2:
        msg += wind_1 + ' ' + tag.text.strip()  # 东风 <3级
    else:
        msg += wind_1 + '转' + wind_2 + tag.text.strip()  # 东风转西北风 <3级
    return msg


def Beijing_weather():  # 短期天气预报
    soup = BeautifulSoup(urlopen('http://www.weather.com.cn/weather1d/101010100.shtml'), 'html.parser')
    tag_0 = soup.find('input', {'id': 'fc_24h_internal_update_time'})
    msg_0 = tag_0['value'] + ' (update)\n'  # 更新时间
    tag_1 = soup.find('input', {'id': 'hidden_title'})
    msg_1 = tag_1['value'] + '\n'  # 当前天气
    tag_2 = soup.find('p', {'class': 'wea'}).find_parent()
    msg_2 = tag_info(tag_2) + '\n'  # 下一段时间天气
    tag_3 = tag_2.find_next_sibling()
    msg_3 = tag_info(tag_3)  # 再下一段时间天气
    return '【北京天气预报】\n' + msg_0 + msg_1 + msg_2 + msg_3


def Beijing_weather_Morning():  # 晨间天气预报，增加各类指数
    soup = BeautifulSoup(urlopen('http://www.weather.com.cn/weather1d/101010100.shtml'), 'html.parser')
    tag_i0 = soup.find('div', {'class':'livezs'})
    msg_i0 = '==' + tag_i0.find_next('h1').text + '==\n'
    tag_i1 = tag_i0.find('span')  # 紫外线指数
    msg_i1 = tag_i_info(tag_i1) + '\n'
    tag_i2 = tag_i1.find_next('span')  # 减肥指数
    msg_i2 = tag_i_star_info(tag_i2) + '\n'
    tag_i3 = tag_i2.find_next('span')  # 健臻血糖指数
    msg_i3 = ''
    tag_i4 = tag_i3.find_next('span')  # 穿衣指数
    msg_i4 = tag_i_info(tag_i4) + '\n'
    tag_i5 = tag_i4.find_next('span')  # 洗车指数
    msg_i5 = ''
    """
    tag_i6 = tag_i5.find_next('span')  # 空气污染扩散指数
    msg_i6 = tag_i_info(tag_i6)
    """

    return Beijing_weather().replace('天气预报', '晨间天气预报') + '\n\n' \
           + msg_i0 + msg_i1 + msg_i2 + msg_i3 + msg_i4 + msg_i5


def Beijing_weather_Night():  # 晚间七天天气预报
    soup = BeautifulSoup(urlopen('http://www.weather.com.cn/weather/101010100.shtml'), 'html.parser')
    tag_0 = soup.find('input', {'id': 'fc_24h_internal_update_time'})
    msg_0 = tag_0.find_next()['value'] + ' (update)\n'  # 更新时间
    msg_0 = ''
    msg_7d = ''
    tag_7d = tag_0.find('h1')
    for i in range(7):
        msg_7d += tag_7d_info(tag_7d) + '\n'
        tag_7d = tag_7d.find_next('h1')
    msg_7d = msg_7d[:-1]
    return '【北京七天天气预报】\n' + msg_0 + msg_7d