import numpy as np
from numpy.linalg import inv

def ImpMidPoint(y0,T,h):
    
     # Initialize variables
    N = int(np.ceil((T[1]-T[0])/h))# number of steps
    h = (T[1]-T[0])/N # adjust step size to fit interval length
    d = len(y0) # dimension of solution
    t = #### time grid
    y = np.zeros((d,N+1)) # initialise solution
    y[:,0] = #### set initial value
    
    # Define matrices needed for time stepping
    Jinv = ####
    A = ####
    
    # Compute solution
    for j in range(0,N):
        y[:,j+1] = ####
      
    return np.array([t,y])