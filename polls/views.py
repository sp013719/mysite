# coding=utf-8
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from polls.models import Poll, Choice
import logging

# Get an instance of logger
logger = logging.getLogger(__name__)
 
def index(request):	
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    logger.info('index is requested')
    context = {'latest_poll_list': latest_poll_list}
    return render(request, 'polls/index.html', context) 
 
def detail(request, poll_id):
    try:
        poll = Poll.objects.get(pk=poll_id)
    except Poll.DoesNotExist:
        raise Http404 # 產生 404 回應
    return render(request, 'polls/detail.html', {'poll': poll})

def results(request, poll_id):
	poll = get_object_or_404(Poll, pk=poll_id)
	return render(request, 'polls/results.html', {'poll': poll})

def vote(request, poll_id):
	poll = get_object_or_404(Poll, pk=poll_id)
	try:
		selected_choice = poll.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'polls/detail.html', {
			'poll': poll,
			'error_message': "You didn't select a choice.",
		})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		return HttpResponseRedirect(reverse('polls:results', args=(poll.id,)))
