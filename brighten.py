from PIL import Image

def brighten(file):
	img=Image.open(open(file))
	img.resize((800,800),Image.ANTIALIAS)
	for i,px in enumerate(img.getdata()):
		x=i%img.size[0]
                y=i/img.size[0]
                red=int(px[0]*3)
		green=int(px[1]*3)
		blue=int(px[2]*3)
		#print red,green,blue
                img.putpixel((x,y),(red,green,blue))
	img.save("finalmath.jpg")
