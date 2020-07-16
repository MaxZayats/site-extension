import requests
import datetime
from bs4 import BeautifulSoup as BS


session = requests.Session()


def authorization(login, password):
	"""Создание авторизованного профиля"""
	body = session.get('https://schools.by/login')
	body_bs = BS(body.content, 'html.parser')
	csrf = body_bs.select('input[name=csrfmiddlewaretoken]')[0]['value']

	headers = {
		'authority': 'schools.by',
		'cache-control': 'max-age=0',
		'upgrade-insecure-requests': '1',
		'content-type': 'application/x-www-form-urlencoded',
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 YaBrowser/19.12.4.25 Yowser/2.5 Safari/537.36',
		'sec-fetch-user': '?1',
		'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
		'sec-fetch-site': 'same-site',
		'sec-fetch-mode': 'navigate',
		'referer': 'https://schools.by/',
		'accept-encoding': 'gzip, deflate, br',
		'accept-language': 'en,ru;q=0.9',
		'cookie': '_ym_uid=1567707469440774662; _ym_d=1567707469; _ga=GA1.2.1769797223.1567707468; slc_cookie=^%^7BslcMakeBetter^%^7D; __utmz=26264290.1579190254.316.64.utmcsr=schools.by^|utmccn=(referral)^|utmcmd=referral^|utmcct=/; _ym_isad=2; __utma=26264290.1769797223.1567707468.1579262439.1579273403.319; __utmc=26264290; _ym_visorc_39239090=w; csrftoken='+csrf+'; __utmt=1; __utmb=26264290.6.9.1579274859398',
	}

	data = {
		'csrfmiddlewaretoken': csrf,
		'username': login,
		'password': password
	}

	profile = session.post(
		'https://schools.by/login', headers=headers, data=data
	)
	return profile


def get_quarter(school_domain, pupil_id, week):
	"""Функция отдаёт точный номер четверти в рамках сайта"""
	quarter = 33   # 33 - номер 1 четверти в 2019

	# Получаем дату начала первой четверти в этом учебном году
	if datetime.date.today().month >= 9:
		# 1 или 2 четверти
		delta = datetime.date.today().year - 2019
		quarter += 4*delta  # Номер первой четверти в текущем учебном году
	else:
		# 3 или 4 четверти
		delta = (datetime.date.today().year-1) - 2019
		quarter += 4*delta + 2  # Номер третьей четверти в текущем учебном году

	quarter = get_exact_quarter(school_domain, pupil_id, quarter, week)
	return quarter


def get_exact_quarter(school_domain, pupil_id, quarter, week):
	"""Функция определяет точный номер четверти из неточного"""
	url = f'{school_domain}.schools.by/pupil/{pupil_id}/dnevnik/quarter/{quarter}/week/{week}'
	body = session.get(url)
	body_bs = BS(body.content, 'html.parser')
	if body_bs.text == 'Выход за границы четверти':
		return quarter + 1
	else:
		return quarter


def get_url_pattern(login, password, week):
	"""Функция отдаёт шаблон ссылки для получения отметок"""
	profile = authorization(login, password)
	body = BS(profile.content, 'html.parser').body

	# Получаем все необходимые параметры для создания ссылки
	school_domain = body.find(class_='u_photo').find('a').get('href').split('.')[0]
	pupil_id = body.find('a', class_='button_green').get('href').split('/')[2]
	quarter = get_quarter(school_domain, pupil_id, week)

	return f'{school_domain}.schools.by/pupil/{pupil_id}/dnevnik/quarter/{quarter}/week/'


def fill_diary(login, password):
	"""Функция отдаёт все отметки"""
	# Получение даты понедельника текущей недели
	today = datetime.date.today()
	week = today + datetime.timedelta(days=-today.weekday()-7, weeks=1)

	try:
		url_pattern = get_url_pattern(login, password, week)
	except:
		return 'Bad Login'

	diary = {}  # Словарь для отметок

	while True:
		url = url_pattern + str(week)  # Основная ссылка
		body = session.get(url)
		body_bs = BS(body.content, 'html.parser')
		if body_bs.text == 'Выход за границы четверти':  # Конец четверти
			break
		else:
			marks = body_bs.findAll('strong')  # Получаем все отметки на неделе
			for mark in reversed(marks):
				lesson = mark.parent.parent.parent.td.span.text\
					.replace('\n', '').replace(' ', '')
				lesson = lesson.replace(lesson[0:2], '')  # Получение названия предмета

				mark = mark.text  # Получение отметки
				if mark != '':  # Ошибочная отметка
					try:
						diary[lesson].insert(0, mark)  # Добавляем в существующий предмет отметку
					except:
						diary[lesson] = [str(mark)]  # Если предмета не существует - создаём

			week = week - datetime.timedelta(days=7)  # Перемещаемся на неделю назад

	return dict(sorted(diary.items()))
