# Import libraries for analysis
import pandas as pd
import re
import nltk
from nltk.corpus import wordnet
nltk.download('omw-1.4')
nltk.download('wordnet')

"""## Load the Data"""

# Load the data that has already been cleaned
file_path = ('/content/drive/MyDrive/Implementation_Dataset/Training_Dataset.csv')
data = pd.read_csv(file_path)                                                  # Read the training Data
test = pd.read_csv  ('/content/drive/MyDrive/Implementation_Dataset/Testing_Dataset.csv') # Read the testing  Data

data_tag = pd.read_csv('/content/drive/MyDrive/Implementation_Dataset/Data_Categorization.csv')  # data tag

data_tag

"""## Tags, Responses and Synonymns values"""

# There are 19 list of intent for use in this case. This will define the response of our intents from the user.
# Define the intents, tag and response
dict_intent ={'intents': [{'tag': 'Alert',
                           'responses': 'Eskom power system is under severe pressure. Please switch off all unnecessary lights, your geyser, pool pump, and non-essential appliances. Thank you!',
                           'synonyms': {'Switch off', 'geyser', 'Pool pumps', 'Appliances', 'Severe pressure'}
                          },
                                       
                          {'tag': 'Anger',
                           'responses': 'Eskom is implementing efforts to restore energy supply. We apologise for the inconvenience caused.',
                           'synonyms': {'sucks','what the hell', 'wtf', 'ffs','fuck', 'hell','fucking', 'futsek', 'nje','tired', 'voetsek', 
                                        'fvcken tired', 'protestors', 'corrupt', 'nonsense', 
                                        'idiots', 'eish', 'fuck eskom', 'protest', 'shit', 'damn it', 
                                        'stupid', 'angry', 'incompetent bullshit', 'fuck off', 'mad'}
                           },
                          
                            {'tag': 'App',
                           'responses': 'Eskom customers can download their loadshedding schedules from loadshedding.eskom.co.za or on the MyEskom App.',
                           'synonyms': {'EskomSePush', 'app', 'Schedule', 'MyEskom App', 'Schedules'}
                          },

                          {'tag': 'Appreciation',
                           'responses': 'Thank you for reiterating our commitment to always providing excellent service!',
                           'synonyms': {'major strides', 'good strides', 'amazing', 'celebrate', 'remarkable', 'better', 'power restored', 
                                        'no more loadshedding', 'thank you', 'gratitude', 'well done'}
                          },

                          {'tag': 'Cable',
                           'responses': 'Cable theft is one of the main reasons for constant power outages. Report cable theft to @SAPoliceService/Eskom Crime Line 0800 11 27 22 (toll-free) or to your local municipality.',
                           'synonyms':{'stolen cable', 'Theft', 'Cable Theft' 'stealing', 'stolen', 'steal','stole',  'Arrest', 'copper cables','Arrested' }
                           },
                          
                          {'tag': 'Coal',
                           'responses': 'The anti-pollution system would increase the plant’s water consumption and increase carbon dioxide emissions.',
                           'synonyms': {'Emmissions', 'Pollution', 'Coal-fine'}
                           },
                          
                          {'tag': 'Debt',
                           'responses': 'The rising electricity debt is crippling Eskom power utility’s service delivery programme. Please, pay your bills!',
                           'synonyms': {'Arrears', 'Overdue', 'Bills', 'debt', 'Owes', 'Owed', 'Debts'}
                          },

                          {'tag': 'Financial',
                           'responses': 'This is not where we want to be as Eskom to ensure sustainability, but it’s a great start in the right direction.',
                           'synonyms': {'Profit', 'Interim report'}
                          },

                          {'tag': 'Illegal',
                           'responses': 'Buying illegal electricity vouchers and illegal connections is a crime. Consumers that are using illegal prepaid electricity vouchers will be disconnected and fined. Eskom encourages communities to play an active role in curbing these atrocities. Report ghost vendors and illegal connections to Eskom Crime Line on 0800 112722.',
                           'synonyms' : {'Illegal vouchers', 'Illegal connections', 'Illegal electricity'}
                          },

                          {'tag': 'Lights out',
                           'responses':'Eskom is implementing efforts to restore energy supply. The estimated time of restoration is currently unknown. We apologise for the inconvenience caused.',
                          'synonyms': {'Electricity shortage', 'Electricity', 'Electricity cut', 'Lights', 'Light', 'Power', 'Energy', 'Current', 'Voltage','No electricity', 'no power', 'electricity shortage', 'shortage of electricity', 'without electricy', 'no light', 'unacceptable', 'without power', 'dark', 'darkness', 'no power supply'}
                          },

                          {'tag': 'Loadshedding',
                           'responses': 'Please visit loadshedding.Eskom.co.za at any moment to see the current loadshedding status. We apologise for the inconvenience caused. Thank you!',
                           'synonyms': {'Loadshedding again', 'Eskom loadshedding', 'Load shedding', 'Load reduction', 'loadshedded', 'Load-shedding', 'Loadshed', 'Loadsheded'}
                          },
                           
                          {'tag': 'Maintenance',
                           'responses': 'Eskom is implementing efforts to achieve operational stability and to restore the security of energy supply for the country. We apologise for the inconvenience caused.',
                           'synonyms': {'Replacement', 'Koeberg Unit 2', 'Maintenances', 'Koeberg'}
                          },

                          {'tag': 'Outages',
                           'responses': 'We are attending to an outage affecting customers in your area. The estimated time of restoration is currently unknown. We apologise for the inconvenience caused.',
                           'synonyms': {'Power outage', 'Power cuts', 'Power outages', 'Black out', 'Power cut', 'outage', 'Power trip', 'Power failure', 'Power off'}
                          },


                          {'tag': 'Price',
                           'responses': 'The price hike is partly being driven by purchases from independent power producers (IPPs) and carbon taxes – two costs that are outside of Eskom"s direct control',
                           'synonyms': {'Increase','Increases', 'Tariffs', 'Prices', 'Price hikes', 'Tariffincrease','Hikes','Tariff hike', 'NERSA', '20.5%', 'Price hike', 'Tariff application', 'Units', '1 April', 'Rate hikes', 'Tariff increase'}
                          },

                          {'tag': 'Stage',
                           'responses': 'Eskom has used significant amounts of its energy reserves. These reserves have been depleted and now need to be replenished. We apologise for the inconvenience caused.',
                           'synonyms': {'2nd stage', 'Stages', 'stage' 'stage 2'}
                          },

                          {'tag': 'Suspension',
                           'responses': 'Loadshedding will be suspended as generation capacity sufficiently recovers. We thank you for support and patience during the loadshedding.',
                            'synonyms': {'Suspended', 'Suspend', 'Suspending'}
                          },

                          {'tag': 'Usage',
                           'responses': 'We urge all customers to help reduce electricity usage in order to ease the pressure on the system. Thank you!',
                          'synonyms': {'Consumption', 'Reduce usage', 'usage', 'Generation usage', 'system'}
                          },


                          {'tag': 'Vandalism',
                           'responses': 'Eskom losing millions of rands to vandalism & infrastructure theft, communities are inconvenienced when their electricity supply is interrupted. It is a criminal offence to damage Eskom"s property. Report offenders to the local @SAPoliceService or Eskom on 0800 11 27 22',
                           'synonyms': {'Sabotage', 'Damage','Missing towers', 'Explosion', 'Transformer'}
                          },

                          {'tag': 'Warning',
                           'responses': 'Eskom had the lowest unplanned capacity loss in a very long time, which was a positive reflection on the performance of the system. However, we are implementing efforts to achieve operational stability and restore the security of the energy supply for the country.',
                           'synonyms': {'Warns', 'warning', 'Risk', 'Warn', 'Exposure', 'Jeopardy', 'Risks'}
                          },
                          ]  }

