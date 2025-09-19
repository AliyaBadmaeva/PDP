from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from openpyxl import Workbook
from datetime import datetime
import pandas as pd
from django.contrib import messages
from django.shortcuts import render, redirect
from accounts.models import Review, LearningSubject, Student, User
from .utils import get_sentiment


MAX_ROWS = 900_000  # чуть меньше лимита Excel


def export_reviews_to_excel(request):  # функция для формирования файла для скачивания отчета Excel
    if request.user.role != 'преподаватель':  # недоступно пользователям с другой ролью
        return HttpResponse('Доступ запрещён', status=403)

    # Берём последние 900 000 отзывов
    print('Отзывы загружаются из dashboard/views.py')
    qs = (Review.objects
          .select_related('learning_subject__subject')
          .order_by('-id_review')  # самые свежие — в начале, сортировка
          .values(  # выбираем нужные поля
              'id_review',
              'review',
              'learning_subject__semester_after_learning',
              'date_of_loading',
              'learning_subject__subject__name_of_subject',
              'score_of_review',
              'name_of_score'
          ))[:MAX_ROWS]  # ограничиваем количество строк

    # Создаём книгу
    wb = Workbook(write_only=True)  # экономит память при большом объёме
    ws = wb.create_sheet(title='Отзывы')  # создаём лист

    # Заголовки
    ws.append([
        'ID отзыва',
        'Название дисциплины',
        'Текст отзыва',
        'Семестр после изучения',
        'Дата загрузки',
        'Дисциплина',
        'Оценка (числ)',
        'Оценка (назв)'
    ])

    # Строки данных (идут уже в нужном порядке)
    for row in reversed(qs):  # reversed - хронологический порядок «сначала старые»
        ws.append([
            row['id_review'],
            row['learning_subject__subject__name_of_subject'],
            row['review'],
            row['learning_subject__semester_after_learning'],
            row['date_of_loading'].strftime('%d.%m.%Y') if row['date_of_loading'] else '',
            row['score_of_review'] if row['score_of_review'] is not None else '',
            row['name_of_score'] or ''
        ])

    # Отдаём файл
    filename = f"reviews_last_{len(qs)}_{datetime.now():%Y-%m-%d_%H-%M}.xlsx"
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    wb.save(response)  # сохраняем
    return response

# Личный кабинет студентов
class StudentDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'dashboard/student_dashboard.html'  # шаблон

    def test_func(self):  # доступ только студентам
        return self.request.user.role == 'студент'

    def get_context_data(self, **kwargs):  # контекст
        print('Файл dashboard/views.py')
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # студент, учебный план и семестр
        student = get_object_or_404(Student, id_student=user)
        curriculum = student.student_group.curriculum
        current_sem = curriculum.num_of_semesters_of_study

        qs = Review.objects.filter(user=user)  # Все отзывы
        context['reviews'] = qs.order_by('-date_of_loading')[:2] # Последние 2 отзыва (самые свежие)
        context['total_reviews'] = qs.count()

        # дисциплины, которые уже изучены
        learned = LearningSubject.objects.filter(
            curriculum=curriculum,
            semester_after_learning__lte=current_sem
        )
        # исключаем те, на которые уже есть отзыв
        reviewed_ids = qs.values_list('learning_subject_id', flat=True)
        context['available_subjects'] = learned.exclude(
            id_learning_subjects__in=reviewed_ids
        )

        return context
    # обработка POST (сохранение отзыва)
    def post(self, request, *args, **kwargs):
        user = request.user
        ls_id = request.POST.get('learning_subject', '').strip()  # изученный предмет, обрезаем лишние пробелы
        text = request.POST.get('review', '').strip()  # отзыв, обрезаем лишние пробелы в начале и конце
        print("из файла dashboard/views.py")

        # пустые поля
        if not (ls_id and text):
            messages.error(request, 'Заполните все поля.')
            return self.get(request, *args, **kwargs)  # выводим форму

        # Некорректный id
        try:
            ls_id = int(ls_id)
        except ValueError:
            messages.error(request, 'Выберите дисциплину из списка.')
            return self.get(request, *args, **kwargs)

        # защита от дубля (на всякий случай)
        if Review.objects.filter(user=user,
                                 learning_subject_id=ls_id).exists():
            messages.error(request, 'Вы уже оставляли отзыв по этой дисциплине.')
            return self.get(request, *args, **kwargs)

        if len(text) < 3:  # минимальная длина
            messages.error(request, 'Отзыв должен быть не менее 3 символов.')
            return self.get(request, *args, **kwargs)

        if len(text) > 512:  # максимальная длина
            messages.error(request, 'Отзыв не должен превышать 512 символов.')
            return self.get(request, *args, **kwargs)

        # Распознаём тональность с помощью нашего алгоритма
        score, label = get_sentiment(text)

        print(f"[DEBUG] label='{label}', len={len(label)}")
        Review.objects.create(
            user=user,
            learning_subject_id=ls_id,
            review=text,
            score_of_review=score,
            name_of_score=label
        )
        # Выводим уведомление
        messages.success(request, f'Отзыв сохранён! Оценка отзыва: {label}')
        context = self.get_context_data()
        context['sentiment_label'] = label
        context['sentiment_score'] = score
        return self.render_to_response(context)


