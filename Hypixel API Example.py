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




    