import numpy as np

class MapMinMaxApplier(object):
    def __init__(self,slope,intercept):
        self.slope = slope
        self.intercept = intercept

    def __call__(self, x):
        return x * self.slope + self.intercept


    def reverse(self,y):
        return (y - self.intercept) / self.slope



def mapminmax(x,ymin=-1,ymax = +1):
    x = np.asanyarray(x)
    xmax = x.max(axis = -1)
    xmin = x.min(axis = -1)

    if (xmax == xmin).any():
        raise ValueError("Some rows have no variation")

    slope = ((ymax - ymin) / (xmax - xmin))[:,np.newaxis]
    intercept = (-xmin*(ymax - ymin)/(xmax - xmin))[:,np.newaxis] + ymin

    ps = MapMinMaxApplier(slope,intercept)
    return ps(x),ps

    
