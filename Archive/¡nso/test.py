from PIL import Image
img=Image.open('Skin/cursortrail.png').convert('RGBA')
px=img.load()

for y in range(img.size[1]):
	for x in range(img.size[0]):
		if 1:
			px[x,y]=(0,0,0,0)

img.save('Skin/empty.png','PNG')	
