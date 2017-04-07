from lxml import html
import requests

page = requests.get('https://mico.myiclubonline.com/iclub/classlist.htm?clubNumber=7856')
tree = html.fromstring(page.content)

schedule = tree.xpath('//table[]/text()')

print schedule