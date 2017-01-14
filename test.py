# -*- coding: utf-8 -*-

# Импортируем нужные нам библиотеки
import urllib, urllib2, re, sys, os, base64, ssl
import parser


def format_direct_link(source_link, q):
        regex = re.compile("\[([^\]]+)\]", re.IGNORECASE)
        return regex.sub(q, source_link)

def get_qualitys(source_link):
        try:
            avail_quality = re.compile("\[([^\]]+)\]", re.S).findall(source_link)[0]
            return avail_quality.split(',')
        except:
            return '0'.split()

def decode_direct_media_url(encoded_url):
        codec_a = ("l", "u", "T", "D", "Q", "H", "0", "3", "G", "1", "f", "M", "p", "U", "a", "I", "6", "k", "d", "s", "b", "W", "5", "e", "y", "=")
        codec_b = ("w", "g", "i", "Z", "c", "R", "z", "v", "x", "n", "N", "2", "8", "J", "X", "t", "9", "V", "7", "4", "B", "m", "Y", "o", "L", "h")
        i = 0
        for a in codec_a:
            b = codec_b[i]
            i += 1
            encoded_url = encoded_url.replace(a, '___')
            encoded_url = encoded_url.replace(b, a)
            encoded_url = encoded_url.replace('___', b)

        return base64.b64decode(encoded_url)

# Функция для получения исходного кода web-страниц
def GetHTML(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3', 'Content-Type':'application/x-www-form-urlencoded'}
    context = ssl._create_unverified_context()
    conn = urllib2.urlopen(urllib2.Request(url, urllib.urlencode({}), headers), context=context)
    html = conn.read()
    conn.close()

    return html

# Тест на работоспособность
#url = 'http://filmix.net/play/114801'
url = 'http://filmix.net/dramy/104910-eddi-orel-2016.html'
#url = 'http://filmix.net/dramy/111228-radiovolna-2016.html'
html = GetHTML(url)

# Отримуємо прямі лінки на всі дубляжі
print 'Прямі лінки на всі дубляжі'.decode('utf-8')
compil2 = re.compile('data-translation-link="([^\"]+)"', re.S).findall(html)
print '========'
# Конвертуємо в читабельний вигляд (в імені перераховані всі якості)
for js in compil2:
    js_str = decode_direct_media_url(js.decode('string_escape').decode('utf-8'))
    print js_str
    if(js_str.find('.txt') != -1):
        playlist = decode_direct_media_url(GetHTML(js_str)).decode('utf-8')
        print playlist

print '========'


# Отримати список дубляжів
print 'Список дубляжів:'.decode('utf-8')
print '++++++++'
trans_all = re.compile('data-locked="no">([^\"]+)</span></li>', re.S).findall(html)
for trans in trans_all:
    print trans

print '========'


'''
# Отримуємо лінк на дубляж по змовчуванню (в імені перераховані всі якості)
print 'Лінк на дубляж по змовчуванню (в імені перераховані всі якості)'.decode('utf-8')
js_string = decode_direct_media_url(re.compile("videoLink = '([^\']+)';", re.S).findall(html)[0].decode('string_escape').decode('utf-8'))
print js_string
if(js_string.find('.txt') != -1):
        playlist = decode_direct_media_url(GetHTML(js_string)).decode('utf-8')
        print playlist

# Отримуємо список присутніх якостей відео
print 'Список присутніх якостей відео'.decode('utf-8')
avail_quality = get_qualitys(js_string)
print avail_quality
print '--------'

# Отрмуємо лінки на відео різної якості
print 'Лінки на відео різної якості'.decode('utf-8')
for q in avail_quality:
                  if(q == ''): continue
                  direct_link = format_direct_link(js_string, q) if q != 0 else js_string
                  print direct_link
'''
