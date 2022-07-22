from flask import session
import requests, json

# Define a class for Card
'''
We have taken name of card, id of card, listname and lsitnameID as properties
'''
class Card:
        def __init__(self, id, name, statusid, status = 'To Do'):
            self.id = id
            self.name = name
            self.statusid = statusid   # listnameID
            self.status = status       # listname

class Category:
    def __init__(self, id, name):
        self.id = id
        self.name = name


def get_cards(url, trellobid, apikey, apitoken):
    """
    Fetches all cards from ToDo list on Trello.

    Returns:
        Dictionary: 
        element 1: The list of Cards as objects - cards from all categories on Trello Board on website
        element 2: The list of all categories as objects containing id and name
    """
    getcardsurl = url+"1/boards/"+trellobid+"/lists?cards=open&key="+apikey+"&token="+apitoken
    headers = {
        'Accept': "application/json"
    }
    r = requests.get(url = getcardsurl, headers=headers)
    carddata = r.json()         # response of this call is a python list of dictionaries
                                # every member of list is a dictionary of cards in that category
    list_nums = len(carddata)   # number of lists - "Done, TO Do, Doing"
    all_cards = []
    all_lists = []             # list of all cards
    if r.status_code == 200:
        for num in range(list_nums):    # go through the lists
            list_name = carddata[num]['name']
            list_name_id = carddata[num]['id']
            all_lists.append( Category( list_name_id, list_name) )
            no_of_cards = len(carddata[num]['cards'])
            for cno in range(no_of_cards):  # go through cards in each list
                cname = carddata[num]['cards'][cno]['name']
                cid = carddata[num]['cards'][cno]['id']

                # Create a list of objects of the class card
                all_cards.append( Card(cid, cname, list_name_id, list_name) )
    else:
        all_cards.append( Card("No ID", "No Name", "No type" ) )
    return { 'allcards': all_cards, 'all_card_category': all_lists }


def add_card(title_to_add, list_to_which_added, url, trellobid, apikey, apitoken):
    """
    Adds a new Card with the specified title to To Do list.

    Args:
        title: The title of the item, Status to be kept. CALL URL, Board ID, API key and API Token

    Returns:
        item: The saved item.
    """
    # Fetch all cards to make sure we don't duplicate
    # Get "To DO" list ID
    all_card_list = []
    cards = get_cards(url, trellobid, apikey, apitoken) # This is a dict of all_cards and categories
    for card in cards['allcards']:
        all_card_list.append(card.name) # Create a list of all card names
    
    # Get the id of the Category
    list_id = "empty"
    for category in cards['all_card_category']:
        if list_to_which_added ==  category.name:
            list_id = category.id

    # Add the item to the lists if it is not already there 
    if title_to_add not in all_card_list and list_id != "empty":
        addcardurl = url+"1/cards?name="+title_to_add+"&idList="+list_id+"&key="+apikey+"&token="+apitoken
        #print (addcardurl)
        headers = {
            'Accept': "application/json"
        }
        c = requests.post(url = addcardurl, headers=headers)
        cdata = c.json()
    else:
        cdata = "Already Present"

    return cdata

def update_card(title_to_update, list_to_which_added, url, trellobid, apikey, apitoken):
    """
    Update an existing Card in the Board. If no existing item matches the ID of the specified item, nothing is updated.

    Args:
        title: The title of the item. CALL URL, Board ID, API key and API Token
    """
    # Fetch all cards to make sure the card exists
    
    all_card_list = []
    existing_items = get_cards(url, trellobid, apikey, apitoken)
    for card in existing_items['allcards']:
        all_card_list.append(card.name) # Create a list of all card names
        if title_to_update == card.name:
            id_to_update = card.id

    # Get the id of the Category
    list_id = "empty"
    for category in existing_items['all_card_category']:
        if list_to_which_added ==  category.name:
            list_id = category.id

    if title_to_update in all_card_list and list_id != "empty":
        updatecardurl = url+"1/cards/"+id_to_update+"?idList="+list_id+"&key="+apikey+"&token="+apitoken
        headers = {
            'Accept': "application/json"
        }
        u = requests.put(url = updatecardurl, headers=headers)
        udata = u.json()
    else:
        udata = "Not Present"

    return udata