from flask import session
import requests, json

# Define a class for Card type 
class Item:
        def __init__(self, id, name, statusid, status = 'To Do'):
            self.id = id
            self.name = name
            self.statusid = statusid
            self.status = status

'''   
        @classmethod
        def from_trello_card(cls, id, name, list):
           return cls( id, name, list )
'''


def get_items(url, trellobid, apikey, apitoken):
    """
    Fetches all cards from ToDo list on Trello.

    Returns:
        list: The list of Cards in All lists on Trello Board.
    """
    getcardsurl = url+"1/boards/"+trellobid+"/lists?cards=open&key="+apikey+"&token="+apitoken
    headers = {
        'Accept': "application/json"
    }
    r = requests.get(url = getcardsurl, headers=headers)
    carddata = r.json()
    card_nums = len(carddata)
    all_cards = []
    if r.status_code == 200:
        for num in range(card_nums):
            card_type = carddata[num]['name']
            card_type_id = carddata[num]['id']
            no_of_cards = len(carddata[num]['cards'])
            for cno in range(no_of_cards):
                cname = carddata[num]['cards'][cno]['name']
                cid = carddata[num]['cards'][cno]['id']
                all_cards.append( Item(cid, cname, card_type_id, card_type) )
    else:
        all_cards.append( Item("No ID", "No Name", "No type" ) )

    return all_cards

def add_item(title_to_add, list_to_which_added, url, trellobid, apikey, apitoken):
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
    status_dict = {}
    items = get_items(url, trellobid, apikey, apitoken)
    for item in items:
        all_card_list.append(item.name) # Create a list of all card names
        status_dict[item.status] = item.statusid # Create a  dict of Status/List-> Status/ListId
    if list_to_which_added in status_dict:
        to_do_id = status_dict[list_to_which_added]
    else:
        to_do_id = status_dict["To Do"]

    # Add the item to the lists if it is not already there 
    if title_to_add not in all_card_list:
        addcardurl = url+"1/cards?name="+title_to_add+"&idList="+to_do_id+"&key="+apikey+"&token="+apitoken
        #print (addcardurl)
        headers = {
            'Accept': "application/json"
        }
        c = requests.post(url = addcardurl, headers=headers)
        cdata = c.json()
    else:
        cdata = "Already Present"

    return cdata

def update_item(title_to_update, list_to_which_added, url, trellobid, apikey, apitoken):
    """
    Update an existing Card in the Board. If no existing item matches the ID of the specified item, nothing is updated.

    Args:
        title: The title of the item. CALL URL, Board ID, API key and API Token
    """
    # Fetch all cards to make sure the card exists
    
    all_card_list = []
    status_dict = {}
    existing_items = get_items(url, trellobid, apikey, apitoken)
    for item in existing_items:
        all_card_list.append(item.name) # Create a list of all card names
        status_dict[item.status] = item.statusid # Create a  dict of Status/List-> Status/ListId
        if title_to_update == item.name:
            id_to_update = item.id
   
   # Get "To DO" list ID
   # Find the id of the list to update
    if list_to_which_added in status_dict:
        to_do_id = status_dict[list_to_which_added]
    else:
        to_do_id = status_dict["To Do"]

    
    if title_to_update in all_card_list:
        updatecardurl = url+"1/cards/"+id_to_update+"?idList="+to_do_id+"&key="+apikey+"&token="+apitoken
        headers = {
            'Accept': "application/json"
        }
        u = requests.put(url = updatecardurl, headers=headers)
        udata = u.json()
    else:
        udata = "Not Present"

    return udata