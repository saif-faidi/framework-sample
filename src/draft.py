_dict = {'k1' : 1 , 'k2': 2}

k1,k2= _dict
print(k1)
print(k2)

def func(**kwargs):
    print(kwargs)

func(**_dict)