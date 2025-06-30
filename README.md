# Преддипломная практика по специальности "Прикладная информатика", профилю "Искусственный интеллект и анализ данных"

В процессе прохождения преддипломной практики необходимо было выполнить ряд задач:

-	Применение теоретических знаний, полученных при обучении в Универси-тете, для решения практических задач.
-	Исследование практического опыта создания и использования различных информационных технологий в структурных подразделениях Университе-та.
-	Решение прикладной задачи анализа данных по определению эмоциональ-ной окраски с применением регулирующей деятельность нормативно-правовой документации.
-	Сбор и изучение информации в Университете от пользователей о необхо-димой реализации инетллектуальной системы.
-	Формулирование требований к создаваемой интеллектуальной системе для различных категорий пользователей информационной системой пользова-телями из Университета.
-	Создание и внедрение интеллектуальной среды в Университет.
-	Создание технического задания на разработку компонентов автоматизиро-ванной интеллектуальной системы в соответствии с нормативно-правовыми актами.
-	Закрепление практических навыков решения професссиональных задач на закрепеленном рабочем месте в качестве исполнителя.
-	Совершенствование навыка самостоятельной работы.
-	Закрепление навыков выполнения трудовых задач в соотвествие с регла-ментирующими их профессиональными стандартами.
-	Составление отчетов и презентаций по итогам выполнения профессио-нальной деятельности.

Была выбрана тема для выпускной квалификационной работы: **«Определение эмоциональной окраски отзывов с помощью интеллектуальной системы»**.

Был проведен анализ структуры Университета и составлено техническое задание.

> База данных

Для создания интеллектуальной системы потребовалось спроектировать базу данных на PostgreSQL.

```
-- Создаем БД
create database itos;
-- Создаем таблицу Контактная информация
CREATE TABLE contact_info (id_contact_info SERIAl PRIMARY KEY, sur-name VARCHAR(45) NOT NULL, name VARCHAR(45) NOT NULL, patronymic VARCHAR(45) NOT NULL, email VARCHAR(45) NOT NULL);
-- Создаем пользовательский тип enum для ролей
CREATE TYPE enum_role AS ENUM('администратор', 'менеджер', 'студент', 'преподаватель');
-- Создаем таблицу Ключевой информации
CREATE TABLE IF NOT EXISTS key_info (user_id SERIAl PRIMARY KEY, login INT NOT NULL, password VARCHAR(45) NOT NULL, id_contact_info INT NOT NULL, role enum_role NOT NULL);
-- Создаем пользовательский тип для профилей подготовки
CREATE TYPE enum_profile AS ENUM('ИИ и анализ данных', 'Корпоратив-ный ИС', 'Кибербезопасность ЦП', 'Игровая компьютерная индустрия', 'Бизнес-аналитик 1С', 'Цифровой дизайн и веб-разработка');
-- Создаем таблицу Профили
CREATE TABLE IF NOT EXISTS profile (id_profile SERIAl PRIMARY KEY, name_of_profile enum_profile NOT NULL);
-- Создаем пользовательский тип для высшего образования
CREATE TYPE enum_education AS ENUM('бакалавриат', 'магистратура', 'специалитет');
-- Создаем таблицу Учебный план
CREATE TABLE IF NOT EXISTS curriculum (id_curriculum SERIAl PRI-MARY KEY, year_of_learning_start SMALLINT NOT NULL, num_of_semesters_of_study SMALLINT NOT NULL, type_of_higher_education enum_education NOT NULL, id_profile INT NOT NULL);
-- Создаем пользовательский тип для преподаваемых на факультете дисци-плин
CREATE TYPE enum_subjects AS ENUM('Автоматизация решения ОиРЗ в КИС', 'Базы данных', 'Алгоритмизация, программирование', 'Высокоуровневые методы прогр-ния');
-- Создаем таблицу Предметы
CREATE TABLE IF NOT EXISTS subjects (id_subject SERIAl PRIMARY KEY, name_of_subject enum_subjects NOT NULL);
-- Создаем таблицу Изученные предметы
CREATE TABLE IF NOT EXISTS learning_subjects (id_learning_subjects SE-RIAl PRIMARY KEY, id_subject INT NOT NULL, id_curriculum INT NOT NULL, semester_after_learning SMALLINT NOT NULL);
-- Создаем пользовательский тип для эмоциональной окраски отзывов
CREATE TYPE enum_sentiment AS ENUM('Негативный', 'Нейтральный', 'Положительный');
-- Создаем таблицу Отзывы
CREATE TABLE IF NOT EXISTS reviews (id_review SERIAl PRIMARY KEY, date_of_loading DATE NOT NULL, user_id INT NOT NULL, id_learning_subjects, review TEXT CONSTRAINT check_size CHECK (char_length(review) <= 512) NOT NULL, score_of_review FLOAT NULL, name_of_score enum_sentiment NULL);
-- Создаем таблицу Студенческие группы
CREATE TABLE IF NOT EXISTS student_group (id_student_group SERIAl PRIMARY KEY, id_curriculum INT NOT NULL);
-- Создаем таблицу Студенты
CREATE TABLE IF NOT EXISTS students (id_students SERIAl PRIMARY KEY, id_student_group INT NOT NULL);
-- Добавим ограничители в таблицу Студенты
ALTER TABLE students ADD CONSTRAINT id_students_UNIQUE UNIQUE (id_students);
ALTER TABLE students ADD CONSTRAINT id_student FOREIGN KEY (id_students) REFERENCES key_info (user_id) ON DELETE RESTRICT ON UP-DATE CASCADE;
ALTER TABLE students ADD CONSTRAINT id_student_group FOREIGN KEY (id_student_group) REFERENCES student_group (id_student_group) ON DE-LETE RESTRICT ON UPDATE CASCADE;
-- Добавим ограничитель в таблицу Студенческие группы
ALTER TABLE student_group ADD CONSTRAINT id_curriculum_idx FOR-EIGN KEY (id_curriculum) REFERENCES curriculum (id_curriculum) ON DELETE RESTRICT ON UPDATE CASCADE;
-- Добавим ограничители в таблицу Отзывы
ALTER TABLE reviews ADD CONSTRAINT id_review_UNIQUE UNIQUE (id_review);
ALTER TABLE reviews ADD CONSTRAINT user_id FOREIGN KEY (us-er_id) REFERENCES key_info (user_id) ON DELETE RESTRICT ON UPDATE CASCADE;
ALTER TABLE reviews ADD CONSTRAINT id_learning_subjects FOREIGN KEY (id_learning_subjects) REFERENCES learning_subjects (id_learning_subjects) ON DELETE RESTRICT ON UPDATE CASCADE;
-- Добавим ограничители в таблицу Изученные предметы
ALTER TABLE learning_subjects ADD CONSTRAINT id-tiime_of_learning_subjects_UNIQUE UNIQUE (id_learning_subjects);
ALTER TABLE learning_subjects ADD CONSTRAINT id_curriculum_idx FOREIGN KEY (id_curriculum) REFERENCES curriculum (id_curriculum);
ALTER TABLE learning_subjects ADD CONSTRAINT id_subject_idx FOR-EIGN KEY (id_subject) REFERENCES subjects (id_subject);
-- Добавим ограничитель в таблицу Учебный план
ALTER TABLE curriculum ADD CONSTRAINT id_profile_idx FOREIGN KEY (id_profile) REFERENCES profile (id_profile);
-- Добавим ограничитель в таблицу Контактная информация
ALTER TABLE contact_info ADD CONSTRAINT idcontact_info_UNIQUE UNIQUE (id_contact_info);
-- Добавим ограничители в таблицу Ключевая информация
ALTER TABLE key_info ADD CONSTRAINT login_UNIQUE UNIQUE (log-in);
ALTER TABLE key_info ADD CONSTRAINT id_contact_info_idx FOREIGN KEY (id_contact_info) REFERENCES contact_info (id_contact_info) ON DELETE RESTRICT ON UPDATE CASCADE;

```

