class matriz:
    def __init__(self,user=True,matriz=[]):
        if user:
            self.mFilas=int(input("Digite el numero de filas\n"))
            self.nColumnas=int(input("Digite el numero de columnas\n"))
            error=True
            while(error):
                self.Ma=[]
                error=False
                for m in range(self.mFilas):
                    print("Digite la %d fila con numeros separados por espacio\n"%(m+1))
                    fila=list(map(float,input().split()))
                    if len(fila)!=self.nColumnas:
                        print("Digite una matriz valida")
                        error=True
                        break
                    self.Ma.append(fila)
            print("La matriz recibida fue: ",self.Ma)
        else:
            self.mFilas=len(matriz)
            self.nColumnas=len(matriz[0])
            self.Ma=matriz
    def __repr__(self):
        return str(self.Ma)
    def Col(self,n):
        arreglo=[]
        for i in range(len(self.Ma)):
            arreglo.append(self.Ma[i][n]);
        return arreglo
    @staticmethod
    def MulV(v1,v2):
        suma=0
        for x in range(len(v1)):
            suma+=(v1[x]*v2[x])
        return suma
    @staticmethod
    def aIde(i,j,valor):
        if i==j:return valor
        return 0
    @classmethod
    def generarEs(cls,m,valor):
        return cls(False,[[matriz.aIde(i,j,valor) for j in range(m)]for i in range(m)])
    def __add__(self,m2):
        if self.mFilas==m2.mFilas and self.nColumnas==m2.nColumnas:
            nuevaMa=[]
            for f in range(self.mFilas):
                nuF=[]
                for c in range(self.nColumnas):
                    nuF.append(self.Ma[f][c]+m2.Ma[f][c])
                nuevaMa.append(nuF)
            return matriz(False,nuevaMa)
        else:
            return "Imposible hacer la operacion"
    def __sub__(self,m2):
        if self.mFilas==m2.mFilas and self.nColumnas==m2.nColumnas:
            nuevaMa=[]
            for f in range(self.mFilas):
                nuF=[]
                for c in range(self.nColumnas):
                    nuF.append(self.Ma[f][c]-m2.Ma[f][c])
                nuevaMa.append(nuF)
            return matriz(False,nuevaMa)
        else:
            return "Imposible hacer la operacion"
    def __mul__(self,m3):
        m2=None
        if type(m3)==int or type(m3)==float:
            return matriz(False,[[self.Ma[i][j]*m3 for j in range(self.nColumnas)]for i in range(self.mFilas)])
        else: m2=m3
        if self.mFilas==m2.nColumnas:
            nuevaMa=[]
            for f in range(self.mFilas):
                fila=[]
                for c in range(m2.nColumnas):
                    fila.append(matriz.MulV(self.Ma[f],m2.Col(c)))
                nuevaMa.append(fila)
            return matriz(False,nuevaMa)
        else:
            return "Imposible hacer la operacion"
    def __pow__(self,potencia,mod=2):
        if self.mFilas==self.nColumnas:
            if potencia==0: return matriz.generarEs(self.mFilas,1)
            aux=self
            for i in range(potencia-1):
                aux=aux*self
            return aux
        else: return "Imposible hacer la operacion"
    def __eq__(self,m2):
        return True if self.Ma==m2.Ma else False
    def ObtMenor(self,f,c):
        return matriz(False,[[self.Ma[i][j] for j in range(self.nColumnas) if j!=c-1]for i in range(self.mFilas) if i!=f-1])
    def Cof(self,nFC,n,por="F"):
        return (-1)**(nFC+n)*(self.ObtMenor(nFC,n).Det())
    def Det(self,por="F",n=1):
        if n>self.mFilas:n=1
        if not self.esCuadrada():return "Imposible hacer la operacion"
        if self.mFilas==1:return self.Ma[0][0]
        if self.mFilas==2:return self.Ma[0][0]*self.Ma[1][1]-self.Ma[0][1]*self.Ma[1][0]
        suma=0
        if por=="F":
            for fila in range(len(self.Ma)):
                suma+=self.Ma[fila][n-1]*self.Cof(fila+1,n)
            return suma
    def MCof(self):
        if not self.esCuadrada():return "Imposible hacer la operacion"
        matNue=[]
        for fila in range(len(self.Ma)):
            filNue=[]
            for columna in range(len(self.Ma)):
                print(fila,columna)
                filNue.append(self.Cof(fila+1,columna+1))
            matNue.append(filNue)
        return matriz(False,matNue)
    def Adj(self):
        return self.MCof().trans()
    def trans(self):
        return matriz(False,[[self.Ma[i][j] for i in range(self.mFilas)]for j in range(self.nColumnas)])
    def esCuadrada(self):
        return True if self.mFilas==self.nColumnas else False
    def esNula(self):
        return True if len(list(filter(lambda fila: len(list(filter(lambda dato: dato==0,fila)))==len(fila),self.Ma)))==len(self.Ma) else False
    def esTriangularS(self):
        return True if self.esCuadrada() and len([[0 for j in range(self.nColumnas) if i>j and self.Ma[i][j]==0] for i in range(self.mFilas)])==(self.mFilas**2-self.mFilas)//2 else False
    def esTriangularI(self):
        return True if self.esCuadrada() and len([[0 for j in range(self.nColumnas) if i<j and self.Ma[i][j]==0] for i in range(self.mFilas)])==(self.mFilas**2-self.mFilas)//2 else False
    def esSimetrica(self):
        return True if self.esCuadrada() and self.Ma==self.trans().Ma else False
    def esAntisimetrica(self):
        return True if self.esCuadrada() and self.Ma==((self.trans())*(-1)).Ma else False
    def esIdempotente(self):
        return True if self.esCuadrada() and self.Ma==(self**2).Ma else False
    def sonInversas(self,matriz2):
        return True if self.esCuadrada() and self.mFilas==matriz2.mFilas and self.nColumnas==matriz2.nColumnas and (self*matriz2).Ma==matriz.generarEs(self.nColumnas,1) else False
    def esNilpotente(self,intentos=10):
        if not self.esCuadrada():return False
        aux=self
        for i in range(intentos):
            if (self**(i+1)).esNula():return True
        return False
    def esInvolutiva(self,intentos=10):
        if not self.esCuadrada():return False
        iden=matriz.generarEs(self.nColumnas,1)
        aux=self
        for i in range(intentos):
            if (self**(i+1)).Ma==iden.Ma:return True
        return False
    def Inversa(self):
        if self.Det()==0:return "Imposible realizar la operacion"
        return self.Adj()*(1/self.Det())
            
    def __repr__(self):
        cadenaF="Matriz %dx%d\n"%(self.mFilas,self.nColumnas)
        for i in self.Ma:
            cadenaSe=" ".join(list(map(str,i)))
            cadenaSe+="\n"
            cadenaF+=cadenaSe
        return cadenaF
    def reemplazar_columna(self,n,vector):
        f=matriz(False,[[self.Ma[i][j] if j!=n else vector[i] for j in range(self.nColumnas)]for i in range(self.mFilas)])
        print(f)
        return f
    def solucionar(self,vector):
        if not self.esCuadrada() or self.Det()==0: return "Imposible realizar la operacion"
        arreglo_solucion=[]
        det=self.Det()
        for n in range(self.nColumnas):
            arreglo_solucion.append(self.reemplazar_columna(n,vector).Det()/det)
        return arreglo_solucion
        
