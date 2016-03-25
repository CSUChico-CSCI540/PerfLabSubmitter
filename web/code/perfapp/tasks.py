from celery import task, current_task

from time import sleep
import math
import sys,os,subprocess
from subprocess import Popen,PIPE 

from redis import Redis
red = Redis(host='redis2', port=6379)
#import sys,os,subprocess
#from subprocess import Popen,PIPE

@task
def testing(count):
    #print "hello"
    for i in range(5):
        sleep(1)
    #print "done with task"
    #red.incr('servers')
    return count
    
@task
def runLab(csrf,server,hostname):
    current_task.update_state(state='PROGRESS', meta={'current': 0, 'total': 100})
    toReturn = ""
    try:
        path = "/code/uploads/"+str(csrf).rstrip().lstrip()+"/"
        #print path
        config = open(path + "config.txt","r")
        current_task.update_state(state='PROGRESS', meta={'current': 1, 'total': 100})
        a="ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no perfuser@"+server+ " \"rm -rf perflab-setup\""
        b=Popen(a, shell=True, stdout=PIPE, stderr=PIPE)
        b.wait()
        c = b.stdout.read()
        current_task.update_state(state='PROGRESS', meta={'current': 2, 'total': 100})
        a="ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no perfuser@"+server+ " \"cp -rf perflab-files perflab-setup\""
        b=Popen(a, shell=True, stdout=PIPE, stderr=PIPE)
        b.wait()
        c = b.stdout.read()
        current_task.update_state(state='PROGRESS', meta={'current': 3, 'total': 100})
        f = open(path+"FilterMain.cpp","r")
        for line in f:
            if "unistd" in line:
                return "Illegal Library unistd"
        a="scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no "+path+"FilterMain.cpp perfuser@"+server+":~/perflab-setup/"
        b=Popen(a, shell=True, stdout=PIPE, stderr=PIPE)
        b.wait()
        c = b.stdout.read()
        current_task.update_state(state='PROGRESS', meta={'current': 4, 'total': 100})
        for line in config:
        	#print line
            line = line.split()
            if line[1]=="Y":
                f = open(path+line[0],"r")
                print line[0]
                for line2 in f:
                    if "unistd" in line2:
                        return "Illegal Library unistd"
                a="scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no "+path+str(line[0])+" perfuser@"+server+":~/perflab-setup/"
                print a
                b=Popen(a, shell=True, stdout=PIPE, stderr=PIPE)
                b.wait()
                c = b.stdout.read()
        current_task.update_state(state='PROGRESS', meta={'current': 5, 'total': 100})
        a="ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no perfuser@"+server+ " \"cd perflab-setup/ ; make filter\""
        b=Popen(a, shell=True, stdout=PIPE, stderr=PIPE)
        b.wait()
        c = b.stdout.read()
        e = b.stderr.read()
        if len(e)>0:
            if "Error" in e:
                return e
            #print e
            if not "ECDSA" in e:
                return e
        #print c
        current_task.update_state(state='PROGRESS', meta={'current': 10, 'total': 100})
        status = 10.0
        tests = 5
        increment = (100.0-status)/(4.0*float(tests))
        scores = []
        #GAUSS
        gauss = []
        count = 0    
        while count < tests:
            a="ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no perfuser@"+server+ " \"cd perflab-setup/ ; ./gauss.sh\""
            b=Popen(a, shell=True, stdout=PIPE, stderr=PIPE)
            b.wait()
            c = b.stdout.read()
            line = c.split()
            try:
                score = float(line[-1])
                if not score > 9000 and not score <=0: # Check for and ignore odd scores
                    scores = scores + [score]
                    gauss = gauss + [score]
                    status = status + increment 
                    count = count + 1   
                    current_task.update_state(state='PROGRESS', meta={'current': status, 'total': 100})         
            except:
                return "gauss " + str(sys.exc_info()) + " " + hostname
            
        #AVG
        count = 0 
        avg = []   
        while count < tests:
            a="ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no perfuser@"+server+ " \"cd perflab-setup/ ; ./avg.sh\""
            b=Popen(a, shell=True, stdout=PIPE, stderr=PIPE)
            b.wait()
            c = b.stdout.read()
            line = c.split()
            try:
                score = float(line[-1])
                if not score > 9000 and not score <=0: # Check for and ignore odd scores
                    scores = scores + [score]
                    avg = avg + [score]
                    status = status + increment 
                    count = count + 1    
                    current_task.update_state(state='PROGRESS', meta={'current': status, 'total': 100})       
            except:
                return "avg " + str(sys.exc_info())+ " " + hostname
            
        #HLINE
        count = 0 
        hline = []   
        while count < tests:
            a="ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no perfuser@"+server+ " \"cd perflab-setup/ ; ./hline.sh\""
            b=Popen(a, shell=True, stdout=PIPE, stderr=PIPE)
            b.wait()
            c = b.stdout.read()
            line = c.split()
            try:
                score = float(line[-1])
                if not score > 9000 and not score <=0: # Check for and ignore odd scores
                    scores = scores + [score]
                    hline = hline + [score]
                    status = status + increment 
                    count = count + 1
                    current_task.update_state(state='PROGRESS', meta={'current': status, 'total': 100})           
            except:
                return "hline " + str(sys.exc_info()) + " " + hostname
            
        #EMBOSS
        count = 0 
        emboss = []   
        while count < tests:
            a="ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no perfuser@"+server+ " \"cd perflab-setup/ ; ./emboss.sh\""
            b=Popen(a, shell=True, stdout=PIPE, stderr=PIPE)
            b.wait()
            c = b.stdout.read()
            e = b.stderr.read()
            line = c.split()
            #print c
            try:
                score = float(line[-1])
                if not score > 9000 and not score <=0: # Check for and ignore odd scores
                    scores = scores + [score]
                    emboss = emboss + [score]
                    status = status + increment 
                    count = count + 1       
                    current_task.update_state(state='PROGRESS', meta={'current': status, 'total': 100})    
            except:
                #print e
                return  "emboss " + str(sys.exc_info()) + " " + hostname
            
        scores.sort()
        #print scores
        
        
        
        toReturn += "gauss: "
        for g in gauss:
            toReturn += str(g) + ".. "
        toReturn += "\navg: "
        for a in avg:
            toReturn += str(a) + ".. "    
        toReturn += "\nhline: "
        for h in hline:
            toReturn += str(h) + ".. "
        toReturn += "\nemboss: "
        for e in emboss:
            toReturn += str(e) + ".. "
        toReturn += "\nScores are "
        for s in scores:
            toReturn += str(int(s)) + " "
        cpe = scores[int((len(scores)+1)/2)]
        toReturn += "\nmedian CPE is " + str(int(cpe)) + " "
        if cpe > 4000:
            score = 0
        else: 
            score = math.log(6000-cpe) * 46.93012749-305.91731341
            if score > 100:
                score = 110
        score = int(score)
        toReturn +="\nResulting score is " + str(score) + "\n"
    except:
        toReturn = "Unexpected error: " + str(sys.exc_info())
    return toReturn