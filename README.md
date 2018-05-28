# People_yandex_parser
Generate emails from name and surname from People.yandex.ru,what include linkedin,vk,facebook etc

Arguments:

'-w', '--work', required=True, help='Place of work' (If place of work contains a space character, needs to be in quotes)
'-l', '--last', required=False. Last page to parse from people.yandex.ru. Default is 10
'-f', '--first', required=False. First page to parse from people.yandex.ru. Default is 0
'-e', '--email', required=False. End of Emails without @ symbol
'-s', '--save_to_file', required=False. Save to file. Without -dont save. With empty line - save to place_of_work.txt . With any string - save to any_string.txt
'-t', '--type', required=False.Type of generation:
With example of user Thomas Anderson:

1=N.Surname:T.Anderson
2=Surname.N:Anderson.T
3=Surname:Anderson
4=Surname.N.P:Anderson.T.A(Anderson.T.B etc to Anderson.T.Z)
5=SurnameN:AndersonT
6=NSurname:TAnderson
7=NameS:ThomasA
8=SName:AThomas

Usage:

With example of user Thomas Anderson

Search with place of work "yandex" from 0 to 50 page with type of generation 1=N.Surname with save to yandex.txt end with end of email @yandex.com

python harv.py -w "yandex" -l 50 -s -t 1 -e yandex.com
