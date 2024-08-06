from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from . import util
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
        print(type(html_conversion))
        print(title)
        return render(request, "encyclopedia/enc.html", {
            "title": title,
            "html_conversion": html_conversion,
        })
    except:
        return render(request, "encyclopedia/error.html", {
            "error": f"There is no page for {title}"
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