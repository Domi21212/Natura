import sys, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
U=os.path.join(os.path.dirname(os.path.abspath(__file__)),'fotos')+'/'
P={1:U+'1_kran.jpg',2:U+'2_man_front.jpg',3:U+'3_stirnflaechen.jpg',4:U+'4_seitenansicht.jpg',5:U+'5_heck_einfahrt.jpg'}
IM={k:Image.open(v).convert('RGB') for k,v in P.items()}
W,H,FPS,DUR=1080,1920,30,30.0
GREEN=(40,68,45); BEIGE=(240,231,211); GREEN_A=(40,68,45,232)
FB='/usr/share/fonts/opentype/inter/Inter-Bold.otf'
FS='/usr/share/fonts/opentype/inter/Inter-SemiBold.otf'
FR='/usr/share/fonts/opentype/inter/Inter-Medium.otf'
# Shots: (start,end,photo,(cx,cy,w) start,(cx,cy,w) end)
S=[(0.0,1.2,3,(600,1000,700),(620,1040,620)),
   (1.2,3.0,4,(470,800,900),(700,800,900)),
   (3.0,6.6,2,(640,600,675),(580,640,600)),
   (6.6,8.4,2,(462,560,500),(470,556,470)),
   (8.4,10.2,3,(690,660,720),(700,720,690)),
   (10.2,13.8,5,(960,600,675),(990,640,590)),
   (13.8,19.2,1,(640,800,900),(640,740,700)),
   (19.2,22.8,1,(690,730,520),(710,740,470)),
   (22.8,27.0,1,(600,930,720),(600,925,840)),
   ]
def ease(x): return x*x*(3-2*x)
def crop(im,cx,cy,w):
    h=w*16/9; iw,ih=im.size
    if h>ih: h=ih; w=h*9/16
    cx=min(max(cx,w/2),iw-w/2); cy=min(max(cy,h/2),ih-h/2)
    x0,y0=cx-w/2,cy-h/2; s=w/W
    return im.transform((W,H),Image.AFFINE,(s,0,x0,0,s,y0),resample=Image.BICUBIC)
def font(p,s): return ImageFont.truetype(p,s)
def textcard(lines,fnt,pad=(46,34),gap=14,radius=22):
    d=ImageDraw.Draw(Image.new('RGBA',(1,1)))
    bbs=[d.textbbox((0,0),l,font=fnt) for l in lines]
    lw=max(b[2]-b[0] for b in bbs); lh=fnt.size
    cw=lw+2*pad[0]; ch=len(lines)*lh+(len(lines)-1)*gap+2*pad[1]+8
    im=Image.new('RGBA',(cw,ch),(0,0,0,0)); dr=ImageDraw.Draw(im)
    dr.rounded_rectangle((0,0,cw-1,ch-1),radius,fill=GREEN_A)
    dr.rectangle((0,radius,8,ch-radius),fill=BEIGE)  # beiger Akzentbalken
    y=pad[1]
    for l,b in zip(lines,bbs):
        dr.text(((cw-(b[2]-b[0]))/2-b[0],y-b[1]+4),l,font=fnt,fill=BEIGE); y+=lh+gap
    return im
T1=textcard(['Buchenstammholz','auf dem Weg zum Kunden'],font(FB,74))
T2=textcard(['Danke für die langjährige','Zusammenarbeit.'],font(FB,66))
def overlay(fr,card,t,t0,t1,y):
    if not(t0<=t<t1): return
    a=min(1,(t-t0)/0.3,(t1-t)/0.3); a=max(0,a)
    dy=int((1-ease(min(1,(t-t0)/0.35)))*24)
    c=card.copy(); al=c.getchannel('A').point(lambda v:int(v*a)); c.putalpha(al)
    fr.paste(c,((W-c.width)//2,y+dy),c)
# Endkarte
def endcard():
    bg=crop(IM[1],600,925,840).filter(ImageFilter.GaussianBlur(22))
    ov=Image.new('RGB',(W,H),GREEN); bg=Image.blend(bg,ov,0.82)
    d=ImageDraw.Draw(bg)
    f1=font(FB,132); txt='NATURA'; sp=26
    ws=[d.textbbox((0,0),ch,font=f1)[2] for ch in txt]; tw=sum(ws)+sp*(len(txt)-1)
    x=(W-tw)/2; y=780
    for ch,w in zip(txt,ws): d.text((x,y),ch,font=f1,fill=BEIGE); x+=w+sp
    d.line((W/2-170,960,W/2+170,960),fill=BEIGE,width=3)
    f2=font(FS,50); s='WALDSERVICE GmbH'; b=d.textbbox((0,0),s,font=f2); d.text(((W-b[2])/2,995),s,font=f2,fill=BEIGE)
    f3=font(FR,40); s='natura-waldservice.de'; b=d.textbbox((0,0),s,font=f3); d.text(((W-b[2])/2,1110),s,font=f3,fill=(214,204,180))
    return bg
END=endcard()
def frame(t):
    if t>=27.0:
        fr=END.copy(); a=min(1,(t-27.0)/0.35)
        if a<1: fr=Image.blend(shot(26.99),fr,a)
        return fr
    return shot(t)
def shot(t):
    for (a,b,p,s0,s1) in S:
        if a<=t<b:
            x=ease((t-a)/(b-a)); v=[s0[i]+(s1[i]-s0[i])*x for i in range(3)]
            fr=crop(IM[p],*v)
            overlay(fr,T1,t,0.2,3.0,330)
            overlay(fr,T2,t,23.3,27.0,330)
            return fr
if __name__=='__main__':
    if sys.argv[1]=='stills':
        for tt in [0.6,2.0,5,7.5,9.3,12,16,21,25,28.5]:
            frame(tt).save(f'still_{tt:05.1f}.jpg',quality=88)
        sys.exit()
    out=sys.argv[1]
    cmd=['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
         '-i','music.wav','-c:v','libx264','-preset','slow','-crf','17','-pix_fmt','yuv420p','-profile:v','high',
         '-c:a','aac','-b:a','192k','-ar','44100','-shortest','-movflags','+faststart',out]
    pr=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for i in range(int(DUR*FPS)):
        pr.stdin.write(frame(i/FPS).tobytes())
    pr.stdin.close(); pr.wait()
