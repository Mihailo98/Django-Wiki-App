import random
from django.urls import reverse
from django.shortcuts import redirect, render
from django import forms
from . import util
from django.http import HttpResponse, HttpResponseRedirect
from markdown2 import Markdown

class newEntryFormm(forms.Form):
    page_Title = forms.CharField(max_length=50)
    content = forms.CharField(widget=forms.Textarea())

class editForm(forms.Form):
    edit_Content = forms.CharField(widget=forms.Textarea())

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    t = util.get_entry(title)
    md = Markdown()
    if t == None:
        return render(request, "encyclopedia/entry.html", {
            'title': 'This entry does not exist'
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            'title': md.convert(t)
        })

def new(request):
    if request.method == 'POST':
        f = newEntryFormm(request.POST)
        if f.is_valid():
            t = f.cleaned_data['page_Title']
            c = f.cleaned_data['content']
            if util.get_entry(t):
                return HttpResponse('This entry already exist')
            util.save_entry(t, c)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "encyclopedia/new_entry.html", {
                'newEntry': f
            })
    return render(request, "encyclopedia/new_entry.html", {
        'newEntry': newEntryFormm()
    })

def edit(request, naziv):
    if request.method == 'POST':
        content = util.get_entry(naziv)
        f = editForm(content)
        if f.is_valid():
            c = f.cleaned_data['edit_Content']
            util.save_entry(naziv, c)
        else:
            return render(request, "encyclopedia/edit.html", {
                'editForm': f,
                'title': naziv
            })
    return render(request, "encyclopedia/edit.html", {
        'editForm': editForm(),
        'title': naziv
    })


def randompage(request):
    naziv = random.choice(util.list_entries())
    return render(request, "encyclopedia/random.html", {
        "entries":  naziv
    })
     