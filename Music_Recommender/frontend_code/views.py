from django.shortcuts import render
from django.http import HttpResponse
from .forms import NameForm


values = []
  
test_dict = { 
    "Dior":"5",
    "Ddu-Ddu":"2",
    "Fancy": "4"
}

# create a function
def selector_page(request):
    bad_songName = False
    if request.method == "POST":
        form = NameForm(request.POST)   
        if form.is_valid():
            cleaned_data = form.cleaned_data
            value = list(cleaned_data.values())[0]
            if value in test_dict:
                values.append(value)
            else:
                bad_songName = True


    context ={
        "list": values,
        "bad_songName": bad_songName
    }
    # return response with template and context
    return render(request, "template.html", context)


def reset_list(request):
    # create a dictionary to pass
    # data to the template
    if len(values) > 0:
        del(values[:])
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

def results(request):
    output = []
    '''
    CALL FUNCTIONS FOR RESULTS HERE AND STORE IN OUTPUT
    '''
    context = {
        "final_results:"

    }


    return render(request, "song_output.html", context)




# create a dictionary to pass
    # # data to the template
    # if len(values) > 0:
    #     del(values[:])
    # if request.method == "POST":
    #     form = NameForm(request.POST)   
    #     if form.is_valid():
    #         cleaned_data = form.cleaned_data
    #         value = list(cleaned_data.values())[0]
    #         values.append(value)

    # context ={
    #     "data":"Gfg is the best",
    #     "list": values,

        # "list":[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # }    
    # return response with template and context



# def index(request):
#     response = HttpResponse()
#     response.write("<p>Test Text</p>")
#     response.write("<p>Here's another paragraph</p>")
#     return response
# # Create your views here.
