#libraries
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import openpyxl
import math

#function to convert time in decimals
def convert_time (hours_c):
    if int(hours_c[0:2])>0 & int(hours_c[3:5])==0:
        x=int(hours_c[0:2])
        if int(hours_c[3:5])>0:
            horas=int(hours_c[3:5])/60
            x=x+horas
    elif (int(hours_c[3:5])>0):
        x=int(hours_c[3:5])/60
    elif int(hours_c[0:2])==0 & int(hours_c[3:5])==0:
        x=0
    return x

#function to use lagrange Interpolation
def lagrange_inter(x,hoursknown,containersknown,matrix):
    fx=0
    lx= np.ones(len(hoursknown))
    #Using the Lagrange interpolation method to estimate the number of containers
    for i in range(len(hoursknown)):
        for j in range(len(hoursknown)):
            if(i!=j):
                lx[i] = lx[i] * ((x-hoursknown[j])/(hoursknown[i]-hoursknown[j]))
        fx = fx + (containersknown[i]* lx[i])
    #print('lx = ', lx)
    #print('fx = ', fx)
    #adding the result for x to the matrix
    matrix=np.append(matrix,[x,math.floor(fx),fx])
    matrix=matrix.reshape(int(len(matrix)/3),3)
    return (matrix)

#funtion to sort the matrix and change the format of the time
def sort_convert_time(matrix):
    #Sorting the matrix
    matrixsor=np.sort(matrix,axis=0)
    #changing hours to HH:MM format
    for i in range (len(matrixsor)):
        #print(time)
        horas = int(matrixsor[i,0])
        minutos = (matrixsor[i,0]*60) % 60
        #print('horas ',horas,'min ',minutos)
        matrixsor[i,0] ='%02d:%02d' % (horas, minutos)
    return matrixsor

#read file
file = pd.read_csv(r'C:\Users\mmdav\Downloads\HelgenTech\container_data.csv')

#Change NaN to 0
file['ContainersProcessed']=file['ContainersProcessed'].fillna(0)

#split timestamp in date and time and added to the file
timestamp=file['Timestamp'].str.split(expand=True)
timestamp.columns = ['date','time']
file= pd.concat([file,timestamp],axis=1)


#graphic with missing values
plt.figure(1)
plt.title('Containers Processed with Missing Values')
plt.xlabel('Hours')
plt.ylabel('Containers')
plt.plot(file['time'],file['ContainersProcessed'],'o-')
plt.show
#plt.savefig('ContainersProcessedMV.png')


#filter the data to obtain only the values known and create a matrix
filter_cont=file['ContainersProcessed'] > 0
dataknown = file[filter_cont]
#print(dataknown)
containersknown=dataknown['ContainersProcessed'].reset_index(drop=True)
hoursknown=(dataknown['time']).reset_index(drop=True)
for i in range (len(hoursknown)):
    hoursknown[i]=convert_time(hoursknown[i])
matrix=np.column_stack((hoursknown,containersknown,containersknown))

#for x=2
matrix=lagrange_inter(2,hoursknown,containersknown,matrix)
#for x=4
matrix=lagrange_inter(4,hoursknown,containersknown,matrix)

matrixprb2=sort_convert_time(matrix)

#save matrix with all the values calculated in Excel
df = pd.DataFrame(matrixprb2, columns = ['Time','Containers_Estimated','Containers_Calculated'])
df.to_excel('ValuesCalculatedPrb2.xlsx', sheet_name='Estimation')

#graphic without missing values and save the image
fig, axs = plt.subplots(2)
fig.suptitle('Containers Processed with Values Calculated')
fig.supxlabel('Time')
fig.supylabel('Containers')
axs[0].plot(file['time'],file['ContainersProcessed'],'o-')
axs[1].plot(matrixprb2[:,0],matrixprb2[:,1],'o-')
#plt.plot(matrixprb2[:,0],matrixprb2[:,1],'o-') 
plt.show
#plt.savefig('ContainersProcessedPrb1.png')

#create an algorith to insert values into the matrix
flag=0

while flag==0:
    timex=input('Insert Time with format HH:MM if you want to cancel insert N')
    x=0
    if len(timex)==5:
        x=convert_time(timex)
        print('x = ',x,'horas = ',int(timex[0:2]),'minutos = ',int(timex[3:5]))
        matrix=lagrange_inter(x,hoursknown,containersknown,matrix)
    elif timex=='N':
        flag=1
    else:
        print('Try again with the correct format')

matrixsor=sort_convert_time(matrix)

#save matrix with all the values calculated in Excel
df = pd.DataFrame(matrixsor, columns = ['Time','Containers_Estimated','Containers_Calculated'])
df.to_excel('ValuesCalculated.xlsx', sheet_name='Estimation')

#graphic without missing values
plt.figure()
plt.title('Containers Processed with Values Calculated')
plt.xlabel('Time')
plt.ylabel('Containers')
plt.plot(matrixsor[:,0],matrixsor[:,1],'o-')
plt.show
#plt.savefig('ContainersProcessedPrb2.png')

