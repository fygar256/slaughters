#!/usr/bin/python3
import supertext as st
import random

HITMAX=1 # number of pigs to hit

counter=0
number_of_enemies=3
number_of_hits=0
wait=2
skipratio=0
enemy1=chr(0x95)+chr(0x90)+chr(0x92)
enemy2=chr(0x93)+chr(0x96)+chr(0x94)
canon1=" "+chr(0x85)+chr(0x84)+chr(0x86)+" "
canon2=" "+chr(0x91)+chr(0x91)+chr(0x91)+" "
bulletchar=chr(0x82)
canonx=18
canony=23
epos=[]
bx=0
by=0

def enemies():
    global epos
    while(len(epos)<number_of_enemies):
        epos+=[[random.randrange(0,36)+1,0]]
    for i in range(len(epos)):
        x=epos[i][0]
        y=epos[i][1]
        st.color((255,255,255))
        st.locate(x,y)
        st.putstr("   ")
        st.locate(x,y+1)
        st.putstr(enemy1)
        st.locate(x,y+2)
        st.putstr(enemy2)
        epos[i]=[x,y+1]
        
def bullet():
    global bx,by
    if bx==0:
        if st.getkey('space'):
            bx=canonx+2
            by=canony
        else:
            return
    st.color((255,255,0))
    st.locate(bx,by)
    st.putchar(' ')
    by-=1
    if by==0:
        bx=0
    st.locate(bx,by)
    st.putchar(bulletchar)

def hit():
    global epos,bx,by,number_of_hits
    if bx==0:
        return number_of_hits
    l=[]
    for e in epos:
        (x,y)=(e[0],e[1])
        if (x==bx or x+1==bx or x+2==bx) and (y+1==by or y==by):
            number_of_hits+=1
            st.locate(x,y)
            st.putstr('   ')
            st.locate(x,y+1)
            st.putstr('   ')
            bx=0
        else:
            l+=[e]
    epos=l
    return number_of_hits

def invaded():
    for e in epos:
        if e[1]==23:
            return 1
    return 0

def canon():
    global canonx
    st.locate(canonx,canony)
    st.color((0,255,255))
    st.putstr(canon1)
    st.locate(canonx,canony+1)
    st.putstr(canon2)
    if st.getkey('4'):
        canonx-=1 if canonx>0 else 0
    elif st.getkey('6'):
        canonx+=1 if canonx<35 else 0

def disp_scores():
    st.locate(0,0)
    st.color((0,255,0))
    st.putstr("THE PIGSLAUGHTER ")
    st.color((255,255,0))
    st.putstr("NUMBER OF HITS: ")
    s=str(number_of_hits)
    st.color((255,255,255))
    st.putstr(s)

def difficulty(n):
    if n<5:
        return(2.0,9,1)
    elif n<20:
        return(1.7,8,3)
    elif 20<=n<40:
        return(1.5,7,4)
    elif 40<=n<60:
        return(1.0,6,5)
    elif 60<=n<80:
        return(0.5,5,6)
    elif 80<=n<100:
        return(0.3,4,7)
    else:
        return(0.0,1,8)

def main():
    global number_of_enemies,wait,counter
    st.setscreen("PIGSLAUGHTER")
    while(1):
        (wait,skipratio,number_of_enemies)=difficulty(number_of_hits)
        canon()
        bullet()
        counter+=1
        if not counter%skipratio:
            enemies()
        h=hit()
        disp_scores()

        if h==HITMAX:
            while(not st.getkey('q')):
                st.color((0,255,0))
                st.locate(13,12)
                s="YOU HIT "+str(number_of_hits)+" PIGS"
                st.putstr(s)
                st.color((255,0,0))
                st.locate(13,13)
                st.putstr("MISSION CLEARED")
                st.refresh()
                st.color((0,255,255))
                st.locate(15,14)
                st.putstr("HIT 'q' KEY")
            return

        if invaded():
            while(not st.getkey('q')):
                st.color((0,255,0))
                st.locate(8,12)
                st.putstr("THE PIGS HAVE INVADED")
                st.color((255,0,0))
                st.locate(15,13)
                st.putstr("GAME OVER")
                st.color((0,255,255))
                st.locate(14,14)
                st.putstr("HIT 'q' KEY")
                st.refresh()
            return

        if st.getkey('q'):
            exit(1)
        st.refresh()
        st.sleep(wait)

if __name__=="__main__":
    main()
    exit(0)
