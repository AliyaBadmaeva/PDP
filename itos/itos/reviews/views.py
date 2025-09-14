from datetime import datetime
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, HttpResponse
from django.utils.timezone import make_aware
from .utils import get_sentiment
from accounts.models import Review, LearningSubject, User
import pandas as pd

# Загрузка файла менеджером
def manager_required(u):
    return u.is_authenticated and u.role == User.MANAGER

@login_required
@user_passes_test(manager_required)
def upload_reviews(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST"}, status=405)

    file = request.FILES.get("file")
    if not file:
        return JsonResponse({"error": "No file"}, status=400)

    try:
        df = pd.read_excel(file)          # колонки: subject_id, text
        texts = df["text"].astype(str).tolist()
        scores_labels = [get_sentiment(t) for t in texts]   # (score, label)
        bulk = [
            Review(
                learning_subject_id=row["subject_id"],
                user=request.user,
                review=row["text"],
                score_of_review=sc,
                name_of_score=lb
            )
            for (_, row), (sc, lb) in zip(df.iterrows(), scores_labels)
        ]
        Review.objects.bulk_create(bulk)
        return JsonResponse({"created": len(bulk)})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


#  Студент добавляет отзыв
def student_required(u):
    return u.is_authenticated and u.role == User.STUDENT

@login_required
@user_passes_test(student_required)
def student_review(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST"}, status=405)

    text = request.POST.get("text", "").strip()
    subject_id = request.POST.get("subject_id")
    if not text or not subject_id:
        return JsonResponse({"error": "text & subject_id required"}, status=400)

    score, label = get_sentiment(text)
    rev = Review.objects.create(
        learning_subject_id=subject_id,
        user=request.user,
        review=text,
        score_of_review=score,
        name_of_score=label
    )
    return JsonResponse({"id": rev.id_review, "label": label, "score": score})


# Преподаватель качает Excel
def teacher_required(u):
    return u.is_authenticated and u.role == User.TEACHER

@login_required
@user_passes_test(teacher_required)
def export_reviews(request):
    date_from = request.GET.get("from")
    date_to = request.GET.get("to")
    qs = Review.objects.select_related("learning_subject", "user")
    if date_from:
        qs = qs.filter(date_of_loading__gte=make_aware(datetime.fromisoformat(date_from)))
    if date_to:
        qs = qs.filter(date_of_loading__lte=make_aware(datetime.fromisoformat(date_to)))

    df = pd.DataFrame.from_records(
        qs.values(
            "id_review", "date_of_loading", "user__username",
            "learning_subject__subject__name_of_subject",
            "review", "score_of_review", "name_of_score"
        )
    )
    resp = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    resp["Content-Disposition"] = 'attachment; filename="reviews.xlsx"'
    df.to_excel(resp, index=False)
    return resp
