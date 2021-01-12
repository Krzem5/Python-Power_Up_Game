from PIL import Image, ImageTk
from tkinter import *
import time



class Levels:
    def __init__(self):
        pass
    def get_(self):
        self.lvls={}
        with open(f'data\\levels.txt','r') as f:
            idx=0
            for l in f:
                if not l.startswith('#'):
                    map_=[]
                    l=l.replace('\n','').split('&')
                    for y in range(len(l[0].split(';'))):
                        map_.append([11]*len(l[0].split(';')[y].split(',')))
                    for y in range(len(l[0].split(';'))):
                        for x in range(len(l[0].split(';')[y].split(','))):
                            map_[y][x]=int(l[0].split(';')[y].split(',')[x])
                    self.lvls[idx]=[map_,[int(l[1].split(',')[0]),int(l[1].split(',')[1])],int(l[2])]
                    idx+=1
    def get(self,idx):
        self.get_()
        return self.lvls[idx]
    def next_lvl(self,idx):return idx+1
class Level:
    def __init__(self,tk,cnv,tiles,ar,re,slf,lvl_id=0,lvl_map=[[[13,13,13,13,13],[32,31,44,41,34],[32,21,22,21,34],[32,33,43,42,34],[22,22,22,22,22],[22,22,22,22,22],[11,11,11,11,11]],[3,3],5]):
        self.tk,self.cnv,self.l_m,self.l_m_o,self.l_s_p,self.t_l,self.p_d,self.p_f,self.m_m,self.lvl_id,self.ar,self.re,self.t_s,self.m,self.slf,self.m_m_=tk,cnv,list(lvl_map[0]),[],lvl_map[1],tiles,{11:'u',12:'r',13:'d',14:'l',21:'rl',22:'ud',31:'url',32:'urd',33:'rdl',34:'udl',41:'ur',42:'rd',43:'dl',44:'lu'},{'u':'d','r':'l','d':'u','l':'r'},{'u':(-1,0),'r':(0,1),'d':(1,0),'l':(0,-1)},lvl_id,ar,re,time.time(),0,slf,lvl_map[2]
        self.cnv.bind_all('<Button-1>',func=self.turn_tile)
        self.arr=self.cnv.create_image(10,10,image=self.ar,anchor='nw')
        self.res=self.cnv.create_image(1860,10,image=self.re,anchor='nw')
        self.prepare()
    def prepare(self):
        self.l_h,self.l_w=len(self.l_m),len(self.l_m[0])
        self.l_pos_c=[952.5-(self.l_w*25),502.5-(self.l_h*25)]
        for y in range(self.l_h):
            self.l_m_o.append([None]*self.l_w)
        for y in range(self.l_h):
            for x in range(self.l_w):
                self.l_m_o[y][x]=self.cnv.create_image(x*50+self.l_pos_c[0],y*50+self.l_pos_c[1],image=self.t_l['off'][int(str(self.l_m[y][x])[0])-1][f'@{(int(str(self.l_m[y][x])[1])-1)*90}'],anchor='nw')
        self.marker=self.cnv.create_image(self.l_s_p[0]*50+self.l_pos_c[0]+16,self.l_s_p[1]*50+self.l_pos_c[1]+16,image=self.t_l['marker'],anchor='nw')
        self.update_power()
    def turn_tile(self,arg):
        x_,y_,x,y=self.l_pos_c[0],self.l_pos_c[1],-1,-1
        for xp in range(self.l_w):
            if xp<((arg.x-x_)/50)<(xp+1):
                x=xp
        for yp in range(self.l_h):
            if yp<((arg.y-y_)/50)<(yp+1):
                y=yp
        if x>-1 and y>-1:
            self.m+=1
            self.cnv.delete(self.l_m_o[y][x])
            if str(self.l_m[y][x])[0] in ['1','3','4'] and str(self.l_m[y][x])[1]=='4':self.l_m[y][x]-=3
            elif str(self.l_m[y][x])[0] in ['1','3','4'] and not str(self.l_m[y][x])[1]=='4':self.l_m[y][x]+=1
            elif str(self.l_m[y][x])[0]=='2' and str(self.l_m[y][x])[1]=='2':self.l_m[y][x]-=1
            elif str(self.l_m[y][x])[0]=='2' and not str(self.l_m[y][x])[1]=='4':self.l_m[y][x]+=1
            self.l_m_o[y][x]=self.cnv.create_image(x*50+self.l_pos_c[0],y*50+self.l_pos_c[1],image=self.t_l['off'][int(str(self.l_m[y][x])[0])-1][f'@{(int(str(self.l_m[y][x])[1])-1)*90}'],anchor='nw')
            self.update_power()
        if 9<arg.x<31 and 9<arg.y<41:
            self.cnv.unbind_all('<Button-1>')
            Main.open_lvl_tab(Main,self.lvl_id)
        if 1859<arg.x<1901 and 9<arg.y<41:self.reset_lvl()
    def update_power(self):
        for y in range(self.l_h):
            for x in range(self.l_w):
                self.cnv.delete(self.l_m_o[y][x])
                self.l_m_o[y][x]=self.cnv.create_image(x*50+self.l_pos_c[0],y*50+self.l_pos_c[1],image=self.t_l['off'][int(str(self.l_m[y][x])[0])-1][f'@{(int(str(self.l_m[y][x])[1])-1)*90}'],anchor='nw')
        x,y=self.l_s_p[0],self.l_s_p[1]
        self.l_p_c,self.l_p_t_l=[[self.l_s_p[0],self.l_s_p[1]]],1
        d=self.p_d[self.l_m[y][x]]
        self._update_p(list(self.p_d[self.l_m[y][x]]),x,y,x,y)
        self.cnv.delete(self.marker)
        self.marker=self.cnv.create_image(self.l_s_p[0]*50+self.l_pos_c[0]+16,self.l_s_p[1]*50+self.l_pos_c[1]+16,image=self.t_l['marker'],anchor='nw')
        if self.l_p_t_l==self.l_w*self.l_h:self.end()
    def _update_p(self,d_,x,y,ox,oy):                   
        self.cnv.delete(self.l_m_o[y][x])
        self.l_m_o[y][x]=self.cnv.create_image(x*50+self.l_pos_c[0],y*50+self.l_pos_c[1],image=self.t_l['on'][int(str(self.l_m[y][x])[0])-1][f'@{(int(str(self.l_m[y][x])[1])-1)*90}'],anchor='nw')
        for d in d_:
            try:
                x_,y_=self.m_m[d][1]+x,self.m_m[d][0]+y
                if [x_,y_]!=[ox,oy] and [x_,y_] not in self.l_p_c and x_>-1 and y_>-1:
                    if self.p_f[d] in list(self.p_d[self.l_m[y_][x_]]):
                        self.l_p_c.append([x_,y_])
                        self.l_p_t_l+=1
                        if len(list(self.p_d[self.l_m[y_][x_]]))>1:
                            d__=list(self.p_d[self.l_m[y_][x_]])
                            d__.remove(self.p_f[d])
                            self._update_p(d__,x_,y_,x_,y_)
                        else:
                            self.cnv.delete(self.l_m_o[y_][x_])
                            self.l_m_o[y_][x_]=self.cnv.create_image(x_*50+self.l_pos_c[0],y_*50+self.l_pos_c[1],image=self.t_l['on'][int(str(self.l_m[y_][x_])[0])-1][f'@{(int(str(self.l_m[y_][x_])[1])-1)*90}'],anchor='nw')
            except Exception as er:
                pass
    def end(self):
        self.t_e=time.time()
        self.cnv.unbind_all('<Button-1>')
        self.cnv.delete(self.arr)
        self.cnv.delete(self.res)
        self.click_=self.cnv.create_text(15,15,text='Tap anywhere to continue...',font=('Tempus Sans ITC',20),anchor='nw')
        self.cnv.bind_all('<Button-1>',func=self.end_)
    def end_(self,arg):
        self.cnv.unbind_all('<Button-1>')
        self.cnv.delete(self.click_)
        Main.finish_lvl(self.slf,self.lvl_id,round((self.t_e-self.t_s)),self.m,self.m_m_)
    def reset_lvl(self):
        self.cnv.unbind_all('<Button-1>')
        self.cnv.delete(self.arr)
        self.cnv.delete(self.res)
        for y in range(self.l_h):
                for x in range(self.l_w):
                    self.cnv.delete(self.l_m_o[y][x])
        self.cnv.delete(self.marker)
        Level(self.tk,self.cnv,self.t_l,self.ar,self.re,self.slf,lvl_id=self.lvl_id,lvl_map=list(self.slf.level_manager.get(self.lvl_id)))
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
        self.all_tiles,self.other_img={'on':[{},{},{},{}],'off':[{},{},{},{}],'marker':None},{'arrows':{},'other':{}}
        self.all_tiles['marker']=ImageTk.PhotoImage(Image.open('data\\img\\tiles\\tile_marker.bmp'))
        for st in ['on','off']:
            for n in range(1,5):
                rot=['@0','@90','@180','@270']
                if n==2:rot=['@0','@90']
                for r in rot:
                    self.all_tiles[st][n-1][r]=ImageTk.PhotoImage(Image.open(f'data\\img\\tiles\\tile_{n}_{st}_{r}.bmp'))
        self.other_img['arrows']['left_arrow']=ImageTk.PhotoImage(Image.open('data\\img\\other\\arrow_left.bmp'))
        self.other_img['arrows']['right_arrow']=ImageTk.PhotoImage(Image.open('data\\img\\other\\arrow_right.bmp'))
        self.other_img['arrows']['reset_arrow']=ImageTk.PhotoImage(Image.open('data\\img\\other\\arrow_reset.bmp'))
        self.other_img['other']['diamond1']=ImageTk.PhotoImage(Image.open('data\\img\\other\\diamond1.bmp'))
        self.other_img['other']['diamond2']=ImageTk.PhotoImage(Image.open('data\\img\\other\\diamond2.bmp'))
        self.canvas=Canvas(self.tk,bg='white',width=10,height=10,borderwidth=0,highlightbackgroun='white',highlightthickness=0,highlightcolor='white')
        self.canvas.pack(padx=0,pady=0)
        self.canvas['height']=1005
        self.canvas['width']=1905
        self.canvas.bind_all('<Escape>',func=self.kill)#temp
        self.level_manager=Levels()
        Level(self.tk,self.canvas,self.all_tiles,self.other_img['arrows']['left_arrow'],self.other_img['arrows']['reset_arrow'],self,lvl_id=0,lvl_map=list(self.level_manager.get(0)))
    def kill(self,arg):
        self.tk.destroy()
        quit()
    def test_img(self):
        x,y=0,0
        for x in range(4):
            for y in range(len(list(self.all_tiles['on'][x].keys()))):
                self.canvas.create_image(x*51,y*51,image=self.all_tiles['off'][x][f'@{y*90}'],anchor='nw')
                self.canvas.create_image((x*51)+150,y*51,image=self.all_tiles['on'][x][f'@{y*90}'],anchor='nw')
                self.canvas.create_image((x*51)+300,y*51,image=self.all_tiles['on'][x][f'@{y*90}'],anchor='nw')
                self.canvas.create_image((x*51)+300+15,y*51+15,image=self.all_tiles['marker'],anchor='nw')
    def open_lvl_tab(self,idx_start):
        self.canvas.delete('all')
        all_=[]
    def finish_lvl_btn(self,arg):
        if 9<arg.x<31 and 9<arg.y<41:
            self.canvas.delete('all')
            self.open_lvl_tab(self.data_lvl)
        elif 199<arg.x<641 and 879<arg.y<991:
            self.canvas.delete('all')
            Level(self.tk,self.canvas,self.all_tiles,self.other_img['arrows']['left_arrow'],self.other_img['arrows']['reset_arrow'],self,lvl_id=self.data_lvl,lvl_map=list(self.level_manager.get(self.data_lvl)))
        elif 1249<arg.x<1711 and 879<arg.y<991:
            self.canvas.delete('all')
            self.data_lvl=self.level_manager.next_lvl(self.data_lvl)
            if self.data_lvl!=None:Level(self.tk,self.canvas,self.all_tiles,self.other_img['arrows']['left_arrow'],self.other_img['arrows']['reset_arrow'],self,lvl_id=self.data_lvl,lvl_map=list(self.level_manager.get(self.data_lvl)))
    def finish_lvl(self,lvl_id,t,m,m_m_):
        self.st_txt=self.canvas.create_text(950,-75,text=f'Time: {t}s    Moves: {m}',font=('Tempus Sans ITC',75),anchor='center')
        while self.canvas.coords(self.st_txt)[1]<75:
            self.canvas.move(self.st_txt,0,5)
            self.tk.update()
            self.tk.update_idletasks()
            time.sleep(0.02)
        p,l_d=self.calculate_points(t,m,m_m_),[]
        while p>0:
            if p>=1:
                p-=1
                l_d.append(2)
            else:
                p-=0.5
                l_d.append(1)
        cr=952.5-((len(l_d)-1)/2)*50
        time.sleep(0.5)
        self.diamonds=[]
        for d in l_d:
            d_=self.canvas.create_image(cr+950,225,image=self.other_img['other'][f'diamond{d}'],anchor='center')
            while self.canvas.coords(d_)[0]!=cr:
                self.canvas.move(d_,-25,0)
                self.tk.update()
                self.tk.update_idletasks()
                time.sleep(0.01)
            cr+=50
            self.diamonds.append(d_)
        self.canvas.create_image(10,10,image=self.other_img['arrows']['left_arrow'],anchor='nw')
        self.b_txt=self.canvas.create_text(950,1005,text=f'Try Agein\t\tNext Level',font=('Tempus Sans ITC',75),anchor='center')
        while self.canvas.coords(self.b_txt)[1]>925:
            self.canvas.move(self.b_txt,0,-5)
            self.tk.update()
            self.tk.update_idletasks()
            time.sleep(0.02)
        self.data_lvl=int(lvl_id)+1
        self.data_lvl-=1
        self.canvas.bind_all('<Button-1>',func=self.finish_lvl_btn)
    def calculate_points(self,t,m,m_m_):
        p=0
        if m<=m_m_:p+=2
        elif m_m_*2>m>m_m_:p+=1
        else:p+=0
        if m_m_<=10:a=1
        elif 10<m_m_<=25:a=2
        elif 25<m_m_<=40:a=3
        elif 40<m_m_<=65:a=4
        else:a=5
        if t<=15:b=1
        elif 15<t<=35:b=2
        elif 35<t<=65:b=3
        elif 65<t<=115:b=4
        else:b=5
        if (a-b+4)/2>2 and a>2:p+=(a-b+4)/2
        elif (a-b+4)/2>2 and a<=2:p+=2
        else:p+=(a-b+4)/2
        return p
Main()

