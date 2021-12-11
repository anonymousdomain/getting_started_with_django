from django.shortcuts import render


# Create your views here.
def pizza(request):
    return render(request, "pizzeria/pizza.html")
