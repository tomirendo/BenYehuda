from django.shortcuts import render

# Create your views here.
def index(req):
    return render("index.html")
def script(req):
    return render("script.js")
