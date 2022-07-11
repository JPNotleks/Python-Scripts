import numpy as np
from ImpMidPoint import ImpMidPoint
import matplotlib.pyplot as plt

y0 = ####
T = ####
h = ####

[t,y] = ImpMidPoint(y0,T,h)

# Plot the solution
plt.plot(t,y[0,:],label="p")
plt.plot(t,y[1,:],label="q")
plt.xlabel("t")
plt.legend(loc="upper right")
plt.savefig("prb2sol.pdf")

# Plot the Hamilonian
plt.figure()
H = ####
plt.plot(t,H,label="H")
plt.xlabel("t")
plt.ylim(0,5)
plt.legend(loc="upper right")
plt.savefig("prb2ham.pdf")