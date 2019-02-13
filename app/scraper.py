import requests
from bs4 import BeautifulSoup
import datetime



class Job:
    def __init__(self, title, pub_date, price, link):
        self.title = title
        self.pub_date = pub_date
        self.price = price
        self.link = link
    def __str__(self):
        return self.title

def get_html(url):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1'}
    r = requests.get(url, headers=headers)
    return r.text

def is_today_freelansim(d):
    if '~' in d:
        return True
    return False

def is_today(pub_date):
    now = datetime.datetime.now()
    m = ['Января', 'Ферваля', 'Марта', 'Апреля', 'Мая', 'Июня', 'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря']
    months = {i:month for i, month in enumerate(m, 1)}
    now = f'{now.day} {months[now.month]}'
    if pub_date.lower().split() == now.lower().split():
        return True
    return False

def get_freelansim(html):
    freelansim = []
    soup = BeautifulSoup(html, 'lxml')
    lis = soup.find_all('li', class_='content-list__item')
    for li in lis:
        title = li.find('div', class_='task__title').text.replace('\n', ' ').strip()
        d = li.find('div', class_='task__params params').find('span', class_='params__published-at icon_task_publish_at').text
        # check if job added today
        if not is_today_freelansim(d):
            continue
        pub_date = d.replace('~', '').replace('\n', ' ').strip()
        price = li.find('div', class_='task__price').text.replace('\n', ' ').strip()
        link = 'https://freelansim.ru' + li.find('div', class_='task__title').find('a').get('href')

        data = Job(title, pub_date, price, link)
        freelansim.append(data)
    return freelansim

def connect_freelansim():
    freelansim = []
    queries = ['python', 'django', 'парсер', 'бот']
    for query in queries:
        q = f'https://freelansim.ru/tasks?q={query}'
        freelansim += get_freelansim(get_html(q))
    return freelansim

def get_hh(html):
    hh = []
    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find_all('div', class_='vacancy-serp-item')

    for div in divs:
        pub_date = div.find('span', class_='vacancy-serp-item__publication-date').text.strip().replace(u'\xa0', u' ')
        if not is_today(str(pub_date)):
            continue
        title = div.find('a', class_='bloko-link').text.strip()
        price = div.find('div', {'class' :'vacancy-serp-item__compensation', 'data-qa': 'vacancy-serp__vacancy-compensation'})
        if not price:
            price = 'Договорная'
        else:
            price = price.text.strip()
        link = div.find('a', class_='bloko-link').get('href')

        data = Job(title, pub_date, price, link)
        hh.append(data)
    return hh

def normalize_skills_moikrug(skills):
    normalized = []
    for skill in skills:
        normalized.append(skill.text.replace('(', '').replace(')', '').strip().split())
    return normalized

def get_moikrug(html):
    moikrug = []
    soup = BeautifulSoup(html, 'lxml')
    jobs = soup.find_all('div', class_='job')

    for job in jobs:

        d = job.find('span', class_='date').text.split()[:-1]
        pub_date = ' '.join(d)
        if not is_today(pub_date):
            continue

        rank = 'Junior'
        s = job.find('div', class_='specialization').find_all('a', class_='skill')
        try:
            skill = normalize_skills_moikrug(s)[1][1]
        except IndexError:
            continue

        if skill == rank:
            title = job.find('div', class_='title').get('title').strip()

            try:
                price = job.find('div', {'class': 'count', 'title': 'Зарплата'}).text
            except:
                price = 'По договоренности'
            link = 'https://moikrug.ru' + job.find('div', class_='title').find('a').get('href')

        data = Job(title, pub_date, price, link)
        moikrug.append(data)
    return moikrug




def get_all():
    freelansim = connect_freelansim()
    hh_url = 'https://hh.ru/search/vacancy?clusters=true&enable_snippets=true&schedule=remote&text=junior+python&label=not_from_agency&from=cluster_label'
    hh = get_hh(get_html(hh_url))
    moikrug_url = 'https://moikrug.ru/vacancies?q=python+junior&currency=rur&remote=1'
    moikrug = get_moikrug(get_html(moikrug_url))
    sites = [freelansim, hh, moikrug]
    all_jobs = []
    for site in sites:
        all_jobs.extend(site)
    return all_jobs


def main():
    pass


if __name__ == '__main__':
    main()
