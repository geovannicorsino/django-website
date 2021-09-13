from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import ToDoList, Item
from .forms import CreateNewList


# Create your views here.

def index(request, id):
    ls = ToDoList.objects.get(id=id)

    if request.method == "POST":
        if request.POST.get("save"):
            for item in ls.item_set.all():
                p = request.POST
                item.complete = "clicked" == p.get("c" + str(item.id))
                if "text" + str(item.id) in p:
                    item.text = p.get("text" + str(item.id))

                item.save()

        elif request.POST.get("add"):
            newItem = request.POST.get("new")
            if newItem != "":
                ls.item_set.create(text=newItem, complete=False)

    return render(request, "main/list.html", {"ls": ls})


def home(request):
    return render(request, "main/home.html", {})


def create(request):
    if request.method == "POST":
        form = CreateNewList(request.POST)

        if form.is_valid():
            n = form.cleaned_data["name"]
            t = ToDoList(name=n)
            t.save()
            request.user.todolist.add(t)
        return HttpResponseRedirect(f'/{t.id}')
    else:
        form = CreateNewList()
    return render(request, "main/create.html", {"form": form})


def view(request):
    lenght = len(request.user.todolist.all())
    return render(request, "main/view.html", {"lenght": lenght})
