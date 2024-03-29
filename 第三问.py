import math
import random

class Vertex:
    def __init__(self,key):
        self.id = key
        self.connectedTo = {}
        self.Distance=0
        self.Pred=None
        self.Color='white'
    
    def addNeighbor(self,nbr,weight=0):
        self.connectedTo[nbr] = weight
    
    def setDistance(self,distance):
        self.Distance=distance
    
    def setPred(self,vertex):
        self.Pred=vertex
    
    def setColor(self,color):
        self.Color = color

    def __str__(self):
        return str(self.id) + ' connectedTo: '+str([x.id for x in self.connectedTo])
    
    def getConnections(self):
        return self.connectedTo.keys()
    def getConnections_keys(self):
        return [x.id for x in self.connectedTo]
    
    def getId(self):
        return self.id
    
    def getWeight(self,nbr):
        return self.connectedTo[nbr]

    def getDistance(self):
        return self.Distance
    
    def getPred(self):
        return self.Pred
        
    def getColor(self):
        return self.Color
    
class Graph:
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0
        
    def addVertex(self,key):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        self.vertList[key]=newVertex
        return newVertex
    
    def addNewVertex(self,key,vertex):
        self.numVertices = self.numVertices + 1
        self.vertList[key]=vertex
        return vertex

    def getVertex(self,n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def getEdge(self,edgelist,vertexslist):
        edge_list=[]
        for i in vertexslist:
            for j in vertexslist:
                if i!=j and i<j:
                    if (i,j) in edgelist:
                        edge_list.append((i,j))
        return edge_list
        
    def __contains__(self,n):
        return n in self.vertList
    
    def addEdge(self,f,t,cost=0):#f,t为编号key
        if f not in self.vertList:
            nv = self.addVertex(f) 
        if t not in self.vertList:
            nv = self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t],cost)
        self.vertList[t].addNeighbor(self.vertList[f],cost)
        
    def getVertices(self):
        return self.vertList.keys()
    
    def __iter__(self):
        return iter(self.vertList.values())
class TFU(Vertex): #TFU元件
    def __init__(self,key,name="TFU",Fault_signal=0):
        Vertex.__init__(self,key)
        self.name=name
        self.Fault_signal=Fault_signal #故障电流信号0为无故障电流，1为存在故障电流
        self.Successor_wirelist=[]     #计算期望时候，要设计到的所有馈线，即发送故障会影响到该点的所有馈线
        self.I_S_B=0                  #要求的期望
    
    def set_Fault_signal(self,Fault_signal): #设置当前的是否流经故障电流
        self.Fault_signal=Fault_signal
        
    def set_Successor_wirelist(self,Successor_wirelist):
        self.Successor_wirelist=Successor_wirelist

    def set_I_S_B(self,wire_list):
        self.I_S_B=0
        for successor_wirelist in self.Successor_wirelist:
            self.I_S_B=wire_list[successor_wirelist-1]|self.I_S_B

    def get_Fault_signal(self): #获得当前数据
        return self.Fault_signal

    def get_Successor_wirelist(self):
        return self.Successor_wirelist
    
    def get_I_S_B(self):
        return self.I_S_B
class Queue:
    def __init__(self):
        self.items = []
        
    def isEmpty(self):
        return self.items == []
    
    def enqueue(self, item): #复杂度为O(n)
        self.items.insert(0, item)
        
    def dequeue(self):      #复杂度为O(1)
        return self.items.pop()
    
    def size(self):
        return len(self.items)
def bfs(g,start):
    start.setDistance(0)
    start.setPred(None)
    vertQueue = Queue()
    vertQueue.enqueue(start)
    while (vertQueue.size() > 0):
        currentVert = vertQueue.dequeue()
        for nbr in currentVert.getConnections():
            if (nbr.getColor() == "white"):
                nbr.setColor('gray')
                nbr.setDistance(currentVert.getDistance()+1)
                nbr.setPred(currentVert)
                vertQueue.enqueue(nbr)
            currentVert.setColor('black')
def traverse(y):
    x=y
    while (x.getPred()):
        print(x.getId())
        x=x.getPred()
    print(x.getId())
def traverselist(y):
    x=y
    lst=[]
    while (x.getPred()):
        lst.append(x.getId())
        x=x.getPred()
    lst.append(x.getId())
    return lst

