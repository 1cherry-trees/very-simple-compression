#/usr/bin/env python3

# P(x_i == 1 | x_0:i-1")

# enwik6: 1000000
# gzip  :  356268

# enwik4: 10000
# gzip  :  3728
import math
enw4 = open("x", "rb").read()#location of enwik4

def bitgen(x):
	for c in x:
		for i in range(8):
			yield int((c & (0x80>>i)) != 0)

bg = bitgen(enw4)

#stupid compresser:

from collections import defaultdict
lookup = defaultdict(lambda: [1,2])

NUMBER_OF_BITS = 16

HH = 0.0
try:
	prevx = [-1]*NUMBER_OF_BITS
	while 1:
		x = next(bg)

		#use tables
		px = tuple(prevx)

		#lookup[px] is the prediction that the next bit is 1 when using the 4 that are behind it
		p_1 =(lookup[px][0] / lookup[px][1])
		p_0 = 1.0 - p_1

		p_x = p_1 if x == 1 else 1.0 - p_1
		#H = -(p_0*math.log2(p_0) + p_1*math.log2(p_1))
		H = -(math.log2(p_x))
		HH += H

		#incrememntal table lookup
		lookup[px][0] += x == 1
		lookup[px][1] += 1
		prevx.append(x)
		prevx = prevx[-NUMBER_OF_BITS:]
except:
	pass
print("%.2f bytes of entropy" % (HH/8.0))
