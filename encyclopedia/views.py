import secrets
from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util
from markdown2 import Markdown


class Create(forms.Form):
    title = forms.CharField(label="title", max_length=50)
    markdown = forms.CharField(label="markdown",widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request,title):
    return render(request, "encyclopedia/entry.html", {
           "entry": Markdown().convert(((util.get_entry(title)))),
           "title": title
     })
 

def search(request):
   value = request.GET.get("q")
   if(util.get_entry(value) is not None):
        return HttpResponseRedirect(reverse("title", kwargs={'title': value}))
   else:
        substrings = []
        # looping through the entries in the list
        for entry in util.list_entries():
            # if the character in value is in the entry then append the entry to the substring list
            if value.lower() in entry.lower():
                substrings.append(entry)

        return render(request,"encyclopedia/result.html", {
            "entries": substrings,
            "value": value
        })

def create(request):
    if request.method == "POST":
        form = Create(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            markdown = form.cleaned_data["markdown"]
            if util.get_entry(title):
                return render(request, "encyclopedia/create.html", {
                    "form": Create(),
                    "error": "Entry already exists"
                })
                
            else:
                util.save_entry(f"#{title}",markdown)
                return HttpResponseRedirect(reverse("title", kwargs={'title': title}))
    else:
        return render(request,"encyclopedia/create.html", {
            "form": Create()
        })



def edit(request,title):
  if request.method == "POST":
         title = request.POST["title"]
         markdown = request.POST["markdown"]
         util.save_entry(title,markdown)
         return HttpResponseRedirect(reverse("title", kwargs={"title": title}))
  else:
        return render(request,"encyclopedia/edit.html", {
            "content": util.get_entry(title),
            "title": title,
            
        })


def random(request):
    random=secrets.choice(util.list_entries())
    return HttpResponseRedirect(reverse("title", kwargs={"title": random}))