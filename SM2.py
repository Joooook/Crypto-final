import hashlib
import math
from gmpy2 import powmod,invert

class SM2(object):
    def __init__(self,a,b,p,G):
        self.a=a
        self.b=b
        self.p=p
        self.O=[0,0]
        self.G=G
        self.Par=256
        self.G_list=[]

    def sub_Jacobian(self,p1, p2):
        return self.add_Jacobian(p1, (p2[0], -p2[1], p2[2]))

    def add_Jacobian(self, p1, p2):  # Jacobian加重射影坐标系下的点加运算 ,返回一个三元组
        p = self.p
        a = self.a
        p3=[0,0,0]
        if p1[2] == 0:
            return p2
        elif p2[2] == 0:
            return p1
        elif p1[2] == 1 and p2[2] == 1:
            if p1[0] == p2[0] and p1[1] == p2[1]:
                xx = (p1[0] ** 2) % p
                yy = (p1[1] ** 2) % p
                yyyy = (yy ** 2) % p
                s = (2 * (((p1[0] + yy) ** 2) % p - xx - yyyy)) % p
                m = (3 * xx + a) % p
                p3[0] = (m ** 2 - 2 * s) % p
                p3[1] = (m * (s - p3[0]) - 8 * yyyy) % p
                p3[2] = (2 * p1[1]) % p
                return p3
            elif p1[0] == p2[0] and (p1[1] + p2[1]) % p == 0:
                return (1, 1, 0)
            h = (p2[0] - p1[0]) % p
            r = (2 * (p2[1] - p1[1])) % p
            hh = h ** 2 % p
            i = (4 * hh) % p
            j = (h * i) % p
            v = (p1[0] * i) % p
            p3[0] = (r ** 2 - j - 2 * v) % p
            p3[1] = (r * (v - p3[0]) - 2 * p1[1] * j) % p
            p3[2] = (2 * h) % p
            return p3
        elif p1[2] == p2[2]:
            if p1[0] == p2[0] and p1[1] == p2[1]:
                xx = (p1[0] ** 2) % p
                yy = (p1[1] ** 2) % p
                yyyy = (yy ** 2) % p
                zz = (p1[2] ** 2) % p
                s = (2 * (((p1[0] + yy) ** 2) % p - xx - yyyy)) % p
                if (a + 3) % p == 0:
                    m = (3 * (p1[0] - zz) * (p1[0] + zz)) % p
                else:
                    m = (3 * xx + a * (zz ** 2)) % p
                p3[0] = (m ** 2 - 2 * s) % p
                p3[1] = (m * (s - p3[0]) - 8 * yyyy) % p
                p3[2] = ((p1[1] + p1[2]) ** 2 - yy - zz) % p
                return p3
            elif p1[0] == p2[0] and (p1[1] + p2[1]) % p == 0:
                return (1, 1, 0)
            A = ((p2[0] - p1[0]) ** 2) % p
            D = ((p2[1] - p1[1]) ** 2) % p
            B = (p1[0] * A) % p
            C = (p2[0] * A) % p
            p3[0] = (D - B - C) % p
            p3[1] = ((p2[1] - p1[1]) * (B - p3[0]) - p1[1] * (C - B)) % p
            p3[2] = (p1[2] * (p2[0] - p1[0])) % p
            return p3
        elif p2[2] == 1:
            z1z1 = (p1[2] ** 2) % p
            u = (p2[0] * z1z1) % p
            s = (p2[1] * p1[2] * z1z1) % p
            h = (u - p1[0]) % p
            r = (2 * (s - p1[1])) % p
            if h == 0:
                return (1, 1, 0)
            hh = (h ** 2) % p
            i = (4 * hh) % p
            j = (h * i) % p
            v = (p1[0] * i) % p
            p3[0] = (r ** 2 - j - 2 * v) % p
            p3[1] = (r * (v - p3[0]) - 2 * p1[1] * j) % p
            p3[2] = ((p1[2] + h) ** 2 - z1z1 - hh) % p
            return p3
        elif p1[2] == 1:
            z2z2 = (p2[2] ** 2) % p
            u = (p1[0] * z2z2) % p
            s = (p1[1] * p2[2] * z2z2) % p
            h = (u - p2[0]) % p
            r = (2 * (s - p2[1])) % p
            if h == 0:
                return (1, 1, 0)
            hh = (h ** 2) % p
            i = (4 * hh) % p
            j = (h * i) % p
            v = (p2[0] * i) % p
            p3[0] = (r ** 2 - j - 2 * v) % p
            p3[1] = (r * (v - p3[0]) - 2 * p2[1] * j) % p
            p3[2] = ((p2[2] + h) ** 2 - z2z2 - hh) % p
            return p3
        else:
            zz1 = (p1[2] ** 2) % p
            zzz1 = (p1[2] * zz1) % p
            zz2 = (p2[2] ** 2) % p
            zzz2 = (p2[2] * zz2) % p
            l1 = (p1[0] * zz2) % p
            l2 = (p2[0] * zz1) % p
            l3 = (l1 - l2) % p
            l4 = (p1[1] * zzz2) % p
            l5 = (p2[1] * zzz1) % p
            l6 = (l4 - l5) % p
            if l3 == 0:
                return (1, 1, 0)
            l7 = (l1 + l2) % p
            l8 = (l4 + l5) % p
            p3[2] = (p1[2] * p2[2] * l3) % p
            ll3 = l3 ** 2 % p
            l9 = l7 * ll3 % p
            p3[0] = ((l6 ** 2) % p - l9) % p
            l10 = (l9 - 2 * p3[0]) % p
            p3[1] = ((l10 * l6 - l8 * ll3 % p) // 2) % p
            return p3

    def pre_process(self, w):
        p1=(self.G[0],self.G[1],1)
        self.G_list.append(p1)
        p2 = self.add_Jacobian(p1, p1)
        p2 = (p2[0] * invert(powmod(p2[2], 2, self.p), self.p)) % self.p, (p2[1] * invert(powmod(p2[2], 3, self.p), self.p)) % self.p, 1
        self.G_list.append(p2)
        for i in range(1, 1 << (w - 1)):
            pi = self.add_Jacobian(self.G_list[2 * i - 2], p2)
            pi = (pi[0] * invert(powmod(pi[2], 2, self.p), self.p)) % self.p, (pi[1] * invert(powmod(pi[2], 3, self.p), self.p)) % self.p, 1
            self.G_list.append(pi)
            self.G_list.append((1, 1, 0))

    def mul_optimizer(self, k, point, w, flag):
        p=self.p
        naf = []
        ind = k
        mod_wnd = 1 << w
        sup = (1 << (w - 1)) - 1
        length = 0
        # 求NAF
        while ind:
            if ind % 2 == 1:
                ki = ind % mod_wnd
                if ki > sup:
                    ki = ki - mod_wnd
                ind = ind - ki
            else:
                ki = 0
            naf.append(ki)
            length = length + 1
            ind = ind // 2
        # 预处理
        if flag == 0:  # 如果不是基点，则进行；否则跳过
            p_list = [(point[0],point[1], 1)]
            p2 = self.add_Jacobian(p_list[0], p_list[0])
            p2 = (p2[0] * invert(powmod(p2[2], 2, p), p)) % p, (p2[1] * invert(powmod(p2[2], 3, p), p)) % p, 1
            p_list.append(p2)
            for i in range(1, 1 << (w - 1)):
                pi = self.add_Jacobian(p_list[2 * i - 2], p2)
                pi = (pi[0] * invert(powmod(pi[2], 2, p), p)) % p, (pi[1] * invert(powmod(pi[2], 3, p), p)) % p, 1
                p_list.append(pi)
                p_list.append((1, 1, 0))
        else:  # 如果是基点，则直接取全局变量中已处理好的数据
            p_list = self.G_list
        q = (1, 1, 0)
        j = length - 1
        # 主循环
        while j >= 0:
            q = self.add_Jacobian(q, q)
            if naf[j] > 0:
                q = self.add_Jacobian(q, p_list[naf[j] - 1])
                j = j - 1
            elif naf[j] < 0:
                q = self.sub_Jacobian(q, p_list[-naf[j] - 1])#-????
                j = j - 1
            else:
                j = j - 1
        x, y, z = q
        return (x * invert(powmod(z, 2, p), p)) % p, (y * invert(powmod(z, 3, p), p)) % p


    def add(self,P,Q):
        if P==self.O:
            return Q
        if Q==self.O:
            return P
        if P[0]==Q[0] and P[1]!=Q[1]:
            return self.O
        if P!=Q:
            lam= ((Q[1]-P[1]) * int(invert(Q[0] - P[0], self.p))) % self.p
        else :
            lam= ((3*P[0]**2+self.a) * int(invert(2 * P[1], self.p))) % self.p
        x=(lam**2-P[0]-Q[0]) %self.p
        y=(lam*(P[0]-x)-P[1]) %self.p
        return [x,y]

    def sub(self,P,Q):
        return self.add(P,[Q[0],-Q[1]])

    def mul(self,k,A):
        k1=bin(k%self.p)[2:]
        count=0
        res=self.O
        while count<len(k1):
            res = self.add(res, res)
            if k1[count]=='1':
                res = self.add(res, A)
            count+=1
        return res
    def H256(self,Z):
        return self.bytes2bit(hashlib.sha256(int.to_bytes(int(Z,2),math.ceil(len(Z)/8),'big')).hexdigest())

    def KDF(self,Z,klen):
        H=[]
        ct=1
        last=math.ceil(klen/256)-1
        for i in range(math.ceil(klen/256)):
            H.append(self.H256(Z+bin(ct)[2:].rjust(32,'0')))
            ct+=1
        if klen%256!=0:
            H[last]=H[last][:klen-256*math.floor(klen/256)]
        return ''.join(H)

    def field2bytes(self,a):
        t=self.Par
        l=t//4
        return hex(a)[2:].rjust(l,'0')

    def field2bit(self,a):
        return self.bytes2bit(self.field2bytes(a))
    def point2bytes(self, C):
        X1=self.field2bytes(C[0])
        Y1=self.field2bytes(C[1])
        return '04'+X1+Y1
    def bytes2field(self,a):
        return int(a,16)

    def bytes2point(self, C):
        C=C[2:]
        X = self.bytes2field(C[:self.Par//4])
        Y = self.bytes2field(C[self.Par//4:])
        return [X,Y]
    def bit2bytes(self,bits):
        return hex(int(bits,2))[2:].rjust(math.ceil(len(bits)/4),'0')
    def bytes2bit(self,B):
        return bin(int(B,16))[2:].rjust(len(B)*4,'0')
    def point2bit(self,C):
        return self.bytes2bit(self.point2bytes(C))
    def xor(self,a,b,klen):
        return bin(int(a,2)^int(b,2))[2:].rjust(klen,'0')
    def encrypt(self,M,k,pub):
        klen=len(M)
        C1=self.point2bit(self.mul(k, self.G))
        kpub=self.mul(k,pub)
        x2,y2=self.field2bit(kpub[0]),self.field2bit(kpub[1])
        t=self.KDF(x2+y2,klen)
        C2=self.xor(M,t,klen)
        C3=hashlib.sha256(int.to_bytes(int(x2+M+y2,2),math.ceil(len(x2+M+y2)/8),'big')).hexdigest()
        return self.bit2bytes(C1)+self.bit2bytes(C2)+C3
    def decrypt(self,C,pri):
        l = self.Par//4
        C1=self.bytes2point(C[:l*2+2])
        C2=self.bytes2bit(C[l*2+2:-64])
        klen = len(C2)
        priC1=self.mul(pri,C1)
        x2, y2 = self.field2bit(priC1[0]), self.field2bit(priC1[1])
        t=self.KDF(x2+y2,klen)
        M=self.bit2bytes(self.xor(C2,t,klen))
        return M