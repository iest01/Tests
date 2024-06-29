def returnSkillXP():
  response = req.get("https://api.hypixel.net/resources/skyblock/skills")
  data = response.json
  print(data)