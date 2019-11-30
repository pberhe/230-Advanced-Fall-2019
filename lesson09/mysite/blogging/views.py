from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from blogging.models import Post
from django.template import loader
from django import forms
from django.utils import timezone
from blogging.forms import MyCommentForm
from datetime import datetime


def stub_view(request, *args, **kwargs):
    body = "Stub View\n\n"
    if args:
        body += "Args:\n"
        body += "\n".join(["\t%s" % a for a in args])
    if kwargs:
        body += "Kwargs:\n"
        body += "\n".join(["\t%s: %s" % i for i in kwargs.items()])
    return HttpResponse(body, content_type="text/plain")


def list_view(request):
    published = Post.objects.exclude(published_date__exact=None)
    posts = published.order_by('-published_date')
    context = {'posts': posts}
    return render(request, 'blogging/list.html', context)


def detail_view(request, post_id):
    published = Post.objects.exclude(published_date__exact=None)
    try:
        post = published.get(pk=post_id)
    except Post.DoesNotExist:
        raise Http404
    context = {'post': post}
    return render(request, 'blogging/detail.html', context)


def add_model(request):
    if request.method == "POST":
        form = MyCommentForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.created_date = datetime.now()
            model_instance.modified_date = datetime.now()
            model_instance.published_date = datetime.now()
            model_instance.save()
            return redirect('/')
    else:
        form = MyCommentForm()
        return render(request, "blogging/comment_template.html", {'form': form})