def sign(r):
    if r>=0.1:
        return 1
    else:
        return -1
def sigmoid(v):
    if v>4:
        return 0.98
    elif v<-4:
        return -0.98
    else:
        return 1/(1+math.e**(-v))

class Particle:
    def __init__(self,X,V): #初始速度和初始位置，均通过随机产生
        self.X=X            #粒子的空间位置
        self.V=V            #粒子当前的速度
        self.pX=0           #粒子的最优位置
        self.k=0            #当前迭代次数
        self.t=0            #进入探索阶段后的迭代次数
        self.state=0        #粒子当前阶段 0为捕食阶段，1位探索阶段
        self.F=0            #粒子当前的适应度,评价函数评价值
        self.min_F=1000     #粒子当前的最优平均值
    
    def set_X(self,X):
        self.X=X
    
    def set_V(self,V):
        self.V=V

    def replace_X(self,NewV):
        NewX=[]
        for i in range(len(NewV)):
            v=NewV[i]
            sigmoid_v=sigmoid(v)
            if random.random()<sigmoid_v:
                x=1
            else:
                x=0
            NewX.append(x)
        self.X=NewX

    def replace_V(self,V,state,pgX,hpX=[]):
        NewV=[]
        if state==0: #为捕食状态
            for i in range(len(V)):
                v=V[i]
                px=self.pX[i]
                x=self.X[i]
                pgx=pgX[i]
                w=w_max-(w_max-w_min)*(self.k/T)
                newv=w*v+c1*random.random()*(px-x)+c2*random.random()*(pgx-x)
                # if newv>4:
                #     newv=4
                # elif newv<-4:
                #     newv=-4
                NewV.append(newv)
        elif state==1:  #为探索状态
            for i in range(len(V)):
                v=V[i]
                px=self.pX[i]
                x=self.X[i]
                pgx=pgX[i]
                hpx=hpX[i]
                c3=random.random()
                w=w_max-(w_max-w_min)*(self.t/(T-self.k+self.t))
                r=random.random()
                newv=w*sign(r)*v+c1*random.random()*(px-x)+c2*random.random()*(pgx-x)+c3*random.normalvariate(0,1)*(x-hpx)
                # if newv>4:
                #     newv=4
                # elif newv<-4:
                #     newv=-4
                NewV.append(newv)
        self.V=NewV

    def set_pX(self,X):#将当前设置为最优位置
        self.pX=X

    def replace_k(self):
        self.k=self.k+1
    
    def replace_t(self):
        self.t=self.t+1
    
    def replace_state(self,state):
        self.state=state

    def replace_F(self,g,wire_list):
        self.F=0
        w_=0.5      #权重
        for i in range(len(wire_list)):
            vertex=g.getVertex(i+1)
            vertex.set_I_S_B(self.X)
            ISB=vertex.get_I_S_B()
            self.F=self.F+abs(wire_list[i]-ISB)
            # print("wire_list[i]",wire_list[i],"ISB",ISB,"I",abs(wire_list[i]-ISB))
        self.F=self.F+w_*sum(self.X)
    def replace_min_F(self,F):
        self.min_F=F
        
    def get_X(self):
        return self.X
    
    def get_V(self):
        return self.V
    
    def get_pX(self):
        return self.pX
    
    def get_k(self):
        return self.k
    def get_t(self):
        return self.t
    
    def get_state(self):
        return self.state
    
    def get_F(self):
        return self.F
        
    def get_min_F(self):
        return self.min_F

# vertexslist=[i for i in range(1,10)]
# edgelist=[(1,2),(2,3),(3,4),(4,9),(9,5),(5,6),(6,7),(7,8)]
# wire_list=[1 for i in range(3)]+[0 for i in range(5)]   #1代表故障，0代表正常，-1代表停电
# S_list=[1,8]    #系统电源与断路器
# NA_list=[9]      #联络开关
vertexslist=[i for i in range(1,15)]
edgelist=[(1,2),(2,3),(3,13),(13,4),(4,5),(5,6),(7,8),(8,9),(9,14),(14,10),(10,11),(11,12)]
wire_list=[-1 for i in range(3)]+[0 for i in range(3)]+[-1 for i in range(3)]+[0 for i in range(3)]   #1代表故障，0代表正常，-1代表停电
# wire_list=[1 for i in range(2)]+[0 for i in range(12)]   #1代表故障，0代表正常，-1代表停电
S_list=[1,6,7,12]    #系统电源与断路器
NA_list=[13,14]      #联络开关

