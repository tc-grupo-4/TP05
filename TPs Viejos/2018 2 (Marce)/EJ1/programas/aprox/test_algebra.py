# Testeo elemental de algebra

from sympy import *

a = symbols("a", real= True)
s = symbols("s", real= True)

h = (s - 1j * a) * (s + 1j * a)

print(expand(h))



