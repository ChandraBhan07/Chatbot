# short_= open('forms.txt', encoding= 'utf-8', mode='a')
# short_.write("model name\n\n")
# short_.write("Today\n")
# short_.write("tommorrow\n")
# short_.close()
modelpath = "data/chatbot v1.4473 2021-05-28 21_06 (32,50).h5"
from datetime import datetime 

date = str(datetime.now())[8:10] + "-" + str(datetime.now())[5:7] + "-"+ str(datetime.now())[:4]

parts = modelpath.split(' ')
filename = parts[0] +' '+ parts[1] +' '+ date

a = 'Today'
b = 'Tommorrow'

file = open(filename, encoding = 'utf-8', mode= 'a')
file.write('User: ' + a + '\n')
file.write('Comp: '+ b +'\n\n')
file.close()