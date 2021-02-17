import random
from django.shortcuts import render
from .models import WordTable as Word

NUM = Word.objects.all().count()
MAX_SIZE = 4
word_queue = [0]
cur = 1


def _use_data_list(content):
    # 用于数据的左右遍历
    global word_queue, cur
    word_queue.append(content)
    word_queue[0] += 1
    cur = len(word_queue) - 1
    if word_queue[0] >= MAX_SIZE:
        word_queue.pop(1)
        word_queue[0] -= 1


# Create your views here.
def index(request):
    content = dict()
    w = Word.objects.get(pk=random.randrange(1, NUM))
    w.use_num += 1
    w.save()
    content['word'] = w.word
    content['trans'] = w.trans
    _use_data_list(content)
    return render(request, 'index.html', context={'content': content})


def left(request):
    global cur
    cur -= 1
    if word_queue[0] == 0 or cur == 0:
        cur = len(word_queue) - 1
    return render(request, 'index.html', context={'content': word_queue[cur]})


def right(request):
    global cur
    cur += 1
    if cur > len(word_queue) - 1:
        cur = 1
    return render(request, 'index.html', context={'content': word_queue[cur]})


def translate(request):
    content = dict()
    res = request.GET.get('word')
    w = Word.objects.filter(word__contains=res)
    if w:
        content['word'] = w[0].word
        content['trans'] = w[0].trans
        _use_data_list(content)
        return render(request, 'index.html', context={'content': content})
    else:
        return index(request)