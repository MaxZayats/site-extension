# Сайт-дополнение для schools.by

**Сайт доступен по <a href='http://MaxZayats.pythonanywhere.com/'>ссылке</a>**<br>
Логин: test<br>Пароль: test

# Аутентификация
  ![Аутентификация](https://i.imgur.com/N7Zg5OQ.png)
    
  *Сайт не предусматривает регистрацию.*<br>
  Логином и паролем являются логин и пароль от сайта вашей школы на базе <a href='https://schools.by/'>schools.by</a>

# Страница с отметками
  ![Страница с отметками](https://i.imgur.com/kQaUfvj.png)
1. Все отметки можно изменять.<br>
   При изменении отметок также меняется средний балл.
2. Общий балл является средним арифметическим всех округлённых средних баллов.
    ![Страница с отметками](https://i.imgur.com/vmrW5m3.png)
3. Кнопка "Обновить" позволяет обновить отметки.<br>
   ![Обновить](https://i.imgur.com/uksQgLr.png)<br>
   Для обновления нужно ввести пароль.<br>
   ![Ввести пароль](https://i.imgur.com/Vw7ssbi.png)
4. Кнопка "Выйти" позволяет выйти из аккаунта.

# Особенности работы
1. Сайт написан на Python(Flask) без использования баз данных.
2. Сайт адаптирован под мобильные устройства.
3. Все данные(логин, отметки) хранятся в виде куки в браузере.<br>
   Пароль **не сохраняется!**
4. Отметки достаются путём парсинга сайта <a href='https://schools.by/'>schools.by</a><br>
   В период летних каникул парсинг сайта не возможен.
