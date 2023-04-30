from django.shortcuts import render
from django.http import HttpResponse
from .forms import NameForm


values = []
  
# create a function
def geeks_view(request):
    # create a dictionary to pass
    # data to the template
    # if len(values) > 0:
    #     del(values[:])
    if request.method == "POST":
        form = NameForm(request.POST)   
        if form.is_valid():
            cleaned_data = form.cleaned_data
            value = list(cleaned_data.values())[0]
            values.append(value)

    context ={
        "data":"Gfg is the best",
        "list": values,

        # "list":[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    }
    # return response with template and context
    return render(request, "template.html", context)




# def index(request):
#     response = HttpResponse()
#     response.write("<p>Test Text</p>")
#     response.write("<p>Here's another paragraph</p>")
#     return response
# # Create your views here.
