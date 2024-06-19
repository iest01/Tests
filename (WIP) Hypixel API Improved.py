import requests as req

def enterDetails():
  global key, uuid # set as global variable so that it can be used in other functions 
  key = input("Enter your API key: ") # input function allows the user to enter their API key
  uuid = input("Enter your UUID (visit here if you don't know: https://mcuuid.net/ ): ")
  print("\nLoading the menu!")
  

def fetchData():
  global key, uuid
  header = {"key":{key}, "uuid":{uuid}} # creating a header to shorten the url and improve code reusability 
  response = req.get("https://api.hypixel.net/skyblock/profiles?", params=header) # request data from the specific endpoint and apply the header
    
  print(f"Request URL: {response.url}")  # Requests the full url and prints it for debugging purposes
  print(f"Response Status Code: {response.status_code}")  # Grabs the response status code and prints it (Status Code: 200 means everything is working!)
  data = response.json() # initialising a variable of the json response
  return data

def purseValue():
  data = fetchData() # initialise the data variable as the json response
  profile = data["profiles"][0] # view the first profile in the response (there's only one profile but we have to declare this anyway)
  purse = profile["members"][uuid]["coin_purse"] # iterate through the branches to the category we want
  print(purse)
    
def skillLevels():
  data = fetchData()
  profile = ["profiles"][0]
  skills = profile["members"][uuid] # rest of the route is a bit funky so will have to fix this and other options later
  print(skills)

def main(): # menu function
  open=True
  while open:
    print ("""
    1. Enter Key and UUID (Please select this option first if you haven't entered your details)
    2. View Purse Value
    3. View Skill Levels
    4. Exit
    """)
    choice = input("Please enter the corresponding number: ") 
    if choice=="1": 
      enterDetails()
    elif choice=="2":
      print("\n Here is your purse value. Remember to deposit at the bank so you don't lose it!") 
      purseValue()
    elif choice=="3":
      print("\n Here are your skill levels!") 
      skillLevels()
    elif choice=="4":
      print("\n See you later!") 
      open = False
    else:
      print("\n Please enter a valid option from the list above!") 
      
if __name__ == "__main__": # this idiom is to ensure the menu function is executed first when the program is ran directly
    main()
  