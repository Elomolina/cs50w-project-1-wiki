from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from . import util
from . import forms
import random
import markdown2

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def encyclopedia(request, title):
    try:
        markdown = util.get_entry(title)
        html_conversion = markdown2.markdown(markdown)
        html_conversion = str(html_conversion)
        return render(request, "encyclopedia/enc.html", {
            "title": title,
            "html_conversion": html_conversion,
        })
    except:
        return render(request, "encyclopedia/error.html", {
            "error": f"There is no page for {title}"
        })


def edit(request, title):
    textarea = util.get_entry(title)
    data = {
        "textarea":textarea
    }
    # we pass the initial markdown
    form = forms.editMarkdown(initial=data)
    return render(request, "encyclopedia/edit.html", {
        "title":title,
        "form": form
    })

def search(request):
    if request.method == "POST":
        form = request.POST
        entry = form['q']
        entry = entry.lower()
        entries = []
        for i in util.list_entries():
            entries.append(i.lower())
        #check the exact entry
        if entry in entries:
            redirect_path = reverse("encyclopedia", args = [entry])
            return HttpResponseRedirect(redirect_path)
        else:
            #check substring
            entries_substring = []
            for i in entries:
                if entry in i:
                    entries_substring.append(i)
            if not entries_substring:
                return render(request, "encyclopedia/error.html", {
                    "error": f"There are no entries similar to: {entry}"
                })
            request.session["substrings"] = entries_substring
            request.session["entry"] = entry
            redirect_path = "similar"
            return HttpResponseRedirect(redirect_path)

def similar(request):
    return render(request, "encyclopedia/similar.html", {
        "session": request.session,
    })

def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    redirect_path = reverse("encyclopedia", args = [random_entry])
    return HttpResponseRedirect(redirect_path)


def create(request):
    if request.method == "POST":
        form = forms.createForm(request.POST)
        #check if all inputs are valid
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            entry = util.get_entry(title)
            #check if entry already exist
            if entry is not None:
                return render(request, "encyclopedia/create.html", {
                "form": form,
                "entry": title.lower()
                })
            #creates new entry if it doesnt exist
            else:
                #save entry 
                util.save_entry(title, content)
                redirect_path = reverse("encyclopedia", args = [title])
                return HttpResponseRedirect(redirect_path)
        #return the same form with the error messages
        else:
            return render(request, "encyclopedia/create.html", {
                "form": form
            })
    # get request
    return render(request, "encyclopedia/create.html", {
        "form": forms.createForm()
    })