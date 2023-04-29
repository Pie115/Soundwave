from django.shortcuts import render
from django.http import HttpResponse
  
# create a function
def geeks_view(request):
    # create a dictionary to pass
    # data to the template
    context ={
        "data":"Gfg is the best",
        "list":[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    }
    # return response with template and context
    return render(request, "template.html", context)




# def index(request):
#     response = HttpResponse()
#     response.write("<p>Test Text</p>")
#     response.write("<p>Here's another paragraph</p>")
#     return response
# # Create your views here.
