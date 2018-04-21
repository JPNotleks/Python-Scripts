import random
D=1
x=1;total=0;count=0;y=0;subTotal=0;total2=0;count2=0;subTotal2=0
for y in range(0,100000):
	for x in range(1,16):
		if random.randint(1,97-D)==1:
			subTotal=subTotal+1
		D=D+1
	if subTotal>0:
		total=total+1.0000
	count=count+1.0000
	subTotal=0
	D=1
	x=1
print total/count

x=1;y=0
for y in range(1,100000):
	for x in range(1,6):
		if random.randint(1,8)==1:
			subTotal2=subTotal2+1
	if subTotal2==4:
		total2=total2+1.0000000
	count2=count2+1.0000000
	subTotal2=0
	x=1
print total2/count2
