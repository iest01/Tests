import requests as req

def openMenu(): # menu function to allow the user to access the information they want
    ans=True
while ans:
    print ("""
    1. View Purse Value
    2. View Skill Levels
    3. Exit
    """)
    ans=input("Please enter the corresponding number: ") 
    if ans=="1": 
      print("\n Here is your purse value. Remember to deposit at the bank so you don't lose it!") 
    elif ans=="2":
      print("\n Here are your skill levels!") 
    elif ans=="3":
      print("\n See you later!") 
    elif ans !="":
      print("\n Please enter a valid option from the list above!") 




def enterDetails():
    print("Enter your API key")
    global key 
    key = input() # input function allows the user to enter their API key
    print("Enter your UUID (visit here if you don't know: https://mcuuid.net/ )")
    global uuid # set as global variable so that it can be used in other functions 
    uuid = input()

    header = {"key":{key}, "uuid":{uuid}}
    response = req.get("https://api.hypixel.net/skyblock/profiles?", params=header) # creating a header to shorten the url 
    # and improve code reusability (it applies this header at the end of the requested API url)
    global data 
    data = response.json() # initialising a variable of the json response
    print("Loading your data")

    print("\n ====MENU====")
    openMenu() # calling the openMenu function once the API key and UUID has been entered (none of the requests after this will work without them)


def purseValue():
        purse = data["profiles"][0]["members"][{uuid}]["coin_purse"] # might have to use the trimmed uuid remember to test if this is the case
        print(purse)
    
def skillLevels():
        skills = data["profiles"][0]["members"][{uuid}] # search up the rest of the route on the json results
