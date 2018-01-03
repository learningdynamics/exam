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
        
    # it = np.nditer(Q, flags=['multi_index'])
    # while not it.finished:
    #     action = it.multi_index[0]
    #     actions = it.multi_index[1:]
            
    #     prob = np.prod([Fs[i, a]  for i,a in enumerate(actions) ])
    #     EV[action] +=  it[0] * prob
    #     it.iternext()

    return EV
 