g_list=[]   #对总图进行分块
for S in S_list:
    qulist=[]           #某区域的元件
    for NA in NA_list:
        g=Graph()   #全部节点的拓扑结构
        for i in vertexslist:
            g.addNewVertex(i,TFU(key=i,name="TFU"))
        for edge in edgelist:#边
            g.addEdge(f=edge[0],t=edge[1],cost=None)
        bfs(g,g.getVertex(S)) #对图g中的节点进行广义搜索标记
        qulist=qulist+traverselist(g.getVertex(NA))[1:]
    qulist=list(set(qulist))
    qulist.sort()
    g_list.append(qulist)

failure_vertex=[]
failure_vertex_state=[]
for g_id in range(len(g_list)):
    g0=Graph()
    vertexslist0=g_list[g_id]
    edgelist0=g.getEdge(edgelist,vertexslist0)
    wire_list0=[wire_list[v-1] for v in vertexslist0]
    for i in vertexslist0:
        g0.addNewVertex(i,TFU(key=i,name="TFU"))
    for edge in edgelist0:#边
        g0.addEdge(f=edge[0],t=edge[1],cost=None)
    for i in vertexslist0:
        if i in S_list:
            S=i
    if -1 in wire_list0:
        failure_vertex.append(vertexslist0)
        failure_vertex_state.append([-1 for i in range(len(vertexslist0))])
    if 1 in wire_list0:
        bfs(g0,g0.getVertex(S)) #对图g中的节点进行广义搜索标记
        load_traverse_list={}
        for i in vertexslist0:
            load_traverse_list[i]=traverselist(g0.getVertex(i))
        #用于设置期望做准备,找出节点的故障导致的馈线
        for i in vertexslist0:
            tfu=g0.getVertex(i)
            Successor_wirelist=[]
            for lst in load_traverse_list.values():
                if i in lst:
                    Successor_wirelist.append(lst[0])
            tfu.set_Successor_wirelist(Successor_wirelist)
            tfu.set_I_S_B(wire_list0)
        # T=100           #总迭代次数
        Particle_swarm=[]
        T=200
        N=500           #总种群数
        D=len(vertexslist0)            #粒子解空间维度
        for i in range(N):
            X=[]
            V=[]
            for j in range(D):
                X.append(random.randint(0,1))
                V.append(random.uniform(-4,4))
            particle=Particle(X,V)
            particle.replace_F(g0,wire_list0)
            particle.replace_min_F(particle.get_min_F())
            Particle_swarm.append(particle)
        w_max=0.9
        w_min=0.4
        c1=1.494
        c2=1.794
        hpX=[]      #探索阶段的粒子的所有解中的最全局优解
        pgX=[]      #所有解空间内粒子的全局最优解
        pgV=[]
        g_min_F=10000
        h_min_F=10000
        F=[]        #记录每次迭代的最优F
        M=1         #每次前往探索的粒子数
        m_1=0         #当前探索的粒子数
        for a in range(T):      #循环迭代T次
            for particle in Particle_swarm:         #遍历所有的粒子
                nowF=0                             #粒子更新前的适应值
                if particle.get_state()==0:         #如果粒子是捕获状态
                    nowF=particle.get_F()          #记录更新前的F值
                    if g_min_F>nowF:               #如果最小的适应度小于当前,设置群体最优解
                        g_min_F=nowF
                        pgX=particle.get_X()
                        pgV=particle.get_V()
                    if particle.get_min_F()>nowF:   #设置粒子最优解
                        particle.replace_min_F(nowF)#替换个体最优时间
                        particle.set_pX(particle.X) #替换个体最优位置
                    particle.replace_V(particle.get_V(),0,pgX)#更新速度
                    particle.replace_X(particle.get_V())#更新当前位置
                    particle.replace_F(g,wire_list0)                #更新适应度F
                    particle.replace_k()
                elif particle.get_state()==1:
                    # print(a)
                    nowF=particle.get_F()          #记录更新前的F值
                    if g_min_F>nowF:               #如果最小的适应度小于当前,设置群体最优解
                        g_min_F=nowF
                        pgX=particle.get_X()
                        pgV=particle.get_V()
                    if particle.get_min_F()>nowF:   #设置粒子最优解
                        particle.replace_min_F(nowF)#替换个体最优时间
                        particle.set_pX(particle.X) #替换个体最优位置
                    if h_min_F>nowF:
                        h_min_F=nowF
                        hpX=particle.get_X()
                    particle.replace_V(particle.get_V(),1,pgX,hpX)#更新速度
                    particle.replace_X(particle.get_V())#更新当前位置
                    particle.replace_F(g,wire_list0)                #更新适应度F
                    particle.replace_k()
                    particle.replace_t()
            F.append(g_min_F)
            if (a>=3):
                f=(F[a]-F[a-1])/(F[a-1]+F[a-2]+0.000000001)
                if 0<=f and f<=1 and m_1<N-1:
                    for m in range(M):
                        if Particle_swarm[m_1].get_state()==0:
                            X=[]
                            V=[]
                            for j in range(D):
                                X.append(random.randint(0,1))
                                V.append(random.uniform(-4,4))
                            Particle_swarm[m_1].replace_state(1)        #更新状态
                            Particle_swarm[m_1].set_X(X)                #初始化X值
                            Particle_swarm[m_1].set_V(V)                #初始化V值
                            Particle_swarm[m_1].replace_F(g,wire_list)  #求出当前F值
                            Particle_swarm[m_1].replace_min_F(particle.get_min_F())#重设当前粒子的最优解
                            m_1=m_1+1
        failure_vertex.append(vertexslist0)
        failure_vertex_state.append(pgX)

