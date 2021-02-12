from flask import Flask
from flask import request
import requests
from flask import render_template

""" 
Программа берет профессию и город 
и выдает среднюю зарплату и основные требуемые навыки 
в процентном соотношении. 

Запуск: python main.py
"""

app = Flask(__name__)

url = 'https://api.hh.ru/vacancies'

def f_vacancies(page, search):
    '''Средняя Зарплата на одной странице'''
    salary = []
    ''' Переменной salary присвоен словарь , пока пустой'''
    params = {'text': f'{search}', 'page': page}
    '''' Это параметры запроса в search впишется наше слово поиска и номер страницы из найденого?!?!'''
    vacancies = requests.get(url, params=params).json()
    ''''Это запрос по указанному адресу и нашими поисковыми слова, результат запроса присваиваем переменной vacancies '''
    print(type(vacancies),vacancies )
    for item in vacancies['items']:
        ''' т.к. значение vacancies это словарь -> vacancies:Вакансии<-   и Вакансии есть тоже словарь
           id:номер, name:должнсть, 'area':{'id':'104','name':'Челябинск', 'url':'https://api.hh.ru/areas/104'},
           'salary':{'from':45000, 'to':None, 'currency':'RUR', 'gross':False} и т.д.
           мы будем обращаться по ключу 
         '''
        start, stop = 0, 0
        '''' присвоили переменным значения 0 '''
        if item['salary'] and item['salary']['currency'] == 'RUR':
            ''' если в словаре есть ключ item со значением salari и есть ключ salary со значением 'currency':'RUR', 
               то мы продолжаем выполнять цикл
            '''
            if item['salary']['from'] and item['salary']['to']:
                start = int(item['salary']['from'])
                stop = int(item['salary']['to'])
                '''
                Если разделе from и в разделе to есть значения, присваиваем их переменным start & stop 
                и делаем их целыми числами
                '''
            elif item['salary']['from'] and not item['salary']['to']:
                start = int(item['salary']['from'])
                stop = start
            elif not item['salary']['from'] and item['salary']['to']:
                stop = int(item['salary']['to'])
                start = stop
                ''' 
                Если есть данные from, но нет данных в разделе to, значение stop будет равно значению start
                если нет значения from, но есть to, то start=stop (from=to).И все значения форматируем в целое число (int)
                '''
        if (start + stop) / 2 > 0:
            salary.append((start + stop) / 2)
    return salary
''''
Если сумма from&to деленное на 2 >0, то в сисок salary записываем среднее значение от очередной вакансии
'''

def average_salary(search):
    '''Средняя зарпалата'''
    data = search.split()
    search = ' AND '.join(data)
    ''''
     Введеный при старте наш текстовый запрос, мы разделил по пробелу
     и вставили and м/у словами и применили метод join!?!?!?!?  и это все присвоили переменной search
     '''
    params = {'text': f'{search}'}
    pages = requests.get(url, params=params).json()['pages']
    '''
    В переменную pages сохраняем данные запроса, хотим результат в формате json
    и почему то хотим найти словарь со значением['pages'] и хотим его ключ?!?!?!?
    '''
    vacancies = []
    '''
    Опять создали словарь и присвоили ему имя vacancies = []. 
    Получается, что данный словаря изи класса "def f_vacancies(page, search):"
    потому что они внутри классовые, не глобальные?!?!?!?
    '''
    for page in range(pages):
        vacancies.extend(f_vacancies(page, search))
        '''
        Цикл: Для каждой страницы в диапазоне pages(это общее число страниц в ответе от запроса)
        созданный словарь vacancies расширяем, добавляем по одной странце, активируя класс (f_vacancies(page, search))
         который выдает по одной странице '''
    if len(vacancies):
        return sum(vacancies) / len(vacancies)
    '''
    Если длина списка vacancies есть какое то значение, то вернуть 
    частное от суммы данных из переменной (vacancies) (я не пойму суммы вакансий или страниц??
    и длины данных из переменной (vacancies) есть какое то число, то вернуть ?!?!?!
    '''
    else:
        return 'Нет данных!'
'''
В противном случае вывести 'Нет данных!
''''


def one_page_snippet(page, search):
    '''Навыки на одной странице'''
    snippet = [] # здесь сохраняю навыки от соискателя
    params = {'text': f'{search}', 'page': page}
    vacancies = requests.get(url, params=params).json()
    for item in vacancies['items']:
        if item['snippet']['requirement']:
            snippet.append(item['snippet']['requirement'])
            ''''
            Для участников в значениях (от ключа snippet),
            если есть значения  item -> snippet -> requirement, то
            сохраняем их в сисок snippet
            '''
    return snippet



def f_snippet(search):
    req = []  # список слов
    data = search.split()
    search = ' AND '.join(data)
    params = {'text': f'{search}'}
    pages = requests.get(url, params=params).json()['pages']
    for page in range(pages):
        for char in one_page_snippet(page, search):
            req.extend(char.split())
    # грубая обработка
    sym = [',', '.', ';', ':', '<highlighttext>', '</highlighttext>', '/', ')', '(', 'e.g.']
    for i in range(len(req)):
        for s in sym:
            if s in req[i].lower():
                req[i] = req[i].replace(s, '')
    req_resault = [item.lower() for item in req if item]
    # чистая обработка
    sym = ['и', 'знание', 'с', 'на', 'работы', 'в', 'and', 'автоматизации', 'разработки', 'или', 'программирования',
           'данных', 'понимание', 'умение', 'от', '-', 'знания', 'лет', 'навыки', 'языков', 'владение', 'будет',
           'написания', 'уверенное', 'уровне', 'для', 'по', 'принципов', 'из', 'плюсом', 'желательно', 'работать',
           'высшее', '3', 'языка', 'r', 'не', 'скриптов', 'experience', 'систем', 'как', 'желание', 'года', 'базовые',
           'in', 'анализа', 'of', 'to', 'приветствуется', 'основ']
    for i in range(len(req_resault)):
        for s in sym:
            if s == req_resault[i].lower():
                req_resault[i] = req_resault[i].replace(s, '')
    req_resault = [item.lower() for item in req_resault if item]
    # частотный словарь
    my_dict = {}
    for k in req_resault:
        my_dict[k] = req_resault.count(k)
    # сортировка навыков
    resault = list(my_dict.items())
    resault.sort(key=lambda x: x[1], reverse=True)
    # оставляем наиболее частые навыки
    number = 20
    summ = sum([i[1] for i in resault[:number]])
    dict_list = []
    for item in resault[:number]:
        dict_list.append([item[0], f'{round(100 * item[1] / summ, 2)}%'])
    return dict_list


@app.route("/")
def hello():
    '''Главная страница с описанием сервиса'''
    return render_template("index.html")


@app.route("/form", methods=['GET', 'POST'])
def form():
    '''Страница с формой запроса'''
    if request.method == 'GET':
        return render_template('form.html')
    else:
        try:
            search = round(average_salary(request.form['search']), 2)
            search = str(search)+'Руб.'
            snippet = f_snippet(request.form['search'])
        except:
            search = "Не корректный запрос."
            snippet = []
        return render_template("search.html", salary=search, search=request.form['search'], snippet=snippet)



@app.route("/contacts")
def contacts():
    '''Страница с контактами'''
    contacts = ['Артём Рожков', 'E-mail: Artem_White@mail.ru', 'Тел.: +7 916 440 6 110', 'Github: https://github.com/HeyArtem']
    return render_template("contacts.html", cont=contacts)


if __name__ == '__main__':
    app.run()














