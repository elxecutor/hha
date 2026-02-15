from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import QuestionForm
from .models import Question


def submit_question(request):
    """Handle question submission"""
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save()
            messages.success(request, 'Your question has been submitted successfully!')
            return redirect('questions:submit')
    else:
        form = QuestionForm()

    context = {
        'form': form,
        'title': 'Ask a Question'
    }
    return render(request, 'questions/submit.html', context)


def view_questions(request):
    """Display submitted questions (for admin/staff review)"""
    # Only show questions if user is staff/admin
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to view questions.')
        return redirect('core:index')

    questions = Question.objects.all()
    paginator = Paginator(questions, 20)  # 20 questions per page
    page = request.GET.get('page', 1)
    questions_page = paginator.get_page(page)

    context = {
        'questions': questions_page,
        'title': 'Question Bank'
    }
    return render(request, 'questions/list.html', context)
