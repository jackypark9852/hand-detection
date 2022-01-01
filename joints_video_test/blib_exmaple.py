import matplotlib.pyplot as plt
import numpy as np
plt.ion() ## Note this correction
fig=plt.figure()
plt.axis([0,1000,0,1])

i=0
x=list()
y=list()

while i <1000:
    plt.cla()
    temp_y=np.random.random();
    x.append(i);
    y.append(temp_y);
    plt.scatter(x,y);
    i+=1;
    plt.show()
    plt.pause(0.0001) #Note this correction