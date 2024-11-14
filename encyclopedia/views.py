from django.shortcuts import render
import markdown
from . import util
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
import random
# This returns the default index page.
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# This return the entry's page.
def title(request, name):
    nam = None
    text = None
    try:
        text = markdown.markdown(util.get_entry(name))
        for line in util.get_entry(name).split("\n"):
            if line.startswith('# '):
                nam = line[2:].strip()
                break
            else:
                nam = name
    except:
        nam = "Not Found"
        text = f"Sorry, there is no page for {name}"      
    return render(request, "encyclopedia/title.html", {
        "title": nam,
        "text": text
    })

# This is for search bar.
def search(request):
    if request.method == 'POST':
        entries = util.list_entries()
        query = request.POST.get('query', '')
        entries = [entry.lower() for entry in entries]
        if query.lower() in entries:
            return title(request,query) # Code until this line redirect user to the query of page which is present
        
# Now the code for the query which matches that of data        
        q = 0
        p_entries = list()
        for entry in entries:
            if query.lower() in entry:
                q = 1
                p_entries.append(entry)
        if q == 1:
            return render(request, "encyclopedia/search.html",{
            'q': q,
            'entries': p_entries
        })
    # for the code if the entry is releavent to the data present
        elif q == 0:
            return render(request, "encyclopedia/search.html",{
                'q': q,
                'search': query
            })
        
# for making form we will make a form class
class NewForm(forms.Form):
    #This is a sub class made from Form class in the forms file or module.
    entry = forms.CharField(label='Enter Title')
    text = forms.CharField(widget=forms.Textarea, label='Write the content here')



#This code is for making a new entry.
def new_page(request):
    if request.method == 'POST': #run when form is submitted
        entries = util.list_entries()
        form = NewForm(request.POST) # Makes the form which handles the POST request.
        if form.is_valid():
            entry = form.cleaned_data['entry']
            text = form.cleaned_data['text']
            entries = [entry.lower() for entry in entries]
            if entry.lower() in entries:
                a = 1
                return render(request, 'encyclopedia/new_page.html', {
                    'a':a,
                    'entry':entry
                    })
            else:
                util.save_entry(entry, ('# '+entry+'\n'+text))
                return title(request,entry)
    a = 0
    # run to give a form to the user.
    return render(request, "encyclopedia/new_page.html",{
        'a':a,
        'form' : NewForm()
    })


# A form for editing the content of entry
class EditForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)

# This code is for changing a previous entry.
def edit_page(request, name):
    # Getting data from the markdown file
    data = util.get_entry(name)
    if request.method == 'POST':
        form = EditForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            util.save_entry(name, text)
            return title(request,name)
    return render(request,'encyclopedia/edit_page.html',{
        'title':name,
        'form': EditForm ({ 'text':data})
    })


# This code is for giving a random page to the user
def random_page(request):
    '''It renders a random page'''
    page = random.choice(util.list_entries())
    return title(request, page)
