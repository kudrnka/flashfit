# -*- coding: utf-8 -*- (Python reads this)
import numpy
from numpy import matrix, matlib, linalg
import math

class ModelABC:
    name = u"A→B→C"

    def getInitialParameters(self, time):
        return [10 / (time[len(time) / 2] - time[0]), 3 / (time[len(time) / 2] - time[0])]

    def rcalc(self, k, a_0, t, y):
        """
        Parameter k (=parameter) is a column vector.
        Parameter a_0 is a number.
        Parameter t is a list of time values.
        Parameter y is a column vector of measured values.
        Returns tuple of three values:
        - first value is a list of residuals 'r'
        - second value is a matrix of concentrations 'c'
        - third value is a matrix 'a'
        """
        # First column of C contains concentrations of A
        c0 = a_0 * matlib.exp(-k[0,0] * t)
        # Second column of C contains concetrations of B
        c1 = a_0 * (k[0,0] / (k[1,0] - k[0,0])) * (matlib.exp(-k[0,0] * t) - matlib.exp(-k[1,0] * t))
        # Third column of C contains concentrations of C
        c2 = a_0 - c0 - c1
        c = matlib.hstack((c0, c1, c2))
    
        # elimination of linear parameters
        # [0] because we just need the result, not the residuals etc.
        a = linalg.lstsq(c, y)[0]

        # calculate residuals
        # ca = c * a (matrix multiplication)
        r = y - matlib.dot(c, a)    
        return (r, c, a)
    
class ModelFirst:
    name = u"Single First Order"

    def getInitialParameters(self, time):
        return [10 / (time[len(time) / 2] - time[0])]

    def rcalc(self, k, a_0, t, y):
        # First column of C contains concentrations of A
        c = a_0 * matlib.exp(-k[0,0] * t)
   
        # elimination of linear parameters
        # [0] because we just need the result, not the residuals etc.
        a = linalg.lstsq(c, y)[0]

        # calculate residuals
        r = y - matlib.dot(c, a)        
        return (r, c, a)

class ModelFirst2:
    name = u"Dual First Order"

    def getInitialParameters(self, time):
        return [10 / (time[len(time) / 2] - time[0]), 3 / (time[len(time) / 2] - time[0])]

    def rcalc(self, k, a_0, t, y):
        c0 = a_0 * matlib.exp(-k[0,0] * t)
        c1 = a_0 * matlib.exp(-k[1,0] * t)
        c = matlib.hstack((c0, c1))
    
        # elimination of linear parameters
        # [0] because we just need the result, not the residuals etc.
        a = linalg.lstsq(c, y)[0]

        # calculate residuals
        r = y - matlib.dot(c, a)    
        return (r, c, a)

def ngml(model, p, a_0, t, y, logger = None):
    """
    Newton-Gauss-Levenberg/Marquardt algorithm
    Parameter p is a list of initial parameters.
    a_0 is a number (usually 1e-3)
    Parameter t contains a list of time values.
    Parameter y is a list of measured values.

    Also check leastsq in SciPy, as it might be useful:
     http://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.leastsq.html
    Wikipedia:
     http://en.wikipedia.org/wiki/Levenberg%E2%80%93Marquardt_algorithm
     http://en.wikipedia.org/wiki/Non-linear_least_squares
    """
    # make column vector from y
    y = matrix(y).transpose()
    # make column vector from p
    p = matrix(p).transpose()
    # make column vector from t
    t = matrix(t).transpose()

    ssq_old = 1e50
    # Marquardt parameter
    mp = 0
    # convergence limit
    mu = 1e-4
    # step size for numerical diff
    delta = 1e-6

    it = 0 # iteration
    j = matlib.empty([len(t), len(p)]) # Jacobian
    while it < 50:
        # call calc of residuals
        (r0, c, a) = model.rcalc(p, a_0, t, y)
        ssq = matlib.sum(matlib.multiply(r0, r0))
        conv_crit = (ssq_old - ssq) / ssq_old
        if logger:
            logger("Fitting absorbance: it=%i, ssq=%g, mp=%g, conv_crit=%g" % (it, ssq, mp, conv_crit))
        if abs(conv_crit) <= mu: # ssq_old=ssq, minimum reached !
            if mp == 0:
                break # if Marquardt par zero, stop
            else:
                mp = 0 # set to 0 , another iteration
                r0_old = r0
        elif conv_crit > mu: # convergence !
            mp = mp / 3.0
            ssq_old = ssq  
            r0_old = r0
            for i in range(0, len(p)):					
                p[i] = (1 + delta) * p[i]						
                r = model.rcalc(p, a_0, t, y)[0];
                j[:,i] = ((r - r0) / (delta * p[i]))[:,0]
                p[i] = p[i] / (1 + delta)						
        elif conv_crit < -mu: # divergence !
            if mp == 0:											
                mp = 1 # use Marquardt parameter
            else:
                mp = mp * 5										 
            p = p - delta_p # and take shifts back

        # augment Jacobian matrix
        j_mp = matlib.vstack((j, mp * matlib.eye(len(p))))
        # augment residual vector
        r0_mp = matlib.vstack((r0_old, matlib.zeros(p.shape)))
        # calculate parameter shifts
        delta_p = linalg.lstsq(-j_mp, r0_mp)[0]
        # add parameter shifts
        p = p + delta_p 
        it += 1
       
    # Curvature matrix
    curv = matlib.dot(j.H, j)

    # Should 'r' be returned, or maybe 'r0' should be? 
    return (p, ssq, c, a, curv, r0)

