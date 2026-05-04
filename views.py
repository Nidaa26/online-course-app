from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, Enrollment, Submission, Choice, Question
from django.http import HttpResponseRedirect
from django.urls import reverse


def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    enrollment = Enrollment.objects.get(user=user, course=course)
    submission = Submission.objects.create(enrollment=enrollment)
    selected_ids = request.POST.getlist('choice')
    selected_choices = Choice.objects.filter(id__in=selected_ids)
    submission.choices.set(selected_choices)
    submission.save()
    return HttpResponseRedirect(
        reverse('onlinecourse:show_exam_result',
                args=(course_id, submission.id))
    )


def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    selected_ids = submission.choices.values_list('id', flat=True)

    total_score = 0
    question_results = []
    for question in course.question_set.all():
        q_selected = [cid for cid in selected_ids
                      if question.choice_set.filter(id=cid).exists()]
        is_correct = question.is_get_score(q_selected)
        if is_correct:
            total_score += question.grade
        question_results.append({
            'question': question,
            'is_correct': is_correct,
            'selected_choices': question.choice_set.filter(id__in=q_selected),
        })

    context = {
        'course': course,
        'total_score': total_score,
        'question_results': question_results,
        'passed': total_score >= 80,
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
