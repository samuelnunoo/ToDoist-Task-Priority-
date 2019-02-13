#Import Libs
from datetime import datetime, date, timezone
import math, time
from todoist.api import TodoistAPI
from rq import Queue
from worker import conn
q=Queue(connection=conn)

#Sync
api=TodoistAPI("Token")

Labels=[]
Tasks=[]
Projects=[]
 #Create Tables
def Tables():   
   
    global Labels
    Labels=[]
   
    for i in api.state['labels']:
        string=i['name']
        Labels.append([i['name'],i['id'],int(string[len(string)-1])])   
    
    global  Tasks
    Tasks=[]
    print(len(Tasks),'before')
    for i in api.state['items']:
        if i['checked']==0:
            Tasks.append([i['id'],i['labels'],i['content'],i['priority'],i['due_date_utc'],i['project_id']])
        
    global  Projects
    Projects=[]
 
    print(len(Tasks),"Tasks")
    for i in api.state['projects']:
        value=0
        if i['name']=='Work':
            value=5
        Projects.append([i['name'],i['id'],value])


  #Funtions 
def AddL(y,data,inter,out):
    for k in data:
        if k[inter]==y and k[0][0]=="V":
            
            return(2*int(k[out]))   
        elif k[inter]==y:
            
            return(int(k[out]))
def Main_L(data):
    for i in data:
        value=0
        
        for k,v in enumerate(i[1]):
            call=AddL(int(v),Labels,1,2)
            value+=call
            
        if len(i)<7:
            i.append(value)
        else:
            i[6]=value
def Discriminate():
    for i in Tasks:
        Work=AddL('Work',Projects,0,1)
        print(Work,i[5])
        if i[5]==Work:
         i[6]=int(i[6])+5
def date():        
    for i in Tasks:
        if i[4]!=None and len(i)<8:
            time = datetime.strptime(str(i[4]), '%a %d %b %Y %H:%M:%S %z')
            i.append(time)
        elif len(i)<8:
            i.append(None)
def date_update():

    for i in Tasks:
        if i[7]!=None:
            today=datetime.now(timezone.utc)
            a=abs(today-i[7])
            b=a
            b=int(a.days)
           
           
            diff=Convert(b)

            

            if len(i)==8:
                i.append(diff)
            else:
                i[8]=diff
        if i[7]==None:
            if len(i)==8:
                
                i.append(-1*math.inf )
            else:
                
                i[8]=-1*math.inf 
def Convert(x):
    if x==0:
        return 8
    elif x==1:
        return 7
    elif x>1 and x<=7:
        return 6
    elif x>7 and x<=14:
        return 5
    elif x>14 and x<=30:
        return 4
    elif x>30 and x<=60:
        return 3
    elif x>60 and x<=182:
        return 2
    elif x>182 and x<math.inf:
        return 1
    elif x==math.inf:
        return 0      
def Sort(alist): 
    for num in range(len(alist)-1,0,-1):
        for i in range(num):
     
            points=alist[i][6]+ alist[i][8]
            points2=alist[i+1][6]+ alist[i+1][8]
          
            if points > points2:
                temp = alist[i]
                alist[i] = alist[i+1]
                alist[i+1] = temp
def Run():
    
   api.sync();Tables();Main_L(Tasks);date();date_update();Sort(Tasks);Priority2()   
def Priority2():
    
    for i,v in enumerate(Tasks):
        target=len(Tasks)
        print(target,"target")
        rank=0
        item=api.items.get_by_id(v[0])
        num=i+1

        if target<4:
            rank=4-i
        else:
            
            if num <= (target/4):
                rank=1
            elif num > (target/4) and num<= (target/2):
          
                rank=2
            elif num > (target/2) and num<= target*(3/4):
            
                rank=3  
            elif num > target*(3/4) and num<=target:
                rank=4
        print(rank,'rank')
        item.update(priority=rank)
     
    api.commit()

while True:
    Run()
    time.sleep(60)





