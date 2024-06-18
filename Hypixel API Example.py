import requests as req # import the requests HTTP library to use get

key = "add-your-key-here", # paste your hypixel API key here
uuid = "add-your-minecraft-uuid-here" # paste your minecraft uuid (find it here: https://mcuuid.net/)
header = {"key":{key}, "uuid":{uuid}} # creating a header to shorten the url and improve code reusability (it applies this header at the end of the requested API url)

response = req.get("https://api.hypixel.net/skyblock/profiles?", params=header) # sending get request to the specified API url, in this case the skyblock player profile
data = response.json() # initialising data variable which is just the response of the API in json

purse = data["profiles"][0]["members"]["330ed8459b9a425f89cb2f8217437df4"]["coin_purse"] # example of initialising a variable for specific values (in this csae our purse value).
# it must iterate through each field in the json array to return the desired category (coin purse)
print ("Purse Balance: ")
print(purse)


def openMenu():
    ans=True
while ans:
    print ("""
    1. View Purse Value
    2. View Skill Levels
    3. Exit
    """)
    ans=input("What would you like to do? ") 
    if ans=="1": 
      print("\n Here is your purse value. Remember to deposit at the bank so you don't lose it!") 
    elif ans=="2":
      print("\n Here are your skill levels!") 
    elif ans=="3":
      print("\n See you later!") 
    elif ans !="":
      print("\n Not Valid Choice Try again") 




def enterDetails():
    print("Enter your API key")
    key = input()
    print("Enter your UUID (visit here if you don't know: https://mcuuid.net/ )")
    uuid = input()

    header = {"key":{key}, "uuid":{uuid}}
    response = req.get("https://api.hypixel.net/skyblock/profiles?", params=header)
    data = response.json()
    print("Loading your data")

    print("\n ====MENU====")
    openMenu()


    def purseValue():
        purse = data["profiles"][0]["members"][{uuid}]["coin_purse"] # might have to use the trimmed uuid remember to test if this is the case
        print(purse)


    