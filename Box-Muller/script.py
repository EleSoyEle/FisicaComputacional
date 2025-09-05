import random
import math

import numpy as np
import matplotlib.pyplot as plt

def MakeRandomNormalNumbers(mean,points):
    z_0 = []
    z_1 = []
    for i in range(points):
        u1 = random.uniform(0,1)
        u2 = random.uniform(0,1)
        R = math.sqrt(-2*math.log(u1))
        z_0.append(R*math.cos(2*math.pi*u2)+mean)
        z_1.append(R*math.sin(2*math.pi*u2)+mean)
    return z_0,z_1


print(MakeRandomNormalNumbers(0,100))