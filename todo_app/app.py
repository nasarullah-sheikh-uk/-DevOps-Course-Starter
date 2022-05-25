from flask import Flask

# we need to import this method for rendering templates and is not imported by default
from flask import render_template  , redirect

# we need request module to query the application from browser
from flask import request

########################################################################################
#####  The default repo has some functions written in ./data/sessions_items.py
####   Importing functions written under ./data/sessions_items.py
#####
from todo_app.data.session_items import get_items
from todo_app.data.session_items import get_item
from todo_app.data.session_items import add_item
from todo_app.data.session_items import save_item
from todo_app.data.session_items import remove_item   # I have added this for strech goal

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())

# to test hello works
@app.route('/hello')
def hello():
    return '...it is working!! .....Hello, World'


@app.route('/')
def index():
    # The index page should go to templates/index.html
    # unsorted
    #current_items=get_items()

    # TASK sort by status
    # sort the list of dictionaries by a dictionay key
    # Sorting a list of dictionaries raises an error by default if sorted() is used
    # reference - https://note.nkmk.me/en/python-dict-list-sort/
    # sorting by status key
    current_items=sorted(get_items(), key=lambda x: x['status'])  
    return render_template('index.html', items=current_items)


############################################################################################
#  Adding a route/URL path to add new item
#  This takes the form data from index page, so a form needs to be added there
##
@app.route('/additem', methods=['GET', 'POST'])
def additem():
    if request.method == 'POST':
        title_to_add=request.form.get('title')  # i have named title in index.html form
        add_item(title_to_add)
        ##  If you want to reset the item list -- u will have to create a new browser session
        return redirect('/')                    # requested in task to use redirect
    else:
        return redirect('/')



############################################################################################
#  Adding a route/URL path to mark an item complete
#  This takes the form data from index page, so a form needs to be added in template/index.html
##
@app.route('/updateitem', methods=['GET', 'POST'])
def updateitem():
    if request.method == 'POST':
        id_to_update=request.form.get('ID')  # i have named ID in index.html form
        whole_item=get_item(id_to_update)    # Check if we have the ID otherwise go back
        if whole_item is None:
            ##  No ID Go back to main page
            return redirect('/') 
        else:
            whole_item.update({'status': 'Complete'})
            save_item(whole_item)
            return redirect('/')            # Once updated go to index and show
    else:
        return redirect('/')


############################################################################################
#  Adding a route/URL path to remove an item 
#  This takes the form data from index page, so a form needs to be added in template/index.html
##
@app.route('/removeitem', methods=['GET', 'POST'])
def removeitem():
    if request.method == 'POST':
        id_to_remove=request.form.get('RID')  # i have named ID in index.html form
        remove_item(id_to_remove)
        return redirect('/') 
    else:
        return redirect('/')


    