failure_wire_list=[0 for i in range(len(wire_list))]
for areaid in range(len(failure_vertex)):
    area=failure_vertex[areaid]
    area_wire=failure_vertex_state[areaid]
    print(area,area_wire)
    for vid in range(len(area)):
        v=area[vid]
        v_w=area_wire[vid]
        if v_w==1:
            failure_wire_list[v-1]=1
        elif v_w==-1:
            failure_wire_list[v-1]=-1

switch=[0 for i in range(min(NA_list)-1)]+[1 for i in range(len(NA_list))]
for i in range(len(failure_wire_list)):
    if failure_wire_list[i]==1:
        key1,key2=edgelist[i]
        if key1 not in NA_list and key2 not in NA_list:
            switch[key1-1]=1
            switch[key2-1]=1
        elif key1 in NA_list:
            switch[key2-1]=1
        elif key2 in NA_list:
            switch[key1-1]=1
    elif failure_wire_list[i]==-1 and (i+1) in S_list:
        for j in [x.id for x in g.getVertex(i+1).connectedTo]:
            switch[j-1]=1
            failure_wire_list[i]=1

naswich=[]
for failure_id in [i+1 for i in range(len(failure_wire_list)) if failure_wire_list[i]==1]:
    find=0
    if find==0:
        for x in S_list:
            for j in S_list:
                if x!=j and find==0:
                    g=Graph()   #全部节点的拓扑结构
                    for i in vertexslist:
                        g.addNewVertex(i,TFU(key=i,name="TFU"))
                    for edge in edgelist:#边
                        g.addEdge(f=edge[0],t=edge[1],cost=None)
                    bfs(g,g.getVertex(x)) #对图g中的节点进行广义搜索标记
                    if failure_id in traverselist(g.getVertex(j)) and find==0:
                        for na in NA_list:
                            if na in traverselist(g.getVertex(j)):
                                naswich.append(na)
                                find=1
for i in naswich:
    switch[i-1]=0

failure_wire_id=[]
if -1 not in failure_wire_list:
    failure_wire_id=failure_wire_id+[i+1 for i in range(len(failure_wire_list)) if failure_wire_list[i]==1]
    print("故障")
    print("停电区域",failure_wire_id)
else:
    failure_wire_id=failure_wire_id+[i+1 for i in range(len(failure_wire_list)) if failure_wire_list[i]==1 or failure_wire_list[i]==-1]
    print("停电")
    print("停电区域",failure_wire_id)
print("故障区域",failure_wire_list)
print("开关变化,为1的开关将其断开,0为打开",switch)
