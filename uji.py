import os
count=0
for x in os.listdir('project/ujicoba/data-raw/'):
    print(x)
    if os.path.isfile(os.path.join('project/ujicoba/data-raw/',x)):
        count +=1

print("File Count",count)