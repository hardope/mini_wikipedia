from django.shortcuts import render
import markdown2
from . import util
from django import forms
import random
from django.urls import reverse
from django.http import HttpResponseRedirect



def index(request):
    try:
        name = request.GET.get('value', '')
        if name == '':
            raise NameError
        fetch_entry(name)
        print(fetch_entry(name))
        if fetch_entry(name) == None:
            match_list = []
            for entry_name in util.list_entries():

                if name in entry_name:
                    match_list.append(entry_name)
            if match_list == []:
                pass
            else:
                return render(request, "encyclopedia/results.html",{
                    'list': match_list
                })
        return render(request, "encyclopedia/entry.html")

    except:
        pass

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        })

def search_que(request, name):
    if request.method == "POST":
        name = request.POST.get("name")
        entry = request.POST.get("entry")
        if name in util.list_entries():
            return render(request, "encyclopedia/error.html", {
                'error': 'Entry Exists'
            })
        else:
            util.save_entry(name, entry.lstrip())
            HttpResponseRedirect("name")


    if name == 'random':
        name = util.list_entries()
        name = name[random.randint(0, len(util.list_entries())-1)]
        fetch_entry(name)
        return render(request, "encyclopedia/entry.html", {
            'name': name
        })

    elif name == 'new_entry':
        return render(request, "encyclopedia/new.html")

    else:
        fetch_entry(name)
        return render(request, "encyclopedia/entry.html", {
            'name': name
        })

def edit(request, name):
    if request.method == 'GET':
        entry = util.get_entry(name)
        return render(request, "encyclopedia/edit.html", {
            'name': name,
            'entry': entry
        })
    else:
        entry = request.POST.get("entry")
        util.save_entry(name, entry)
        fetch_entry(name)
        return render(request, "encyclopedia/entry.html", {
            'name': name
        })

def fetch_entry(name):
    check = 1
    entries = util.get_entry(name)

    if entries == None:
        entries = f"<h1>{name} was not found.<h1>"
        check = 0

    entries = markdown2.markdown(entries)

    with open('encyclopedia/templates/encyclopedia/entries.html', 'w') as f:
        f.write(entries)
    if check == 1:
        return 'found'
     