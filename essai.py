import json
from lib.se_utils import se_utils

class dom (se_utils):

    def __init__(self):
        super().__init__()
        self.elements = {'' : [{'name':'xpath'}]}
        f =  open('objects.json', 'r')
        self.elements.clear()
        dom = json.load(f)
        for page in dom['pages']:
            self.elements.update({page['name']: {'name':'xpath'}})
            self.elements[page['name']].clear()
            for obj in page['objects']:
                self.elements[page['name']].update({obj['name']:obj['xpath']})

app = dom()
print (app.elements['Login']['UserName'])
# print(app.elements)
pass