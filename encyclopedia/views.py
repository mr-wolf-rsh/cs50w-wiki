from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from markdown2 import markdown
from random import randint

from . import util


class TextAreaForm(forms.Form):
    content = forms.CharField(label="Content:",
                              widget=forms.Textarea(attrs={"rows": 20, "cols": 30}))


class NewEntryForm(TextAreaForm):
    file_name = forms.CharField(label="File Name:", required=True)
    field_order = ['file_name', 'content']


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "title_var": "All Pages"
    })


def select_entry(request, entry_name):
    entry = util.get_entry(entry_name)
    return render(request, "encyclopedia/entry.html", {
        "entry_name": entry_name,
        "entry": markdown(entry) if entry is not None and entry != '' else entry
    })


def search_entry(request):
    q = request.GET.get('q', '')
    if not q:
        return HttpResponseRedirect(reverse("encyclopedia:index"))
    filtered = [e for e in util.list_entries() if q.lower() in e.lower()]
    if len(filtered) != 1 or filtered[0].lower() != q.lower():
        return render(request, "encyclopedia/index.html", {
            "entries": filtered,
            "title_var": "Search Results"
        })
    else:
        return redirect("encyclopedia:select_entry", entry_name=filtered[0])


def create_entry(request):
    if request.method == "POST":
        new_entry_form = NewEntryForm(request.POST)
        if new_entry_form.is_valid():
            entry_name = new_entry_form.cleaned_data["file_name"]
            entry = util.get_entry(entry_name)
            if entry:
                return render(request, "encyclopedia/new_page.html", {
                "new_entry_form": new_entry_form,
                "already_exists": True
                })
            content = new_entry_form.cleaned_data["content"] + "\n"
            util.save_entry(entry_name, content)
            return redirect("encyclopedia:select_entry", entry_name=entry_name)
        else:
            return render(request, "encyclopedia/new_page.html", {
                "new_entry_form": new_entry_form,
                "already_exists": False
            })
    else:
        return render(request, "encyclopedia/new_page.html", {
            "new_entry_form": NewEntryForm(),
                "already_exists": False
        })


def edit_entry(request, entry_name):
    if request.method == "POST":
        textarea_form = TextAreaForm(request.POST)
        if textarea_form.is_valid():
            content = textarea_form.cleaned_data["content"] + "\n"
            util.save_entry(entry_name, content)
            return redirect("encyclopedia:select_entry", entry_name=entry_name)
        else:
            return render(request, "encyclopedia/edit_page.html", {
                "entry_name": entry_name,
                "textarea_form": textarea_form
            })
    else:
        entry = util.get_entry(entry_name)
        return render(request, "encyclopedia/edit_page.html", {
            "entry_name": entry_name,
            "textarea_form": TextAreaForm(initial={'content': entry}) if entry is not None else None
        })


def randomize(request):
    entries = util.list_entries()
    page = entries[randint(0, len(entries) - 1)]
    return redirect("encyclopedia:select_entry", entry_name=page)
