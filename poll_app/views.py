from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Question, Choice
from django.db.models import Max


def home(request):
    question_list = Question.objects.all()
    context = {'question_list': question_list}
    return render(request, 'poll_app/home.html', context)


def results(request, question_id):
    labels = []
    data = []

    question = get_object_or_404(Question, pk=question_id)
    choices_order = question.choice_set.order_by('-votes')

    for choice in choices_order:
        labels.append(choice.choice_name)
        data.append(choice.votes)
    return render(request, 'poll_app/results.html',
                  {'question': question, "choices_order": choices_order, 'labels': labels, 'data': data, })


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'poll_app/home.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('results', args=(question.id,)))
