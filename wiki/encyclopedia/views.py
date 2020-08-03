from django.shortcuts import render, redirect
from django import forms
from os import path
from wiki.settings import BASE_DIR
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def title(request, title):
    return render(request, "encyclopedia/content.html", {"content": util.get_entry(title), "title": title})


def search(request):
    search = request.POST['q']
    lst = util.sub_query(str(search))
    if util.get_entry(search) is not None:
        return redirect(f'/{search}')
    elif len(lst) != 0:
        return render(request, "encyclopedia/index.html", {"entries": lst})
    else:
        return render(request, "encyclopedia/content.html", {"title": "Not Found"})


class NewPage(forms.Form):

    # class Meta:
    header = forms.CharField(label="New Header")
    body = forms.CharField(label="New Content",
                           widget=forms.Textarea(attrs={'rows': 3}))


class EditForm(forms.Form):
    body = forms.CharField(
        label="Edit", widget=forms.Textarea(attrs={"size": "80"}), empty_value="hello")


def create(request):
    return render(request, "encyclopedia/create.html", {"form": NewPage()})


def add(request):
    # boilerplate data validation
    if request.method == "POST":
        form = NewPage(request.POST)
        if form.is_valid():
            title = form.cleaned_data["header"]
            body = form.cleaned_data["body"]
            # this part takes care of the md file generation
            if util.get_entry(title.capitalize()) is None:
                file_path = path.join(
                    BASE_DIR, f'entries/{title.capitalize()}.md')
                with open(file_path, "w") as file:
                    file.write(f"# {title.capitalize()} \n \n")
                    file.write(body)
                # redirect to the new website if successful
                return redirect(f'/{title}')
            # duplicate finder
            else:
                return render(request, "encyclopedia/content.html", {"message": "Error: Duplicate found"})

        # re-renders the page if the input form is invalid
        else:
            return render(request, "encyclopedia/create.html", {'form': form})
    # if the request method is not post
    return render(request, "encyclopedia/create.html", {"form": NewPage()})


def edit(request, title):
    file_path = path.join(
        BASE_DIR, f'entries/{title.capitalize()}.md')
    with open(file_path, "r") as content:
        return render(request, "encyclopedia/edit.html", {'form': EditForm(), 'title': title})