dict_intent['intents']

# Helper function to convert tag values/text to lower_case
def lower_tag_data(row):
  # convert tag value to a lower case
  return set([value.lower() for value in row])

#  Bring out all the labels(tags) and associated response and put them in a seperate list(containers)
labels = []
responses = []

for intent in dict_intent['intents']:
    responses.append(intent['responses'])
    
    if intent['tag'] not in labels:
        labels.append(intent['tag'])

print("List of all the Tags for the response language")
labels

"""## Basic Preprocessing and Analysis of Tag Intent and Tag"""

# Build a list of keywords and similar keywords from WORDNET
# Get the list of possible keyword from user based on the different patterns in the data
list_words = labels
list_syn={}

for word in list_words:
    synonyms=[]
    synonyms.append(word.lower())
    for syn in wordnet.synsets(word):     # find the synonyms of the desired word in wordnet library
        for lem in syn.lemmas():
            # Remove any special characters from synonym strings
            lem_name = re.sub('[^a-zA-Z0-9 \n\.]', ' ', lem.name())
            synonyms.append(lem_name)

    list_syn[word]=set(synonyms)

print(list_syn)

# Add the customised(personalised) synonmyns to the  wordnet synonymns
new_list_syn = {}
for syn_tag in list_syn:    # loop through the tag synonyms 
  for tag_value in  dict_intent['intents']:  # loop through the tags and synonymns added
    if tag_value['tag'] == syn_tag: #   
      # clean the synonyms data
      human_created_tag = {tag_synonyms.lstrip().rstrip().lower() for tag_synonyms in tag_value['synonyms']} 
      new_list_syn[syn_tag] = human_created_tag.union(list_syn[syn_tag])

