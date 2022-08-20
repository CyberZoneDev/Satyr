from source.database.methods import TokenMethods
from source.utils import Aes
from os import environ, path
import pickle

tm = TokenMethods()

if not path.exists('tmp.pickle'):
    tokens = tm.get()

    for token in tokens:
        if isinstance(token.content, str):
            token.content = Aes.encrypt(token.content, environ['S_T_K'])

    pickle.dump(tokens, open('tmp.pickle', 'wb'))
    print('Work done 1/2')
    # Alter now
    exit()

tokens = pickle.load(open('tmp.pickle', 'rb'))
for token in tokens:
    tm.add(token)

print('Work done 2/2')
