# Выпускная квалификационная работа по специальности "Прикладная информатика", профилю "Искусственный интеллект и анализ данных"

Тема для выпускной квалификационной работы: **«Определение эмоциональной окраски отзывов с помощью интеллектуальной системы»**.

Основаня цель ВКР: **"Создание интеллектуальной системы по определению тональности отзывов студентов по пройденным ИТ-дисциплинам на факультете информацтинных технологий ЧОУ ВО Московского университета им. С.Ю. Витте"**.

Название создаваемой интеллектуальной системы: МУИВ – образовательная статистика по ИТ-дисциплинам – ИТОС.

Был проведен анализ структуры Университета и составлено [техническое задание](https://github.com/AliyaBadmaeva/PDP/blob/main/itos/itos/static/docs/%D0%9C%D0%A3%D0%98%D0%92%20762.02.00.00.000%20%D0%A23%20%D0%A2%D0%B5%D1%85%D0%BD%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%BE%D0%B5%20%D0%B7%D0%B0%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5.pdf).

Было несколько основных задач:

-подбор набора данных для дообучения нейронной сети;

-подбор нейронной сети для анализа тональности;

-обучение нейронной сети;

-создание проекта на Django и приложений (разная функциональность внутри проекта);

-проектирование и создание базы данных на PostgreSQL в соответствии с требованиями Django (есть ограничения и обязательные поля);

-внедрение нейронной сети;

-тестирование;

-отладка.

## Подбор набора данных для дообучения нейронной сети

> **Датасеты**

Первоначально для выполнения задачи был выбран датасет с сайта Kaggle, доступный по [ссылке](https://www.kaggle.com/datasets/sarath02003/multiclass-sentiment-analysis/data), однако научный руководитель в своем отзыве попросил создать модель для русскоязычных данных, поэтому был проведен парсинг отзывов по образовательным IТ курсам с сайта [stepik](https://stepik.org/catalog), два файла для парсинга доступны в папке [research](https://github.com/AliyaBadmaeva/PDP/tree/main/research), в ней же есть файл requirements.txt, он содержит библиотеки для парсинга. В папке research два файла - [один для парсинга ссылок на дисциплины](https://github.com/AliyaBadmaeva/PDP/blob/main/research/keyword_and_courses_link_parse.py), второй - [для парсинга отзывов по ссылкам из первого файла](https://github.com/AliyaBadmaeva/PDP/blob/main/research/parser.py). В папке [output](https://github.com/AliyaBadmaeva/PDP/tree/main/research/output) внутри директории research содержатся два файла - результаты парсинга, файл [stepik_all_reviews_2025-09-07_05-10-59.xlsx](https://github.com/AliyaBadmaeva/PDP/blob/main/research/output/stepik_all_reviews_2025-09-07_05-10-59.xlsx) содержит русскоязычный датасет. 

Первый датасет сохранен в репозитории для истории: он представляет собой отзывы на ИТ-товары, девайсы и приложения. Поскольку в нашем случае задача состоит в определении отзывов на ИТ-дисциплины, данный датасет подходил для задачи текстовой классификации. В датасете присуствует текст отзыва, оценка - целое число и название оценки - "positive" -2, "neutral" - 1, "negative" - 0. Таким образом, стояла задача мультиклассовой классификации.
Первый датасет подгружен в репозиторий файлами: [train_df.csv](https://github.com/AliyaBadmaeva/PDP/blob/main/train_df.csv), [val_df.csv](https://github.com/AliyaBadmaeva/PDP/blob/main/val_df.csv), [test_df.csv](https://github.com/AliyaBadmaeva/PDP/blob/main/test_df.csv).
Также для истории сохранена работа по первому англоязычному датасету:

> **Разведочный анализ данных по первому датасету**

Был проведен разведочный анализ данных -  файл [Badmaeva_A_A__PDP_EDA.ipynb](https://github.com/AliyaBadmaeva/PDP/blob/main/Badmaeva_A_A__PDP_EDA.ipynb).

Поскольку объем файла слишком велик, на Github он иногда не отображается либо полностью, либо не отображаются динамические графики библиотеки Plotly. Но он доступен по [ссылке](https://colab.research.google.com/drive/1akbXMwquQrnqR2IGcyfeEIuUcMFiMJuq#scrollTo=Ho-VgA2Sl__S) на Google Colab или по [ссылке](https://www.kaggle.com/code/aliyabadmaeva/exploratory-data-analysis-for-text-dataset) на Kaggle.
Для запуска блокнота достаточно облачных мощностей Google Colab или Kaggle и установки некоторых библиотек, что прописано в блокнотах в коде.
Надо отметить, что не обязательно объединять все три выборки - тренировочную, тестовую и валидационную в один датасет, но в таком случае размер файла будет еще больше, по этой причине и было проведено объединение данных для разведочного анализа.

## Подбор нейронной сети для анализа тональности и обучение нейронной сети

Поскольку для интеллектуальной системы необходимо быстрое определение тональности, то выбор был сделан в пользу Bert. 

> **Определение эмоциональной окраски англоязычных отзывов с помощью DistilBERT по первому датасету**

Анализ эмоциональной окраски англоязычных отзывов представлен в файле [Badmaeva_A_A__PDP.ipynb](https://github.com/AliyaBadmaeva/PDP/blob/main/Badmaeva_A_A__PDP.ipynb). Была проведена предобработка данных для последующего дообучения предобученной модели DistilBert base uncased на новых данных. Для обучения был выбран Trainer с пободранными параметрами. В результате модель определяет эмоциональную окраску с точностью 76%. Лучшая модель сохранена в папку results и доступна по [ссылке](https://drive.google.com/file/d/18YqaEbiJcMpnVolo_usJs24xYzGI4-dg/view?usp=sharing), т.к. объем слишком большой, то не получается его выложить на Github из-за ограничений на файлы - не более 50МВ.

Также по [ссылке](https://www.kaggle.com/code/aliyabadmaeva/sentiment-analysis-with-bert-pytorch) доступен блокнот на kaggle. Стоит отметить, что для выполнения дообучения модели требуется на локальном компьютере иметь встроенную видеокарту NVidia, желательно не меньше 3070 RTX. Но если датасет будет больше, то нужна модель выше. На Google Colab недостаточно имеющихся мощностей Тесла, поэтому для работы использовались собственные мощности локального компьютера - в качестве ускорителя видеокарта NVidia 3070 RTX. На kaggle предоставляются сразу две облачные видеокарты Тесла Т100, поэтому в блокноте был увеличен размер выборок в тренировочных аргументах, хотя это существенно не повлияло на результат - показатель точности (accuracy).


> **Определение эмоциональной окраски русскоязычных отзывов с помощью RuBERT DeepPavlov по датасету, созданному с помощью парсинга с сайта stepik**

В файле [requirements.txt](https://github.com/AliyaBadmaeva/PDP/blob/main/requirements.txt) приведены необходимые библиотеки для проведения дообучения модели RuBERT от Трансформеров.

Анализ эмоциональной окраски русскоязычных отзывов по образовательным IT-дисциплинам представлен в файле [Badmaeva_AA_RuBert_PDP.ipynb](https://github.com/AliyaBadmaeva/PDP/blob/main/Badmaeva_AA_RuBert_PDP.ipynb), иногда он не отображается, поэтому он также доступен по [ссылке](https://colab.research.google.com/drive/1tCD6YhYxXMu-tU3ltJYzRDGd5bgWsqiU?usp=sharing), либо его можно скачать в репозитории. Для запуска файла необходимо, чтобы датасет лежал в этой же папке. Была проведена предобработка данных для последующего дообучения предобученной модели RuBert DeepPavlov на новых данных. Для обучения был выбран Trainer с пободранными параметрами. В результате модель определяет эмоциональную окраску с точностью 74%. Лучшая модель сохранена в папку ruBert_results и доступна по [ссылке](https://drive.google.com/drive/folders/1Jt38VedhyD4t5KmA_Yk0TuGdVy8GZpQa?usp=sharing), т.к. объем слишком большой, то не получается ее выложить на Github.

Как и для англоязычной модели потребовалось дообучение на локальном компьютере. Использовались собственные мощности локального компьютера - в качестве ускорителя видеокарта NVidia 3070 RTX. 

## Создание проекта на Django и приложений (разная функциональность внутри проекта)

Создание проекта происходило в среде разработки PyCharm. Для создания проекта itos в выбранной папке необходимо выполнить команду: django-admin startproject itos. Далее необходимо перейти в папку проекта через консоль PyCharm (Terminal) набором команды: cd itos. Далее активируем виртуальное окружение: .\venv\Scripts\activate. В папке проекта лежит файл [requirements.txt](https://github.com/AliyaBadmaeva/PDP/blob/main/itos/itos/requirements.txt) со всеми необходимыми библиотеками для работы. Чтобы установить бибилиотеки из файла нужно выполнить команду: pip install -r requirements.txt. После установки необходимых библиотек возможен запуск сервера: 
python manage.py runserver.

ИТОС состоит из следующих частей:

-Общая папка [itos](https://github.com/AliyaBadmaeva/PDP/tree/main/itos/itos/itos) – в ней хранится все, что касается всего проекта в целом. В файле [settings.py](https://github.com/AliyaBadmaeva/PDP/blob/main/itos/itos/itos/settings.py) хранятся настройки проекта, а в файле [urls.py](https://github.com/AliyaBadmaeva/PDP/blob/main/itos/itos/itos/urls.py) все Url сайта.

-В папке [apps](https://github.com/AliyaBadmaeva/PDP/tree/main/itos/itos/apps) содержатся 3 приложения с разной функциональностью:

•	[accounts](https://github.com/AliyaBadmaeva/PDP/tree/main/itos/itos/apps/accounts) - авторизация пользователей;

•	[blog](https://github.com/AliyaBadmaeva/PDP/tree/main/itos/itos/apps/blog) – информационная часть сайта;

•	[dashboard](https://github.com/AliyaBadmaeva/PDP/tree/main/itos/itos/apps/dashboard) - дашборд в зависимости от роли пользователя
.
Для создания приложения внутри проекта нужно ввести команду: python manage.py startapp accounts.

В приложениях 2 главных файла, остальные файлы могут быть пустыми или отсутствовать, в зависимости от функционала приложения. Минимально требуется наличие файлов: urls.py – для url-ов приложения, views.py – для создания функций для связи с шаблонами html-страниц – уровень представлений. 

В приложении accounts есть дополнительный файл [models.py](https://github.com/AliyaBadmaeva/PDP/blob/main/itos/itos/apps/accounts/models.py) – содержит базу данных системы. Также в этом приложении заполнен файл [admin.py](https://github.com/AliyaBadmaeva/PDP/blob/main/itos/itos/apps/accounts/admin.py) для использования админки Django.
 
В приложении blog стоит обратить внимание на файл [context_processors.py](https://github.com/AliyaBadmaeva/PDP/blob/main/itos/itos/apps/blog/context_processors.py), отвечающий за создание кнопок для перехода со страниц блога в личный кабинет пользователя.

Файл в приложении dashboard [utils.py](https://github.com/AliyaBadmaeva/PDP/blob/main/itos/itos/apps/dashboard/utils.py) позволяет использовать нейросеть для определения тональности отзывов до отправки их в базу данных.

- В репозитории не представлена папка models – в ней находится дообученная модель rubert, которую использует ИТОС для оценки тональности отзывов. Из-за ограничений GitHub, модель выложена и доступна по [ссылке](https://drive.google.com/file/d/18YqaEbiJcMpnVolo_usJs24xYzGI4-dg/view).

- Папка [static](https://github.com/AliyaBadmaeva/PDP/tree/main/itos/itos/static) на этом же уровне дает доступ ко всем стилям CSS – в папке [css](https://github.com/AliyaBadmaeva/PDP/tree/main/itos/itos/static/css), к документам, выгружаемым из ИТОС – в папке [docs](https://github.com/AliyaBadmaeva/PDP/tree/main/itos/itos/static/docs), а также картинкам – папка [img](https://github.com/AliyaBadmaeva/PDP/tree/main/itos/itos/static/img).

- Папка [templates](https://github.com/AliyaBadmaeva/PDP/tree/main/itos/itos/templates) на этом же уровне хранит страницы в формате html для каждого приложения в одноименных с названием приложений папках. 

## Проектирование и создание базы данных на PostgreSQL

> База данных на PostgreSQL (первая версия)

Для создания интеллектуальной системы на сайте первоначально была спроектирована база данных на PostgreSQL. Код приведен далее.

```
-- Создаем БД
create database itos;
-- Создаем таблицу Контактная информация
CREATE TABLE contact_info (id_contact_info SERIAl PRIMARY KEY, surname VARCHAR(45) NOT NULL, name VARCHAR(45) NOT NULL, patronymic VARCHAR(45) NOT NULL, email VARCHAR(45) NOT NULL);
-- Создаем пользовательский тип enum для ролей
CREATE TYPE enum_role AS ENUM('администратор', 'менеджер', 'студент', 'преподаватель');
-- Создаем таблицу Ключевой информации
CREATE TABLE IF NOT EXISTS key_info (user_id SERIAl PRIMARY KEY, login INT NOT NULL, password VARCHAR(45) NOT NULL, id_contact_info INT NOT NULL, role enum_role NOT NULL);
-- Создаем пользовательский тип для профилей подготовки
CREATE TYPE enum_profile AS ENUM('ИИ и анализ данных', 'Корпоративный ИС', 'Кибербезопасность ЦП', 'Игровая компьютерная индустрия', 'Бизнес-аналитик 1С', 'Цифровой дизайн и веб-разработка');
-- Создаем таблицу Профили
CREATE TABLE IF NOT EXISTS profile (id_profile SERIAl PRIMARY KEY, name_of_profile enum_profile NOT NULL);
-- Создаем пользовательский тип для высшего образования
CREATE TYPE enum_education AS ENUM('бакалавриат', 'магистратура', 'специалитет');
-- Создаем таблицу Учебный план
CREATE TABLE IF NOT EXISTS curriculum (id_curriculum SERIAl PRIMARY KEY, year_of_learning_start SMALLINT NOT NULL, num_of_semesters_of_study SMALLINT NOT NULL, type_of_higher_education enum_education NOT NULL, id_profile INT NOT NULL);
-- Создаем пользовательский тип для преподаваемых на факультете дисциплин
CREATE TYPE enum_subjects AS ENUM('Автоматизация решения ОиРЗ в КИС', 'Базы данных', 'Алгоритмизация, программирование', 'Высокоуровневые методы прогр-ния');
-- Создаем таблицу Предметы
CREATE TABLE IF NOT EXISTS subjects (id_subject SERIAl PRIMARY KEY, name_of_subject enum_subjects NOT NULL);
-- Создаем таблицу Изученные предметы
CREATE TABLE IF NOT EXISTS learning_subjects (id_learning_subjects SERIAl PRIMARY KEY, id_subject INT NOT NULL, id_curriculum INT NOT NULL, semester_after_learning SMALLINT NOT NULL);
-- Создаем пользовательский тип для эмоциональной окраски отзывов
CREATE TYPE enum_sentiment AS ENUM('Негативный', 'Нейтральный', 'Положительный');
-- Создаем таблицу Отзывы
CREATE TABLE IF NOT EXISTS reviews (id_review SERIAl PRIMARY KEY, date_of_loading DATE NOT NULL, user_id INT NOT NULL, id_learning_subjects INT NOT NULL, review TEXT CONSTRAINT check_size CHECK (char_length(review) <= 512) NOT NULL, score_of_review FLOAT NULL, name_of_score enum_sentiment NULL);
-- Создаем таблицу Студенческие группы
CREATE TABLE IF NOT EXISTS student_group (id_student_group SERIAl PRIMARY KEY, id_curriculum INT NOT NULL);
-- Создаем таблицу Студенты
CREATE TABLE IF NOT EXISTS students (id_students SERIAl PRIMARY KEY, id_student_group INT NOT NULL);
-- Ограничители помогут по уникальным полям нам избежать случайного задвоения информации.
-- Добавим ограничители в таблицу Студенты
-- Уникальное сочетание 2 полей
ALTER TABLE students ADD CONSTRAINT id_students_and_groups_UNIQUE UNIQUE (id_students, id_student_group);
-- Внешний ключ, касакдное изменение при обновлении и ограничения при удалении
ALTER TABLE students ADD CONSTRAINT id_student FOREIGN KEY (id_students) REFERENCES key_info (user_id) ON DELETE RESTRICT ON UPDATE CASCADE;
-- Внешний ключ, касакдное изменение при обновлении и ограничения при удалении
ALTER TABLE students ADD CONSTRAINT id_student_group FOREIGN KEY (id_student_group) REFERENCES student_group (id_student_group) ON DELETE RESTRICT ON UPDATE CASCADE;
-- Уникальное сочетание 2 полей
ALTER TABLE student_group ADD CONSTRAINT id_student_groups_and_curric_UNIQUE UNIQUE (id_student_group, id_curriculum);
-- Добавим ограничитель в таблицу Студенческие группы
ALTER TABLE student_group ADD CONSTRAINT id_curriculum_idx FOR-EIGN KEY (id_curriculum) REFERENCES curriculum (id_curriculum) ON DELETE RESTRICT ON UPDATE CASCADE;
-- Добавим ограничители в таблицу Отзывы
ALTER TABLE reviews ADD CONSTRAINT id_review_UNIQUE UNIQUE (id_review);
ALTER TABLE reviews ADD CONSTRAINT review_UNIQUE UNIQUE (review);
ALTER TABLE reviews ADD CONSTRAINT review_user_subj_UNIQUE UNIQUE (user_id, id_learning_subjects, review);
ALTER TABLE reviews ADD CONSTRAINT user_id FOREIGN KEY (user_id) REFERENCES key_info (user_id) ON DELETE RESTRICT ON UPDATE CASCADE;
ALTER TABLE reviews ADD CONSTRAINT id_learning_subjects FOREIGN KEY (id_learning_subjects) REFERENCES learning_subjects (id_learning_subjects) ON DELETE RESTRICT ON UPDATE CASCADE;
-- Добавим ограничители в таблицу Предметы
ALTER TABLE subjects ADD CONSTRAINT id_sub_and_name_UNIQUE UNIQUE (name_of_subject);
-- Добавим ограничители в таблицу Изученные предметы
ALTER TABLE learning_subjects ADD CONSTRAINT curric_semes_id_learning_subjects_UNIQUE UNIQUE (id_subject, id_curriculum, se-mester_after_learning);
--Внешний ключ
ALTER TABLE learning_subjects ADD CONSTRAINT id_curriculum_idx FOREIGN KEY (id_curriculum) REFERENCES curriculum (id_curriculum);
ALTER TABLE learning_subjects ADD CONSTRAINT id_subject_idx FOREIGN KEY (id_subject) REFERENCES subjects (id_subject);
-- Добавим ограничитель в таблицу Учебный план
ALTER TABLE curriculum ADD CONSTRAINT id_profile_idx FOREIGN KEY (id_profile) REFERENCES profile (id_profile);
ALTER TABLE curriculum ADD CONSTRAINT year_num_type_id_profile_UNIQUE UNIQUE (year_of_learning_start, num_of_semesters_of_study, type_of_higher_education, id_profile);
-- Добавим ограничитель в таблицу Профиль
ALTER TABLE profile ADD CONSTRAINT profile_UNIQUE UNIQUE (name_of_profile);
-- Добавим ограничитель в таблицу Контактная информация
ALTER TABLE contact_info ADD CONSTRAINT idcontact_info_UNIQUE UNIQUE (id_contact_info);
ALTER TABLE contact_info ADD CONSTRAINT unique_info_UNIQUE UNIQUE (surname, name, patronymic, email);
-- Добавим ограничители в таблицу Ключевая информация
ALTER TABLE key_info ADD CONSTRAINT login_pass_UNIQUE UNIQUE (login, password);
ALTER TABLE key_info ADD CONSTRAINT id_contact_info_idx FOREIGN KEY (id_contact_info) REFERENCES contact_info (id_contact_info) ON DELETE RESTRICT ON UPDATE CASCADE;
```

SQL-запросы на заполнение данных здесь не приводятся в целях сохранения персональных данных.

> База данных на фреймворке Django - PostgreSQL (конечная версия)

```
-- Создаем БД
create database itos;
-- Создаем таблицу Аккаунты пользователей
CREATE TABLE accounts_user (id SERIAl PRIMARY KEY, username VAR-CHAR(45) NOT NULL UNIQUE, surname VARCHAR(45) NOT NULL, name VARCHAR(45) NOT NULL, patronymic VARCHAR(45), email VARCHAR(45) NOT NULL), password VARCHAR(128) NOT NULL, role varchar(13) NOT NULL CHECK (role IN ('администратор','менеджер','студент','преподаватель')), is_active BOOLEAN NOT NULL DEFAULT TRUE, is_staff BOOLEAN NOT NULL DE-FAULT FALSE, date_joined TIMESTAMP WITH TIME ZONE NOT NULL DE-FAULT NOW());
```

Password нельзя сделать уникальным, так как это ломает возможность аутентификации в Django-приложениях, так как в таких приложениях пароли хранятся как хэшированне, хэши могут совпасть, только соль может отличаться.

```
-- Добавим ограничитель в таблицу Аккаунты пользователей 
ALTER TABLE contact_info ADD CONSTRAINT unique_info_UNIQUE UNIQUE (surname, name, patronymic, email);
```

Если данные в таблице не будут меняться, то в Django можно объединить таблицы в одну, но поскольку база данных создается для образовательной си-стемы, то возможны изменения предметов – удаление и добавление, так как образовательная структура подразумевает возможность изменений. По этой при-чине решено было создать справочную таблицу в модели БД.

```
-- Создаем таблицу Профили
CREATE TABLE IF NOT EXISTS profile (id_profile SERIAl PRIMARY KEY, name_of_profile NOT NULL CHECK (name_of_profile IN ('ИИ и анализ данных', 'Корпоративный ИС', 'Кибербезопасность ЦП', 'Игровая компьютерная индустрия', 'Бизнес-аналитик 1С', 'Цифровой дизайн и веб-разработка')));
-- Добавим ограничитель в таблицу Профиль
ALTER TABLE profile ADD CONSTRAINT profile_UNIQUE UNIQUE (name_of_profile);
-- Создаем таблицу Учебный план
CREATE TABLE IF NOT EXISTS curriculum (id_curriculum SERIAl PRIMARY KEY, year_of_learning_start SMALLINT NOT NULL, num_of_semesters_of_study SMALLINT NOT NULL, type_of_higher_education NOT NULL CHECK (type_of_higher_education IN ('бакалавриат', 'магистратура', 'специалитет')), profile INT NOT NULL);
-- Добавим ограничитель в таблицу Учебный план
ALTER TABLE curriculum ADD CONSTRAINT id_profile_idx FOREIGN KEY (profile) REFERENCES profile (id_profile);
ALTER TABLE curriculum ADD CONSTRAINT year_num_type_id_profile_UNIQUE UNIQUE (year_of_learning_start, num_of_semesters_of_study, type_of_higher_education, profile);
-- Создаем таблицу Предметы
CREATE TABLE IF NOT EXISTS subjects (id_subject SERIAl PRIMARY KEY, name_of_subject NOT NULL CHECK (name_of_subject IN ('Автоматизация решения ОиРЗ в КИС', 'Базы данных', 'Алгоритмизация, программирование', 'Высокоуровневые методы прогр-ния')));
-- Добавим ограничители в таблицу Предметы
ALTER TABLE subjects ADD CONSTRAINT name_UNIQUE UNIQUE (name_of_subject);
-- Создаем таблицу Изученные предметы
CREATE TABLE IF NOT EXISTS learning_subjects (id_learning_subjects SE-RIAl PRIMARY KEY, subject INT NOT NULL, curriculum INT NOT NULL, se-mester_after_learning SMALLINT NOT NULL);
--Внешний ключ
ALTER TABLE learning_subjects ADD CONSTRAINT id_curriculum_idx FOREIGN KEY (curriculum) REFERENCES curriculum (id_curriculum);
ALTER TABLE learning_subjects ADD CONSTRAINT id_subject_idx FOR-EIGN KEY (subject) REFERENCES subjects (id_subject);
-- Добавим ограничители в таблицу Изученные предметы
ALTER TABLE learning_subjects ADD CONSTRAINT curric_semes_id_learning_subjects_UNIQUE UNIQUE (id_subject, id_curriculum, semester_after_learning);
-- Создаем таблицу Отзывы
CREATE TABLE IF NOT EXISTS reviews (id_review SERIAl PRIMARY KEY, date_of_loading DATE NOT NULL, user INT NOT NULL, learning_subjects INT NOT NULL, review TEXT CONSTRAINT check_size CHECK (char_length(review) <= 512) NOT NULL, score_of_review FLOAT NULL, name_of_score NOT NULL CHECK (name_of_score IN ('Негативный', 'Нейтральный', 'Положительный'));
-- Добавим ограничители в таблицу Отзывы
ALTER TABLE reviews ADD CONSTRAINT id_review_UNIQUE UNIQUE (id_review);
ALTER TABLE reviews ADD CONSTRAINT review_UNIQUE UNIQUE (review);
ALTER TABLE reviews ADD CONSTRAINT review_user_subj_UNIQUE UNIQUE (user_id, id_learning_subjects, review);
ALTER TABLE reviews ADD CONSTRAINT user_id FOREIGN KEY (user) REFERENCES accounts_user (id) ON DELETE RESTRICT ON UPDATE CAS-CADE;
ALTER TABLE reviews ADD CONSTRAINT id_learning_subjects FOREIGN KEY (learning_subjects) REFERENCES learning_subjects (id_learning_subjects) ON DELETE RESTRICT ON UPDATE CASCADE;
-- Создаем таблицу Студенческие группы
CREATE TABLE IF NOT EXISTS student_group (id_student_group SERIAl PRIMARY KEY, id_curriculum INT NOT NULL);
-- Внешний ключ, касакдное изменение при обновлении и ограничения при удалении
ALTER TABLE students ADD CONSTRAINT id_student FOREIGN KEY (id_students) REFERENCES accounts_user (id) ON DELETE RESTRICT ON UP-DATE CASCADE;
-- Создаем таблицу Студенты
CREATE TABLE IF NOT EXISTS students (id_students SERIAl PRIMARY KEY, id_student_group INT NOT NULL);
-- Добавим ограничители в таблицу Студенты
-- Уникальное сочетание 2 полей
ALTER TABLE students ADD CONSTRAINT id_students_and_groups_UNIQUE UNIQUE (id_students, id_student_group);
-- Внешний ключ, касакдное изменение при обновлении и ограничения при удалении
ALTER TABLE students ADD CONSTRAINT id_student_group FOREIGN KEY (id_student_group) REFERENCES student_group (id_student_group) ON DELETE RESTRICT ON UPDATE CASCADE;
-- Уникальное сочетание 2 полей
ALTER TABLE student_group ADD CONSTRAINT id_student_groups_and_curric_UNIQUE UNIQUE (id_student_group, id_curriculum);
-- Добавим ограничитель в таблицу Студенческие группы
ALTER TABLE student_group ADD CONSTRAINT id_curriculum_idx FOREIGN KEY (id_curriculum) REFERENCES curriculum (id_curriculum) ON DELETE RESTRICT ON UPDATE CASCADE;
```


> Веб-сайт

**Описание веб-ресурса**, в который будет внедрена интеллектуальная система распознавания эмоциональной окраски отзывов студентов по преподаваемым ИТ-дисциплинам в Университете.

Веб-ресурс будет иметь сетевую структуру, в нем будет присутсвовать максимальная связанность страниц друг с другом.

* **Первая страница «Авторизация»** – это страница авторизации, где необходимо ввести логин и пароль. 

* **Вторая страница «Главная»** – приветственная, на которой описывается информация о веб-ресурсе, на ней будет отображено предназначение веб-ресура – определение эмоциональной окраски, какие есть типы пользователей и какие у пользователей возможные действия.

* **Третья страница «Написать отзыв»** – страница написания отзыва студентом, на ней будет краткая памятка по загрузке отзыва – необходимо выбрать доступный и изученный в прошлом семестре предмет и написать отзыв не более 512 символов, дата и код отзыва будут генерироваться системой автоматически. Внизу страницы можно будет увидеть прошлые отзывы с датой и будет отображаться их количество. Мотивация для студента будет описана на странице. Для студента написание отзывов – это возможность после 10 отзывов получить мерч в деканате. Данная страница доступна для студентов.

* **Четвертая страница «Загрузить отзывы»** - страница для загрузки на сайт отзывов в Excel-формате менеджером, курирующим учебный процесс. Данная страница доступна только менеджеру. На странице будет памятка о формате загрузки данных. Мотивация для менеджера загружать отзывы – это один из ключевых показателей эффективности.

* **Пятая страница «Статистика»** - страница для скачивания отчетов. Можно скачать отчеты с отзывами и проставленной нейросетью оценкой. Данная страница будет доступна преподавателям. Мотивация для преподавателей – отслеживание эффективности обучения и его качества, может быть использовано для рейтингования преподавателей.

* **Шестая страница «Разведочный анализ данных»**.

* **Седьмая страница «Технологии для NLP»**.

* **Восьмая страница «Часто задаваемые вопросы»**.

* **Девятая страница «О программе»** - на ней будет описана информация о версии, релизах, языке программирования, на котором написан сайт.

* **Десятая страница «Контакты»**.

Веб-сайт будет разрабатываться на языке программирования Python, с использованием фреймворка Django, база данных – PostgreSQL.

**Прототип веб-сайта** представляет собой интерактивную версию макета. В нашем случае был раработан прототип для веб-сайта для ноутбука. Поскольку есть три учетных записи с разным уровнем доступа, то были разработаны интерфейсы для преподавателя, студента и менеджера. Все прототипы разработаны в графи-ческом редакторе Figma и доступны по ссылкам:

[преподаватель](https://www.figma.com/proto/daxkWxoC4EoY25nFM9FyMb/Web?node-id=1004-634&t=D32i2ZSGVqGaeDQ9-1)

[студент](https://www.figma.com/proto/daxkWxoC4EoY25nFM9FyMb/Web?node-id=1013-3874&t=D32i2ZSGVqGaeDQ9-1)

[менеджер](https://www.figma.com/proto/daxkWxoC4EoY25nFM9FyMb/Web?node-id=1013-2043&t=D32i2ZSGVqGaeDQ9-1)



