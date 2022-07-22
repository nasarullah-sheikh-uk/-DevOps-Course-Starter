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
from todo_app.data.trello_items import get_cards
from todo_app.data.trello_items import add_card
from todo_app.data.trello_items import update_card
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
    # It will render a html with two forms and one table
    # It taks a list of objects called items which is a class card 
    # having name, id, status, statusid as properties
    return render_template('index.html', cards=get_cards(url, trellobid, apikey, apitoken))


############################################################################################
#  Adding a route/URL path to add new item
#  This takes the form data from index page
#  We are taking name of the card and its status/list as inputs
#####################################################################
@app.route('/addcard', methods=['GET', 'POST'])
def addcard():
    if request.method == 'POST':
        title_to_add=request.form.get('new_card_name')  # i have named title in index.html form
        list_to_which_added=request.form.get('status') # # i have named status as input from radio button in index.html form
        add_card(title_to_add, list_to_which_added, url, trellobid, apikey, apitoken)
        return redirect('/')                    # requested in task to use redirect
    else:
        return redirect('/')



############################################################################################
#  Adding a route/URL path to update a card 
#  This takes the form data from index page, it can update status/list of card
#  We also check if the card is there
##
@app.route('/updatecard', methods=['GET', 'POST'])
def updatecard():
    if request.method == 'POST':
        title_to_update=request.form.get('card_name')  # i have named this in index.html form
        list_to_which_added=request.form.get('status')
        update_card(title_to_update, list_to_which_added, url, trellobid, apikey, apitoken)
        return redirect('/')            # Once updated go to index and show
    else:
        return redirect('/')