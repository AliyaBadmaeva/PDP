from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from django.shortcuts import redirect

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


class ManagerDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'dashboard/manager_dashboard.html'

    def test_func(self):
        return self.request.user.role == 'менеджер'


class StudentDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'dashboard/student_dashboard.html'

    def test_func(self):
        return self.request.user.role == 'студент'


class TeacherDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'dashboard/teacher_dashboard.html'

    def test_func(self):
        return self.request.user.role == 'преподаватель'

