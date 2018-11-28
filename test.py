from requests import get

content = get("http://www.wordreference.com/definicion/casa").text
print(content)