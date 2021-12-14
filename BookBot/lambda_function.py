import json
import random
import decimal 

# Random Price Function for Books
def random_num():
    return(decimal.Decimal(random.randrange(100, 5000))/100)

def get_title(genre):
    if genre == 'Romance':
        titleList = ["Ravished and Ravenous", "Mermaids and Sirens", "Wild West Of the Heart", "Three's a Crowd", "To Capture a Ring"]
    
    elif genre == 'Fantasy':
        titleList = ["The Crown in the Mist", "Tears of Circe", "Hammer and the Inferno", "The Gilded Beast", "The Ember of the North"]

    elif genre == 'Sci-Fi':
        titleList = ["The Daughters of Atlas", "Cosmic Skull", "2938: Retribution", "Ragnorak Rising", "Bablon Dying"]

    elif genre == 'Mystery':
        titleList = ["Sign of the Burnt Tuba", "Case of the Four-Eyed Monkey", "The Buried Portrait", "Secret of the Spanish Tourists", "Sign of the Ghostly Turnip"]

    else:
        titleList = ["The Heirs of Earth Was", "Steel Duty", "Something Gained", "Darling Dearest", "Dagger in the Heart"]

    return titleList


# Helper LEX functions 
def get_slots(intent_request):
    return intent_request['sessionState']['intent']['slots']
    
def get_slot(intent_request, slotName):
    slots = get_slots(intent_request)
    if slots is not None and slotName in slots and slots[slotName] is not None:
        return slots[slotName]['value']['interpretedValue']
    else:
        return None    

def get_session_attributes(intent_request):
    sessionState = intent_request['sessionState']
    if 'sessionAttributes' in sessionState:
        return sessionState['sessionAttributes']

    return {}

def elicit_intent(intent_request, session_attributes, message):
    return {
        'sessionState': {
            'dialogAction': {
                'type': 'ElicitIntent'
            },
            'sessionAttributes': session_attributes
        },
        'messages': [ message ] if message != None else None,
        'requestAttributes': intent_request['requestAttributes'] if 'requestAttributes' in intent_request else None
    }


def close(intent_request, session_attributes, fulfillment_state, message):
    intent_request['sessionState']['intent']['state'] = fulfillment_state
    return {
        'sessionState': {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'Close'
            },
            'intent': intent_request['sessionState']['intent']
        },
        'messages': [message],
        'sessionId': intent_request['sessionId'],
        'requestAttributes': intent_request['requestAttributes'] if 'requestAttributes' in intent_request else None
    }

def FindGenre(intent_request):
    session_attributes = get_session_attributes(intent_request)
    slots = get_slots(intent_request)
    genre = get_slot(intent_request, 'bookGenre')
    price = '${:,.2f}'.format(random_num())
     
    bookTitle = random.choice(get_title(genre))
    text = "A great "+genre+" book is "+bookTitle+" and costs "+price+" dollars."
    message =  {
            'contentType': 'PlainText',
            'content': text
        }
    fulfillment_state = "Fulfilled"    
    return close(intent_request, session_attributes, fulfillment_state, message)   

    
def dispatch(intent_request):
    intent_name = intent_request['sessionState']['intent']['name']
    response = None
    # Dispatch to your bot's intent handlers
    if intent_name == 'FindGenre':
        return FindGenre(intent_request)

    raise Exception('Intent with name ' + intent_name + ' not supported')

def lambda_handler(event, context):
    response = dispatch(event)
    return response