# Generate possible text from this keywords.
# Building dictionary of Intents & Keywords
keywords={}
keywords_dict={}

for key_word in list_words:
  keywords[key_word]=[]
  
  for synonym in list(new_list_syn[key_word]):
    keywords[key_word].append('.*\\b'+synonym+'\\b.*')

for intent, keys in keywords.items():
    # Joining the values in the keywords dictionary with the OR (|) operator updating them in keywords_dict dictionary
    keywords_dict[intent]=re.compile('|'.join(keys))

print (keywords_dict)

# Build a dictionary of response from the dictionary of intent and tags so that once the label is called the response can be returned
response_dict = {}
for value in dict_intent['intents']:
  response_dict[value['tag']] = value['responses']
  print(value)

# Add unclassified in response dictionary
response_dict['Unrelated messages'] = 'Unrecognized Message'

"""## Testing the algorithm on the machine"""

# Test to see how the response work on the current device or machine
print("Welcome to the Comment-Synthesizer")
print("", end="")

# While loop to run the chatbot indefinetely

while (True):  

    # Takes the user input and converts all characters to lowercase
    print('User Tweet: ', end="")
    user_input = input().lower()

    # Defining the Chatbot's exit condition

    if user_input == 'quit': 

        print ("Thank you for visiting.")

        break    

    matched_intent = None 

    for intent,pattern in keywords_dict.items():


        # Using the regular expression search function to look for keywords in user input

        if re.search(pattern, user_input): 


            # if a keyword matches, select the corresponding intent from the keywords_dict dictionary

            matched_intent=intent  

    # The fallback intent is selected by default
    key='Unrelated messages' 

    if matched_intent in response_dict:


        # If a keyword matches, the fallback intent is replaced by the matched intent as the key for the responses dictionary
        key = matched_intent 


    # The chatbot prints the response that matches the selected intent
    print('Comment-Synthesizer: ', end="")
    print(response_dict[key]) 
    print('=============================')

try:
    from google.colab import drive
except ImportError:
    drive = None


def translate_chat(user_input):
    """
    function that allows bulk testing of the algorithm on multiple sentence/ message

    where user_input: is message, tweet text from a user
    """
    if user_input is None:
        return response_dict["Unrelated messages"]

    user_input = str(user_input).lower()
    matched_intent = None

    for intent, pattern in keywords_dict.items():
        if re.search(pattern, user_input):
            matched_intent = intent

    key = "Unrelated messages"
    if matched_intent in response_dict:
        key = matched_intent

    return response_dict[key]


if __name__ == "__main__":
    if drive is not None:
        drive.mount('/content/drive')

    print("Welcome to the Comment-Synthesizer")
    print("", end="")

    while True:
        print('User Tweet: ', end="")
        user_input = input().lower()

        if user_input == 'quit':
            print("Thank you for visiting.")
            break

        matched_intent = None
        for intent, pattern in keywords_dict.items():
            if re.search(pattern, user_input):
                matched_intent = intent

        key = 'Unrelated messages'
        if matched_intent in response_dict:
            key = matched_intent

        print('Comment-Synthesizer: ', end="")
        print(response_dict[key])
        print('=============================')

    # Optional dataset processing only when running this script directly.
    if 'test' in globals():
        test['Predicted List'] = test['Tweet Text'].apply(translate_chat)
        test[['Predicted Tags', 'Machine Response']] = test['Predicted List'].apply(pd.Series)
        test[['Tweet Text', 'Tags', 'Predicted Tags', 'Machine Response']].to_csv('Predicted_Data.csv', index=False)
        print(test)

