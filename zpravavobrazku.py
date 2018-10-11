from PIL import Image

adresa = "c:\WRK\obrazek.jpg"
obrazek = Image.open(adresa)
mapa = obrazek.load()

for i in range(0,obrazek.width):
    for j in range(0,obrazek.height):
        rgb=mapa[i,j]
        nrgb=(rgb[0]&254,rgb[1]&254,rgb[2]&254)
        mapa[i,j]=nrgb

zprava = "zprava"
binar = ""

for i in range(0,len(zprava)):
    temp=str(bin(ord(zprava[i]) ) )
    temp=temp[2:]
    for j in range(len(temp),8):
        temp= "0"+temp
    binar+=temp
    

pocitadlo = 0
x = 0

for i in range(0,obrazek.width):
    if pocitadlo==(len(binar)):
        if x>0:
            i-=1
        rgb=mapa[i,x]
        nrgb=(rgb[0]+1,rgb[1]+1,rgb[2]+1) #liché číslo u všech barev = konec zprávy
        mapa[i,x]=nrgb
        break
    for j in range(0,obrazek.height):
        if binar[pocitadlo]=="1":
            rgb=mapa[i,j]
            nrgb=(rgb[0]+1,rgb[1],rgb[2])
            mapa[i,j]=nrgb
        pocitadlo+=1
        if pocitadlo==(len(binar)):
            if j+1<obrazek.height:
                x=j+1
            break


        
obrazek.save("c:/WRK/novyobrazek.bmp",)
obrazek.close()