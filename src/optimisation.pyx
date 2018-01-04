import numpy as np
cimport numpy as np

def cython_EVs(int n_actions, np.ndarray Q, np.ndarray Fs):
    cdef np.ndarray EV = np.zeros(n_actions)
    cdef int action, i, a
    cdef tuple actions, index
    cdef double prob, x

    for index, x in np.ndenumerate(Q):
        action = index[0]
        actions = index[1:]

        prob = 1
        for i,a in enumerate(actions):
            prob *= Fs[i, a]
            
        EV[action] +=  x * prob

    return EV
 
def cython_BoltzmannAction(np.ndarray evs, double temp=1.0):
    cdef np.ndarray[double] cs
    cdef double rd
    cdef int l
    
    # Prevent overflow
    # temp = max(temp, 0.3)
    cs = np.array(evs) / temp
    cs -= np.mean(cs)
    if (cs > 650).any():
        cs -= max(cs) + 650
    cs = np.cumsum(np.exp(cs))
    cs = cs / cs[-1]
    rd = np.random.uniform()
    l = len(cs)
    return min(l - np.sum(rd <= cs), l - 1)
