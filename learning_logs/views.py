from django.shortcuts import render, redirect,get_object_or_404
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404


# Create your views here.
def index(request):
    return render(request, 'learning_logs/index.html')


@login_required
def topics(request):
    # topics_ls = Topic.objects.order_by('date_added')
    topics_ls = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics_ls}
    return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
    #topic_ls = Topic.objects.get(id=topic_id)
    topic_ls=get_object_or_404(Topic,id=topic_id)
    if topic_ls.owner != request.user:
        raise Http404
    entries = topic_ls.entry_set.order_by('-date_added')
    context = {'topic': topic_ls, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()

            return redirect('learning_logs:topics')
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'post':
        form = EntryForm()
    else:
        form = EntryForm(data=request.post)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404
    if request.method != 'post':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.post)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
