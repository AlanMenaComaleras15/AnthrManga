# THIS IS A TEST FILE THAT TESTS THE UPLOAD FUNCTION

import requests

url = 'http://localhost:7000/upload/2.epub'

fitxer = {'file': ('haruko.epub', open('../bibi-bookshelf/haruko.epub', 'rb'))}

response = requests.post(url, files=fitxer)

if response.status_code == 200:
    print("Fitxer enviat amb èxit!")
else:
    print("Hi ha hagut un problema en l'enviament del fitxer. Codi d'estat:", response.status_code)