class DashboardRedirectView(LoginRequiredMixin, TemplateView):
    """Перенаправляет админа в admin, остальных — на нужный дашборд."""
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_superuser or user.role == 'администратор':
            return redirect('admin:index')   # стандартная админка
        elif user.role == 'менеджер':
            return redirect('dashboard:manager')
        elif user.role == 'студент':
            return redirect('dashboard:student')
        elif user.role == 'преподаватель':
            return redirect('dashboard:teacher')
        return redirect('accounts:login')        # fallback


MAX_UPLOAD_ROWS = 5000  # максимальное количество строк для загрузки

# Личный кабинет менеджеров
class ManagerDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'dashboard/manager_dashboard.html'   # шаблон

    def test_func(self):  # проверка роли
        return self.request.user.role == 'менеджер'

    def post(self, request, *args, **kwargs):
        """POST-загрузка Excel из того же шаблона."""
        print('Файл dashboard/views.py для загрузки отзывов')
        excel = request.FILES.get('excel')
        if not excel:
            messages.error(request, 'Файл не выбран')
            return self.get(request, *args, **kwargs)

        try:  # пробуем прочитать
            df = pd.read_excel(excel, usecols='A:D', nrows=MAX_UPLOAD_ROWS + 1)
        except Exception as e:  # в случае ошибки
            messages.error(request, f'Не удалось прочитать файл: {e}')
            return self.get(request, *args, **kwargs)

        df.columns = ['username', 'name_of_subject', 'review', 'semester']
        df = df.dropna(how='all')  # удаляем пустые строки
        total, created, skipped = 0, 0, []  # счетчики

        for idx, row in df.iterrows():  # перебираем строки
            total += 1  # увеличиваем счетчик
            reason = self._create_review_from_row(row, request.user)  # создаем отзыв
            if reason:  # если не удалось
                skipped.append(f'строка {idx + 2}: {reason}')  # добавляем причину
            else:  # если удалось
                created += 1  # увеличиваем счетчик
        # Выводим уведомление
        messages.success(request, f'Загружено отзывов: {created} из {total}')
        if skipped:  # если есть пропущенные выводим уведомление
            messages.warning(request, 'Пропущены:\n' + '\n'.join(skipped[:50]))

        return redirect('dashboard:manager')  # перенаправляем на страницу ЛК менеджера

    def _create_review_from_row(self, row, manager):
        """Возвращает пустую строку если успешно, иначе – причину ошибки.
        Тональность определяется автоматически, пользователю не показывается"""
        username = str(row['username']).strip()  # преобразуем в строку и убираем пробелы
        subject_nm = str(row['name_of_subject']).strip()  # преобразуем в строку и убираем пробелы
        review_txt = str(row['review']).strip()  # преобразуем в строку и убираем пробелы
        sem = int(row['semester'])  # преобразуем в число
        # Отладочное сообщение в консоль сервера
        print("из файла dasboard/views.py создаем отзывы из файла менеджера")
        # Проверки на пустоту, nan
        if not review_txt or review_txt.lower() == 'nan' or pd.isna(row['review']):
            return 'Пустой отзыв'
        if len(review_txt) < 3 or review_txt.isspace():  # если меньше 3 символов
            return 'Отзыв слишком короткий (минимум 3 символа)'
        if len(review_txt) > 512:  # если больше 512
            return 'Отзыв > 512 символов'

        try:  # Пытаемся найти студента
            student_user = User.objects.get(username=username, role='студент')
            student = Student.objects.get(id_student=student_user)
        except (User.DoesNotExist, Student.DoesNotExist):  # если не нашли
            # возвращаем причину
            return 'Студент не найден или у студента нет группы'


        curriculum = student.student_group.curriculum  # учебный план
        if sem > curriculum.num_of_semesters_of_study:
            return 'Семестр ещё не завершён'  # если семестр не завершён

        try:  # Пытаемся найти дисциплину
            learn_subj = LearningSubject.objects.get(
                subject__name_of_subject=subject_nm,
                curriculum=curriculum,
                semester_after_learning=sem
            )
        except LearningSubject.DoesNotExist:  # если не нашли
            return 'Дисциплина не входит в учебный план студента'
        # Если отзыв уже существует
        if Review.objects.filter(user=student_user, learning_subject=learn_subj).exists():
            return 'Отзыв уже существует'

        # Нейросеть видит текст отзыва и определяет оценку и название оценки
        score, label = get_sentiment(review_txt)
        # Создаем отзыв
        Review.objects.create(
            user=student_user,
            learning_subject=learn_subj,
            review=review_txt,
            uploaded_by=manager,  # менеджер загрузил
            score_of_review = score,
            name_of_score = label
        )
        return ''


# Личный кабинет преподавателя
class TeacherDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'dashboard/teacher_dashboard.html'  # шаблон

    def test_func(self):  # проверяем, является ли пользователь преподавателем
        return self.request.user.role == 'преподаватель'
