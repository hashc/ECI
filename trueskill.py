import math
import copy
import time
def timelogger(func):
    def inner(*args, **kwargs): #1
        start = time.perf_counter()
        res = func(*args, **kwargs) 
        print("==Time %.2f=="%(time.perf_counter()-start))
        return func(*args, **kwargs) #2
    return inner
def clean(toy_data0):
    Q = {}
    U = {}
    n = 0
    F=[]
    for (q,u) in toy_data0:
        if 'Q' in q:
            if q not in Q:
                qid = n
                Q[q] = n
                n+=1
        else:
            if q not in U:
                U[q]=n
                qid = n
                n+=1

        if 'Q' in u:
            if u not in Q:
                uid = n
                Q[u] = n
                n+=1
        else:
            if u not in U:
                U[u]=n
                uid = n
                n+=1      

        F.append([qid,uid])

    Qid2={Q[key]:key for key in Q}
    Uid2={U[key]:key for key in U}
    Search = dict(zip([k for k in Qid2]+[k for k in Uid2],[1]*len(Qid2)+[0]*len(Uid2)))
    return Search,Q,U,Qid2,Uid2,F,n
# fast version of updating function
def fastupdate(mw,sw,ml,sl,beta): # miu and sigma of winner and loser
    sw2=math.pow(sw,2)
    sl2=math.pow(sl,2)
    t = mw - ml
    c = math.sqrt(34.72222+sw2+sl2)
    c2=math.pow(c,2)
    tc = t/c
    vtc = 0.79788*0.60653**math.pow(tc,2)/math.erfc(-0.70711*tc)
    wtc = vtc*(vtc + tc)
    mw += vtc*sw2/c
    ml -= vtc*sl2/c
    sw *= math.sqrt(1 - wtc*sw2/c2)
    sl *= math.sqrt(1 - wtc*sl2/c2)
    return mw,sw,ml,sl
# update
@timelogger
def update(E0,F,beta,iter_time,record = False):
    E={}
    if record:
        E[0]=copy.deepcopy(E0)
        for i in range(1,iter_time+1):
            print("==iter %d=="%(i),end='\r')
            for winner, loser in F:
                mw,sw = E0[winner]
                ml,sl = E0[loser]
                nmw,nsw,nml,nsl = fastupdate(mw,sw,ml,sl,beta)
                E0[winner]=[nmw,nsw]
                E0[loser]=[nml,nsl]
            E[i]=copy.deepcopy(E0)
    else:
        E = copy.deepcopy(E0)
        for i in range(iter_time):
            print("==iter %d=="%(i+1),end='\r')
            for winner, loser in F:
                mw,sw = E0[winner]
                ml,sl = E0[loser]
                nmw,nsw,nml,nsl = fastupdate(mw,sw,ml,sl,beta)
                E0[winner]=[nmw,nsw]
                E0[loser]=[nml,nsl]
    return E,E0
def get_QS_US(E0,Qid2,Uid2,Search):
    US0={}
    QS0={}
    for i in E0:
        mu,sigma = E0[i]
        if Search[i]:
            QS0[Qid2[i]]=mu-3*sigma+10
        else:
            US0[Uid2[i]]=mu-3*sigma+10
    return QS0,US0
@timelogger
def get_trueskill(toy_data0,iter_time=1,record = False):
    Search,Q,U,Qid2,Uid2,F,n = clean(toy_data0)
    # initialize
    E0 = {}
    mu = 25.0; sigma = 25.0/3; beta = sigma/2
    for i in range(n): 
        E0[i]=[mu,sigma]
    E,E0 = update(E0,F,beta,iter_time,record = record)
    if record:
        EE = {}
        for i in E:
            EE[i]={}
            US0,QS0 = get_QS_US(E[i],Qid2,Uid2,Search)
            EE[i] = [copy.deepcopy(US0),copy.deepcopy(QS0)]
    else:
        US0,QS0 = get_QS_US(E0,Qid2,Uid2,Search)
        EE = [copy.deepcopy(US0),copy.deepcopy(QS0)]
            
    return EE