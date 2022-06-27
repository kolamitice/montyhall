import numpy as np
import time
import matplotlib.pyplot as plt
import random as rd
from sklearn.linear_model import LinearRegression

#creating functions needed in the program
def searchindex(array,output_array):
    for h in range(len(array)):
        if array[h]==0:
            output_array.append(h)
    return output_array


def searchindex2(array,output_array):
    for h in range(len(array)):
        if array[h]==1:
            output_array.append(h)
    return output_array

def calctime(number,array_1):
    mel = number/3600
    array_1[0]=int(mel)
    if array_1[0] !=0:
        mel=mel-array_1[0]
    else:
        mel=mel
    mel = mel*60
    array_1[1]=int(mel)
    if array_1[1]!=0:
        mel=mel-array_1[1]
    else:
        mel=mel
    mel =round(mel*60,3)
    array_1[2]=mel
    return array_1

#until how many tries you want to simulate with calculated estimated time (with linear Regression below)
M=int(input("Enter max number of tries:"))
k_reg=1.261864*10**(-5)
estimated_time_seconds = k_reg*M*M/2

#time calculation
mel_time=np.zeros(shape=3)
calctime(estimated_time_seconds, mel_time)

#output of the estimated execution time and
print("estimated execution time=", mel_time[0],"h", mel_time[1], "min",mel_time[2], "s")
print("Do you want to execute? [y/n]:")
console_input = input()
if console_input == "n":
    print("process terminated")
    exit()

#creating arrays for plotting purpose
win_percentage_1=np.zeros(shape=M)
win_percentage_2=np.zeros(shape=M)
start=np.zeros(shape=M)
end=np.zeros(shape=M)

#creating a list in order to get the winpercentage of both case (swapping,not swapping)
swap = [True,False]

#starting the timer
start1 = time.time()

#looping through the amount of trys
for N in range(M-1):
    start[N]= time.time()   #starting the timer for the Nth try
    print("tries=",N)    #displaying at which try one is
    for index in swap:      #first calculating until N trys while swapping then while staying
        win=0

#doing the montyhall game N times creating array with 3 elementsthe door with the money gets value 1 the doors with the goats value 0 then the door with index j is the door chosen from the player
        for b in range(N):
            index_array=[]
            doors = np.zeros(shape = 3)
            random_list = [0,1,2]
            i = rd.choice(random_list)
            doors[i]=1
            j = rd.choice(random_list)

            if i != j:  #keeping track of opening the door with a goat behind
                x = i+j
                if x==1:
                    k=2
                if x==2:
                    k=1
                if x==3:
                    k=0
                doors = np.delete(doors,k)
                j= searchindex(doors,index_array)[0]
            else:
                index_array=[]
                searchindex(doors,index_array)

                x=rd.uniform(0,1)
                if x<=0.5:
                    doors = np.delete(doors, index_array[1])
                else:
                    doors = np.delete(doors, index_array[0])
                index_array=[]
                j = searchindex2(doors, index_array)[0]

#determine if you won with each strat
            if index==False:
                if doors[j]==1:
                    win = win + 1
            else:
                if j==0:
                    j=1
                else:
                    j=0
                if doors[j]==1:
                    win = win + 1

#calculating the win percentage at the last amount of trys
        if index==True:
            win_percentage_1[N+1] = win/(N+1)*100
        else:
            win_percentage_2[N+1] = win/(N+1)*100
    end[N]= time.time()

#printing the time and making  arrays for the x values of the plots
print("\n \n*****OUTPUT*****")
print("Win percentage if you swap after",M,"tries:\n",win_percentage_1[M-1],"%\n")
print("Win percentage if you don't swap after",M,"tries:\n",win_percentage_2[M-1],"%\n")
end1=time.time()
delta1=end1-start1
kim_time=np.zeros(shape=3)
calctime(delta1,kim_time)
print("actual execution time:\n", kim_time[0],"h", kim_time[1], "min",kim_time[2], "s\n")
print("estimated execution time:\n", mel_time[0],"h", mel_time[1], "min",mel_time[2], "s\n")
print("difference in estimated and acutal time:\n",abs(delta1-estimated_time_seconds), "s")
print("*****************")
x = np.linspace(0,M,M)
x_1 = np.linspace(0,M-1,M-1)

#linear regression in order to predict the estimated execution time (one time executed to determine k with M=10000, k=1.261864e-5)
x_2 = np.linspace(0,M,M).reshape((-1,1))
time=end-start
model = LinearRegression().fit(x_2,time)
chi_sq = model.score(x_2,time)
d = model.intercept_
k = model.coef_
print("\n \n****REGRESSION OUTPUT****")
print("k=", k[0],"\nchi² =", chi_sq)
print("*************************")

#creating the arrays for the limes values
limes1=np.zeros(shape=M)
limes2=np.zeros(shape=M)
limes3=np.zeros(shape=M)
for i in range(len(limes1)):
    limes1[i]=2.0/3.0*100
    limes2[i]=1.0/3.0*100
    limes3[i]=100

#plotting the winpercentages with their limes
plt.figure(1)
plt.xlabel("Number of tries")
plt.ylabel("win percentage")
plt.plot(x,win_percentage_1, label="swap")
plt.plot(x,limes1,label="66.6")
plt.plot(x,win_percentage_2, label="stay")
plt.plot(x,limes2,label="33.3")
plt.legend(loc="best")

#plotting the execution time
end=np.delete(end,M-1)
start=np.delete(start,M-1)
plt.figure(2)
plt.xlabel("Number of tries")
plt.ylabel("execution time (s)")
plt.plot(x_1,end-start, label="actual duration")
plt.plot(x_1,k_reg*x_1, label="estimating function")
plt.legend(loc='best')

plt.show()
