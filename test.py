from requests import get
from bs4 import BeautifulSoup

# Ahora mismo funciona con 'Casa' y 'Mercado', pero no con 'perro' porque
# se puede usar como adjetivo.
content = get("http://www.wordreference.com/definicion/perro").text
soup = BeautifulSoup(content, 'html.parser')
text = soup.find(id="article").div.ol.li.get_text()
definition1 = text[3:text.find(':')] + '.'
example1 = text[text.find(':') + 1:text.find('.', 3) + 1]
second = text[text.find('.  ') + 3:]
definition2 = second[:second.find(':')] + '.'
example2 = second[second.find(':') + 1:second.find('.') + 1]
print('definition1:', definition1)
print('Example 1:', example1.capitalize())
print('definition2:', definition2)
print('Example 2:', example2.capitalize())