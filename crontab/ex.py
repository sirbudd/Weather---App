import datetime
 
with open('date.txt','a') as outFile:
    outFile.write('\n' + str(datetime.datetime.now()))