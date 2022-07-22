from flask import Flask

# we need to import this method for rendering templates and is not imported by default
from flask import render_template , redirect

# we need request module to query the application from browser
from flask import request
import os

# Extract the ENV variables 
url = os.getenv('URL')
apikey = os.getenv('APIKEY') 
apitoken = os.getenv('APIToken')
trellobid = os.getenv('TrelloBID')

########################################################################################
#####  The default repo has some functions written in ./data/sessions_items.py
####   Importing functions written under ./data/sessions_items.py
#####
from todo_app.data.trello_items import get_items
from todo_app.data.trello_items import add_item
from todo_app.data.trello_items import update_item
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
    return render_template('index.html', items=get_items(url, trellobid, apikey, apitoken))


############################################################################################
#  Adding a route/URL path to add new item
#  This takes the form data from index page, so a form needs to be added there
##
@app.route('/additem', methods=['GET', 'POST'])
def additem():
    if request.method == 'POST':
        title_to_add=request.form.get('title')  # i have named title in index.html form
        list_to_which_added=request.form.get('status')
        add_item(title_to_add, list_to_which_added, url, trellobid, apikey, apitoken)
        ##  If you want to reset the item list -- u will have to create a new browser session
        return redirect('/')                    # requested in task to use redirect
    else:
        return redirect('/')



############################################################################################
#  Adding a route/URL path to update a card 
#  This takes the form data from index page, so a form needs to be added in template/index.html
##
@app.route('/updateitem', methods=['GET', 'POST'])
def updateitem():
    if request.method == 'POST':
        title_to_update=request.form.get('ID')  # i have named ID in index.html form
        list_to_which_added=request.form.get('status')
        update_item(title_to_update, list_to_which_added, url, trellobid, apikey, apitoken)
        return redirect('/')            # Once updated go to index and show
    else:
        return redirect('/')



    

