import requests as req # allows the usage of requests through the request library e.g. get
from prettytable import PrettyTable # table formatting


def enterDetails():
  global key, uuid # set as global variable so that it can be used in other functions 
  key = input("Enter your API key: ") # input function allows the user to enter their API key
  uuid = input("Enter your trimmed UUID (visit here if you don't know: https://mcuuid.net/ ): ") # trimmed uuid must be used due to formatting!
  print("\nLoading the menu!")
  

def fetchData():
  key, uuid
  header = {"key":{key}, "uuid":{uuid}} # creating a header to shorten the url and improve code reusability 
  response = req.get("https://api.hypixel.net/skyblock/profiles?", params=header) # request data from the specific endpoint and apply the header
    
  print(f"Request URL: {response.url}")  # Requests the full url and prints it for debugging purposes
  print(f"Response Status Code: {response.status_code}")  # (Status Code: 200 means everything is working!)
  data = response.json()
  return data

def purseValue():
  data = fetchData() # calls the function and declares the response as a variable
  profile = data["profiles"][0] # view the first profile (there's only one profile but we have to declare this anyway)
  purse = profile["members"][uuid]["coin_purse"] # iterate through the list to the category we want
  print(purse)


def returnSkillXP(): # returns how much exp is needed per level for each skill
  data = req.get("https://api.hypixel.net/resources/skyblock/skills").json() # no key or uuid required as this is hard coded, publically accesible data
  
  skillExp = { # dictionary to store the key (skill name) and value (level + exp required) data retrieved from the above endpoint
    "foraging": [
            {"level": level["level"], "expRequired": level["totalExpRequired"]} # uses list comprehension. For each iteration of the line below, a new dictionary is made
            # with the combined level and exp required. This is collected in to a list and assigned to the skill key
            for level in data["skills"]["FORAGING"]["levels"] # iterates over each level and evaluates the above expression
            ],
    "runecrafting": [
      {"level": level["level"], "expRequired": level["totalExpRequired"]}
            for level in data["skills"]["RUNECRAFTING"]["levels"]
            ],
    "taming": [
      {"level": level["level"], "expRequired": level["totalExpRequired"]}
            for level in data["skills"]["TAMING"]["levels"]
            ],
    "Combat": [
      {"level": level["level"], "expRequired": level["totalExpRequired"]}
            for level in data["skills"]["COMBAT"]["levels"]
    ],
    "enchanting": [
      {"level": level["level"], "expRequired": level["totalExpRequired"]}
            for level in data["skills"]["ENCHANTING"]["levels"]
    ],
    "fishing": [
      {"level": level["level"], "expRequired": level["totalExpRequired"]}
            for level in data["skills"]["FISHING"]["levels"]
            ],
    "farming": [
      {"level": level["level"], "expRequired": level["totalExpRequired"]}
            for level in data["skills"]["FARMING"]["levels"]
            ],
    "mining": [
      {"level": level["level"], "expRequired": level["totalExpRequired"]}
            for level in data["skills"]["MINING"]["levels"]
            ]
  }
  return(skillExp)
    
def skillLevels():
  data = fetchData()
  profile = data["profiles"][0]
  
  skills = { # returning each skill level individually and storing them in a "skills" dictionary, as the json response had not grouped these inside of a category. Scalable solution!
    "foraging": profile["members"][uuid]["experience_skill_foraging"], 
    "runecrafting": profile["members"][uuid]["experience_skill_runecrafting"],
    "taming": profile["members"][uuid]["experience_skill_taming"],
    "combat": profile["members"][uuid]["experience_skill_combat"],
    "enchanting": profile["members"][uuid]["experience_skill_enchanting"],
    "fishing": profile["members"][uuid]["experience_skill_fishing"],
    "farming": profile["members"][uuid]["experience_skill_farming"],
    "mining": profile["members"][uuid]["experience_skill_mining"]
  }
  
  table = PrettyTable() # creating a table for better visual clarity
  table.field_names = ["Skill", "Experience"] # naming the 2 fields (will add a 3rd field for specific levels once I figure out how to fetch and compare against another api endpoint)
    
  for skill, Exp in skills.items(): # iterate through each key-value pair within the skills dictionary. Each iteration applies a key (skill) and applies a value (xp) to this 
      table.add_row([skill, Exp]) # adds a row for each of the key-value pairs iterated in the above line
  
  print(table) # prints the table instead of the raw values
  returnSkillXP() # change this later!
  


def main(): # menu function
  open=True
  while open:
    print ("""
    1. Enter Key and UUID (Please select this option first if you haven't entered your details)
    2. View Purse Value
    3. View Skill Levels
    4. Exit
    """)
    choice = input("Please enter the corresponding number: ") # takes keyboard input e.g. 1/2/3/4
    if choice=="1": # if their choice is 1, then run the function below
      enterDetails()
    elif choice=="2": # if their choice is 2, etc, etc
      print("\n Here is your purse value. Remember to deposit at the bank so you don't lose it!") 
      purseValue()
    elif choice=="3":
      print("\n Here are your skill levels!") 
      skillLevels()
    elif choice=="4":
      print("\n See you later!") 
      open = False
    else:
      print("\n Please enter a valid option from the list above!") # data validation (prevents them entering an invalid choice and returns to the menu)
      
if __name__ == "__main__": # this idiom is to ensure the menu function is executed first when the program is ran directly
    main()
  
