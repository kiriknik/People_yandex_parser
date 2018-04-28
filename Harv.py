#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
from bs4 import BeautifulSoup
import urllib3
import urllib
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser(add_help=True, description='People Yandex Parser')
parser.add_argument('-w', '--work', required=True, help='Place of work')
parser.add_argument('-l', '--last', required=False, type=int, help='Last page to parse, default is 10')
parser.add_argument('-f', '--first', required=False, type=int, help='First page to parse, default is 0')
parser.add_argument('-e', '--email', required=False, help='End of Emails')
parser.add_argument('-t', '--type', required=False, type=int,
                    help='Type of generation(1=N.Surname,2=Surname.N,3=Surname,4=Surname.N.P)')
args = parser.parse_args()
if args.type is None: args.type = 1
if args.email is None: args.email = ""
if args.last is None: args.last = 10
if args.first is None: args.first = 0
emails = set()
page = args.first
last = args.last
work=urllib.quote_plus(args.work)
type = args.type
url = "https://yandex.ru/people?ps_job=" + work + "&ps_network=1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17&p="
http = urllib3.PoolManager()


def GetURL(url, page):
    http = urllib3.PoolManager()
    url = url + str(page)
    #print url
    print  ("-------" + "scanning " + str(page) + " page--------")
    r = http.request('GET', url)
    print ("----------" + "status:" + str(r.status) + "--------")
    #print r.data
    return r.data


def transliterate(string):
    capital_letters = {u'А': u'A',
                       u'Б': u'B',
                       u'В': u'V',
                       u'Г': u'G',
                       u'Д': u'D',
                       u'Е': u'E',
                       u'Ё': u'E',
                       u'Ж': u'Zh',
                       u'З': u'Z',
                       u'И': u'I',
                       u'Й': u'Y',
                       u'К': u'K',
                       u'Л': u'L',
                       u'М': u'M',
                       u'Н': u'N',
                       u'О': u'O',
                       u'П': u'P',
                       u'Р': u'R',
                       u'С': u'S',
                       u'Т': u'T',
                       u'У': u'U',
                       u'Ф': u'F',
                       u'Х': u'H',
                       u'Ц': u'Ts',
                       u'Ч': u'Ch',
                       u'Ш': u'Sh',
                       u'Щ': u'Sch',
                       u'Ъ': u'',
                       u'Ы': u'Y',
                       u'Ь': u'',
                       u'Э': u'E',
                       u'Ю': u'Yu',
                       u'Я': u'Ya', }

    lower_case_letters = {u'а': u'a',
                          u'б': u'b',
                          u'в': u'v',
                          u'г': u'g',
                          u'д': u'd',
                          u'е': u'e',
                          u'ё': u'e',
                          u'ж': u'zh',
                          u'з': u'z',
                          u'и': u'i',
                          u'й': u'y',
                          u'к': u'k',
                          u'л': u'l',
                          u'м': u'm',
                          u'н': u'n',
                          u'о': u'o',
                          u'п': u'p',
                          u'р': u'r',
                          u'с': u's',
                          u'т': u't',
                          u'у': u'u',
                          u'ф': u'f',
                          u'х': u'h',
                          u'ц': u'ts',
                          u'ч': u'ch',
                          u'ш': u'sh',
                          u'щ': u'sch',
                          u'ъ': u'',
                          u'ы': u'y',
                          u'ь': u'',
                          u'э': u'e',
                          u'ю': u'yu',
                          u'я': u'ya', }

    translit_string = ""

    for index, char in enumerate(string):
        if char in lower_case_letters.keys():
            char = lower_case_letters[char]
        elif char in capital_letters.keys():
            char = capital_letters[char]
            if len(string) > index + 1:
                if string[index + 1] not in lower_case_letters.keys():
                    char = char.upper()
            else:
                char = char.upper()
        translit_string += char

    return translit_string


def surname(string):
    return (filter(lambda x: x.isalpha(), string[string.rfind(" ") + 1:]))


def name(string):
    return (string[:string.find(" ")])


def dog(end_of_email):
    if end_of_email == "":
        return ("")
    else:
        return ("@" + end_of_email)


def email(string, type):
    if type == 1:
        # return (string[0]+"."+string[string.rfind(" ")+1:]+dog+args.email)
        return (name(string)[0] + "." + surname(string) + dog(args.email))
    if type == 2:
        return (surname(string) + "." + name(string)[0] + dog(args.email))
    if type == 3:
        return (surname(string) + dog(args.email))
    if type == 4:
        return (surname(string) + "." + name(string)[0])


def main():
    list_elements = set()
    for i in range(page, last + 1):
        file = GetURL(url, i)
        soup = BeautifulSoup(file, 'html.parser')  # загружаем html в суп
        divs = soup.findAll(name='li', attrs={'class': 'serp-item'})
        if not divs: break  # ищем дивы
        for element in divs:
            name=element.find(name='div', attrs={'class': 'organic__url-text'})
            name = name.get_text()
            name=name.decode('utf-8')
            name=name[:name.rfind("–")]
            name=transliterate(name).strip()
            list_elements.add(name)
    print ""
    print "I find " + str(len(list_elements)) +" people"
    print "Thank You for choosing our company"
    print ""
    for element in list_elements:
        if type != 4:
            emails.add(email(element, type))
        else:
            for i in range(65, 91):
                emails.add(email(element, 4) + "." + chr(i) + dog(args.email))
    for element in emails:
        print element
        #pass

if __name__ == "__main__":
    main()