SQL-запросы на заполнение данных здесь не приводятся в целях сохранения персональных данных, однако они указаны в отчете.

> Веб-сайт

**Описание веб-ресурса**, в который будет внедрена интеллектуальная система распознавания эмоциональной окраски отзывов студентов по преподаваемым ИТ-дисциплинам в Университете.

Веб-ресурс будет иметь сетевую структуру, в нем будет присутсвовать максимальная связанность страниц друг с другом.

* Первая страница «Авторизация» – это страница авторизации, где необходи-мо ввести логин и пароль. 

* Вторая страница «Главная» – приветственная, на ко-торой описывается информация о веб-ресурсе, на ней будет отображено предна-значение веб-ресура – определение эмоциональной окраски, какие есть типы пользователей и какие у пользователей возможные действия.

* Третья страница «Написать отзыв» – страница написания отзыва студентом, на ней будет краткая памятка по загрузке отзыва – необходимо выбрать доступ-ный и изученный в прошлом семестре предмет и написать отзыв не более 512 символов, дата и код отзыва будут генерироваться системой автоматически. Внизу страницы можно будет увидеть прошлые отзывы с датой и будет отображаться их количество. Мотивация для студента будет описана на странице. Для студента написание отзывов – это возможность после 10 отзывов получить мерч в деканате. Данная страница доступна для студентов и адмиинистратора.

* Четвертая страница «Загрузить отзывы» - страница для загрузки на сайт отзывов в Excel-формате менеджером, курирующим учебный процесс. Данная страница доступна только администратору и менеджеру. На странице будет памятка о формате загрузки данных. Мотивация для менеджера загружать отзывы – это один из ключевых показателей эффективности.

* Пятая страница «Статистика» - страница для скачивания отчетов. Можно скачать отчеты с отзывами и проставленной нейросетью оценкой. Данная страница будет доступна администратору и преподавателям. Мотивация для преподавателей – отслеживание эффективности обучения и его качества, может быть использовано для рейтингования преподавателей.

* Шестая страница «Разведочный анализ данных».

* Седьмая страница «Технологии для NLP».

* Восьмая страница «Часто задаваемые вопросы».

* Девятая страница «О программе» - на ней будет описана информация о версии, релизах, языке программирования, на котором написан сайт.

* Десятая страница «Контакты».

Веб-сайт будет разрабатываться на языке программирования Python, с использованием фреймворка Django, база данных – PostgreSQL.

**Протип веб-сайта** представляет собой интерактивную версию макета. В нашем случае был раработан прототип для веб-сайта для ноутбука. Поскольку есть три учетных записи с разным уровнем доступа, то были разработаны интерфейсы для преподавателя, студента и менеджера. Все прототипы разработаны в графи-ческом редакторе Figma и доступны по ссылкам:

[преподаватель](https://www.figma.com/proto/daxkWxoC4EoY25nFM9FyMb/Web?node-id=1004-634&t=D32i2ZSGVqGaeDQ9-1)

[студент](https://www.figma.com/proto/daxkWxoC4EoY25nFM9FyMb/Web?node-id=1013-3874&t=D32i2ZSGVqGaeDQ9-1)

[менеджер](https://www.figma.com/proto/daxkWxoC4EoY25nFM9FyMb/Web?node-id=1013-2043&t=D32i2ZSGVqGaeDQ9-1)

Репозиторий будет обновляться по мере подготовки ВКР.

