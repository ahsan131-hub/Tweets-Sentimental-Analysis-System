import json

from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from tweetSentiments.model_controller import get_translated_tweets, analyze_tweets_pre_trained_model
from tweetSentiments.models import Question, Choice


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # template = loader.get_template('tweetSentiments/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }

    return render(request, 'tweetSentiments/index.html', context)


@csrf_exempt
def evaluate(request):
    data = json.load(request)
    to_date = data["toDate"]
    keywords = data["keywords"]
    from_date = data["fromDate"]
    limit = data["limit"]
    model = data["model"]
    print(to_date)
    print(from_date)
    print(keywords)
    # print(evaluateTweetsStats(keywords))
    tweets = evaluateTweetsStats(keywords, from_date, to_date, limit)
    stats_array = analyze_tweets_pre_trained_model(tweets, model)
    print(stats_array)
    return JsonResponse({"data": tweets, "stats": stats_array})
    # return JsonResponse({"data": "tweets"})


def detail(request, question_id):
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    # return render(request, 'tweetSentiments/detail.html', {'question': question})
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'tweetSentiments/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'tweetSentiments/results.html', {'question': question})


def vote(request, question_id):
    # return HttpResponse("You're voting on question %s." % question_id)
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, "tweetSentiments/detail.html", {
            "question": question, "error_message": "You did not selected any choice!"
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("results", args=(question.id,)))


def evaluateTweetsStats(keywords, from_date, to_date, limit):
    # print(keywords)
    tweets = get_translated_tweets(keywords, from_date, to_date, limit)
    i = 1
    for sentence in tweets:
        print(f"{i} :    {sentence['tweet']}   ")
        print(f"{i} :    {sentence['date']}   ")
        i += 1
    return tweets