def operar(m1,m2,operacion):
    if operacion==1: return m1*m2
    if operacion==2: return m1+m2
    if operacion==3: return m1-m2
    if operacion==4: return m1**m2
    if operacion==5: return m1*m2
    if operacion==6: return m1*m2
    if operacion==7: return m1*m2
    if operacion==8: return m1*m2
def menu():
    opcion=0
    matrices=[]
    while(opcion!=4):
        print("Elija una de las siguientes:\n1.Crear Matriz\n2. Usar Matriz\n3.Eliminar matriz\n4.Cerrar\nOpcion: ")
        opcion=int(input())
        if(opcion==1):
            NuevaMatriz=matriz()
            print("Exitosamente agregada")
            matrices.append(NuevaMatriz)
        elif(opcion==2):
            if len(matrices)==0:
                print("No hay matrices creadas")
                continue
            for x in range(len(matrices)):
                print("%d."%(x+1))
                print(matrices[x])
                print()
            print("Digite una opcion:")
            opcion2=int(input())
            if opcion2<=0 or opcion2>len(matrices):
                print("Opcion invalida")
                continue
            matrizoperar=matrices[opcion2-1]
            print("Digite una opcion")
            print("1.Multiplicar\n2.Sumar\n3.Restar\n4.Elevar\n5.Verificar")
            opcion3=int(input())
            if opcion3>=1 or opcion3<=4:
                for x in range(len(matrices)):
                    print("%d."%(x+1))
                    print(matrices[x])
                    print()
                print("Digite una opcion:")
                opcion4=int(input())
                if opcion4<=0 or opcion4>len(matrices):
                    print("Opcion invalida")
                    continue
                matrizresul=operar(matrizoperar,matrices[opcion4-1],opcion3)
                print(matrizresul)
                print("Desea guardar esta matriz? (S/N)")
                car=input()
                if car=="S":matrices.append(matrizresul)
            else:
                print("Digite una opcion valida")
                continue
        else: continue
if __name__=="__main__":
    menu()
          
