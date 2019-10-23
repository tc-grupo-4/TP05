# coding=utf-8

from math import pi

f0 = 45982
fz = 50173

w0 = f0 * 2 * pi
wz = fz * 2 * pi
c = 5*(10**(-9))
q = 8.52

r = 1 / (w0*c)


r6 = r

r1 = q * r
r7 = 1 / (r * (wz * c)**2 )
r8 = r7
r4 = r6 * r1 / r8
r3 = r
r2 = r3
r5 = r6


print("R = R2 = R3 = R5 = R6 = ", r)
print("R1 = ", r1)
print("R4 = ", r4)
print("R7 = R8 = ", r7)