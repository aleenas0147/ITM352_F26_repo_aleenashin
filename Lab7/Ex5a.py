names = ("Zendaya", "Tom Holland", "Cher", "Ariana Grande", "Dolly Parton")
ages = (30, 30, 80, 33, 80)

celeb_list = []
age_list = []
for n in names:
    celeb_list.append(n)
for a in ages:
    age_list.append(a)

data = {"celebrities": celeb_list, "ages": age_list}
print(data)



'''without loops'''
data = {"celebrities": list(names), "ages": list(ages)}
print(data)