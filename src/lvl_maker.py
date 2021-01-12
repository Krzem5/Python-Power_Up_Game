from PIL import Image, ImageTk
from tkinter import *
import random



class Main:
    def __init__ (self):
        self.tk=Tk()
        self.tk.title('')
        self.tk['background']='white'
        self.tk.resizable(0,0)
        self.tk.minsize(width=100,height=100)
        self.tk.geometry('1910x1030+-5+-25')
        self.make()
    def make(self):
        self.all_tiles=[[{},{},{},{}],None]
        self.all_tiles[1]=ImageTk.PhotoImage(Image.open('data\\img\\tiles\\tile_marker.bmp'))
        for n in range(1,5):
            rot=['@0','@90','@180','@270']
            if n==2:rot=['@0','@90']
            for r in rot:
                self.all_tiles[0][n-1][r]=ImageTk.PhotoImage(Image.open(f'data\\img\\tiles\\tile_{n}_off_{r}.bmp'))
        self.canvas=Canvas(self.tk,bg='white',width=10,height=10,borderwidth=0,highlightbackgroun='white',highlightthickness=0,highlightcolor='white')
        self.canvas.pack(padx=0,pady=0)
        self.canvas['height']=1005
        self.canvas['width']=1905
        self.l_w,self.l_h,self.map_,self.start_pos_,self.l_m_o=int(input('Width?\t')),int(input('Height?\t')),[],[0,0],[]
        self.l_pos_c=[952.5-(self.l_w*25),502.5-(self.l_h*25)]
        for y in range(self.l_h):
            self.l_m_o.append([None]*self.l_w)
            self.map_.append([None]*self.l_w)
        for y in range(self.l_h):
            for x in range(self.l_w):
                self.l_m_o[y][x]=self.canvas.create_image(x*50+self.l_pos_c[0],y*50+self.l_pos_c[1],image=self.all_tiles[0][0]['@0'],anchor='nw')
                self.map_[y][x]=11
        self.mrk=self.canvas.create_image(self.l_pos_c[0]+16,self.l_pos_c[1]+16,image=self.all_tiles[1],anchor='nw')
        self.canvas.bind_all('<Escape>',func=self.kill)
        self.canvas.bind_all('<Button-1>',func=self.turn)
        self.canvas.bind_all('<Button-3>',func=self.replace)
        self.canvas.bind_all('<space>',func=self.get)
        self.canvas.bind_all('<s>',func=self.start_pos)
    def get(self,arg):
        self.tk.destroy()
        self.map_=[[42, 14, 42, 21, 43], [22, 13, 11, 13, 22], [22, 41, 21, 31, 34], [22, 42, 14, 13, 22], [41, 31, 21, 31, 44]]
        print(self.map_)
        self.randomise()
        print(f"{str(self.map_).replace(' ','').replace('[[','').replace(']]','').replace('],[',';')}&{str(self.start_pos_).replace(' ','').replace('[','').replace(']','')}&{self.m+5}")
    def turn(self,arg):
        x_,y_,x,y=self.l_pos_c[0],self.l_pos_c[1],-1,-1
        for xp in range(self.l_w):
            if xp<((arg.x-x_)/50)<(xp+1):
                x=xp
        for yp in range(self.l_h):
            if yp<((arg.y-y_)/50)<(yp+1):
                y=yp
        if x>-1 and y>-1:
            self.canvas.delete(self.l_m_o[y][x])
            if str(self.map_[y][x])[0] in ['1','3','4'] and str(self.map_[y][x])[1]=='4':self.map_[y][x]-=3
            elif str(self.map_[y][x])[0] in ['1','3','4'] and not str(self.map_[y][x])[1]=='4':self.map_[y][x]+=1
            elif str(self.map_[y][x])[0]=='2' and str(self.map_[y][x])[1]=='2':self.map_[y][x]-=1
            elif str(self.map_[y][x])[0]=='2' and not str(self.map_[y][x])[1]=='4':self.map_[y][x]+=1
            self.l_m_o[y][x]=self.canvas.create_image(x*50+self.l_pos_c[0],y*50+self.l_pos_c[1],image=self.all_tiles[0][int(str(self.map_[y][x])[0])-1][f'@{(int(str(self.map_[y][x])[1])-1)*90}'],anchor='nw')
            self.canvas.delete(self.mrk)
            self.mrk=self.canvas.create_image(self.start_pos_[0]*50+self.l_pos_c[0]+16,self.start_pos_[1]*50+self.l_pos_c[1]+16,image=self.all_tiles[1],anchor='nw')
    def replace(self,arg):
        x_,y_,x,y=self.l_pos_c[0],self.l_pos_c[1],-1,-1
        for xp in range(self.l_w):
            if xp<((arg.x-x_)/50)<(xp+1):
                x=xp
        for yp in range(self.l_h):
            if yp<((arg.y-y_)/50)<(yp+1):
                y=yp
        if x>-1 and y>-1:
            self.canvas.delete(self.l_m_o[y][x])
            if int(self.map_[y][x]/10)==4:self.map_[y][x]=11
            else:self.map_[y][x]=(int(self.map_[y][x]/10)+1)*10+1
            self.l_m_o[y][x]=self.canvas.create_image(x*50+self.l_pos_c[0],y*50+self.l_pos_c[1],image=self.all_tiles[0][int(str(self.map_[y][x])[0])-1][f'@{(int(str(self.map_[y][x])[1])-1)*90}'],anchor='nw')
            self.canvas.delete(self.mrk)
            self.mrk=self.canvas.create_image(self.start_pos_[0]*50+self.l_pos_c[0]+16,self.start_pos_[1]*50+self.l_pos_c[1]+16,image=self.all_tiles[1],anchor='nw')
    def start_pos(self,arg):
        x_,y_,x,y=self.l_pos_c[0],self.l_pos_c[1],-1,-1
        for xp in range(self.l_w):
            if xp<((arg.x-x_)/50)<(xp+1):
                x=xp
        for yp in range(self.l_h):
            if yp<((arg.y-y_)/50)<(yp+1):
                y=yp
        if x>-1 and y>-1:
            self.start_pos_=[x,y]
            self.canvas.delete(self.mrk)
            self.mrk=self.canvas.create_image(x*50+self.l_pos_c[0]+16,y*50+self.l_pos_c[1]+16,image=self.all_tiles[1],anchor='nw')
    def randomise(self):
        self.m=0
        for y in range(len(self.map_)):
            for x in range(len(self.map_[0])):
                if int(self.map_[y][x]/10)==2:
                    d,d_=random.randint(1,2),int(str(self.map_[y][x])[1])
                    if d==d_:m=0
                    else:m=1
                    self.m+=m
                else:
                    d,d_=random.randint(1,4),int(str(self.map_[y][x])[1])
                    if d==d_-1 and d_-1>0:m=3
                    elif d==4 and d_-1==0:m=3
                    elif d==(d_+2)%4:m=2
                    elif d==d_+2 and d_==2:m=2
                    elif d==(d_+1)%4:m=1
                    elif d==d_+1 and d_==3:m=1
                    elif d==d_:m=0
                    else:print(d,d_)
                    self.m+=m
                self.map_[y][x]=int(self.map_[y][x]/10)*10+d
    def kill(self,arg):
        self.tk.destroy()
        quit()
Main()

