import numpy as np
import math
from sympy import AssumptionsContext
from matplotlib import pyplot as plt

def GetSpherePoint (CenterCoordinates, Radius, X, Y):
    z = np.sqrt((abs(Radius**2-(X-CenterCoordinates[0])**2-(Y-CenterCoordinates[1])**2)))+CenterCoordinates[2]
    return z
# Least squares sphere fit function definition
def FitSphere(DataPointsArray):
     # Calculation of average values
    Average = np.mean(DataPointsArray, axis = 0)
    N = len(DataPointsArray)

 # A matrix Calculation
    AMatrix = np.empty(3,dtype=object)
    AMatrixFirstRow = []
    AMatrixSecondRow = []
    AMatrixThirdRow = []
    xdata = []
    ydata = []
    zdata = []
    for i in range(N):
        AMatrixFirstRow.append([(DataPointsArray[i][0]*(DataPointsArray[i][0]-Average[0])),(DataPointsArray[i][0]*(DataPointsArray[i][1]-Average[1])),(DataPointsArray[i][0]*(DataPointsArray[i][2]-Average[2]))])
        AMatrixSecondRow.append([(DataPointsArray[i][1]*(DataPointsArray[i][0]-Average[0])),(DataPointsArray[i][1]*(DataPointsArray[i][1]-Average[1])),(DataPointsArray[i][1]*(DataPointsArray[i][2]-Average[2]))])
        AMatrixThirdRow.append([(DataPointsArray[i][2]*(DataPointsArray[i][0]-Average[0])),(DataPointsArray[i][2]*(DataPointsArray[i][1]-Average[1])),(DataPointsArray[i][2]*(DataPointsArray[i][2]-Average[2]))])
        xdata.append(DataPointsArray[i][0])
        ydata.append(DataPointsArray[i][1])
        zdata.append(DataPointsArray[i][2])
        #print(i, AMatrixFirstRow,'\n',AMatrixSecondRow,'\n', AMatrixThirdRow,'\n', )

    AMatrix = np.array((np.sum(AMatrixFirstRow, axis =0),np.sum(AMatrixSecondRow, axis =0), np.sum(AMatrixThirdRow, axis =0)))
    AMatrix = np.multiply((2/N),AMatrix)

 # B Matrix Calculation
    BMatrixFirstRow = []
    BMatrixSecondRow = []
    BMatrixThirdRow = []

    for i in range(N):
        BMatrixFirstRow.append(((DataPointsArray[i][0]**2+DataPointsArray[i][1]**2+DataPointsArray[i][2]**2)*(DataPointsArray[i][0]-Average[0])))
        BMatrixSecondRow.append(((DataPointsArray[i][0]**2+DataPointsArray[i][1]**2+DataPointsArray[i][2]**2)*(DataPointsArray[i][1]-Average[1])))
        BMatrixThirdRow.append(((DataPointsArray[i][0]**2+DataPointsArray[i][1]**2+DataPointsArray[i][2]**2)*(DataPointsArray[i][2]-Average[2])))
        #print(i, BMatrixFirstRow,'\n',BMatrixSecondRow,'\n', BMatrixThirdRow,'\n', )
    
    BMatrix = np.array((np.sum(BMatrixFirstRow, axis =0),np.sum(BMatrixSecondRow, axis =0), np.sum(BMatrixThirdRow, axis =0))).transpose()
    BMatrix = np.multiply((1/N),BMatrix)

 # Results Calculation
    CenterCoordinates = np.matmul(AMatrix.transpose(),AMatrix)
    CenterCoordinates = np.linalg.inv(CenterCoordinates)
    CenterCoordinates = np.matmul(CenterCoordinates,AMatrix.transpose())
    CenterCoordinates = np.matmul(CenterCoordinates,BMatrix)
    #print ("Suggested Center Coordinates", CenterCoordinates)

    R=[]
    for i in range (N):
        R.append((DataPointsArray[i][0]-CenterCoordinates[0])**2+(DataPointsArray[i][1]-CenterCoordinates[1])**2+(DataPointsArray[i][2]-CenterCoordinates[2])**2) 
    Radius = math.sqrt(np.sum(R)/N)
    #print('Radius', Radius)
    # Error Calculation
    a = []
    b = []
    for i in range (N):
        a.append((DataPointsArray[i][2]-GetSpherePoint(CenterCoordinates,Radius,DataPointsArray[i][0],DataPointsArray[i][1]))**2)
        b.append((DataPointsArray[i][2]-Average[2])**2)
    Error = np.sum(a)/np.sum(b)-1
   
    return (CenterCoordinates,Radius,xdata,ydata,zdata, Error)

# Invoking the fucntion and reading values
with open("Input.txt","r") as DataPointsFile:
    lines = [[float(x) for x in line.split(",")] for line in DataPointsFile]
    DataPoints = np.array(lines) 
print("Datapoints Array",'\n', DataPoints)

# breaking the tuple from the function
CenterCoordinates, Radius, xdata, ydata, zdata, Error = FitSphere(DataPoints)
print('\n', 'The results are:','\n','Center of the sphere: ', CenterCoordinates,'\n','Radius of the sphere', Radius, '\n','Fit quality', Error)

# Plotting the sphere
fig = plt.figure()
ax = plt.axes(projection='3d')
xlist = np.linspace(DataPoints.min(),DataPoints.max(),100)
ylist = np.linspace(DataPoints.min(),DataPoints.max(),100)
ax.set(xlim=(DataPoints.min(), DataPoints.max()), ylim=(DataPoints.min(), DataPoints.max()),zlim = (DataPoints.min(), DataPoints.max()))
X,Y= np.meshgrid(xlist,ylist)
Z = np.sqrt(((Radius**2-(X-CenterCoordinates[0])**2-(Y-CenterCoordinates[1])**2)))+CenterCoordinates[2]
ax.scatter3D(xdata, ydata, zdata, cmap='Greens')
ax.scatter3D(CenterCoordinates[0], CenterCoordinates[1], CenterCoordinates[2], cmap='Red')
ax.plot_wireframe(X, Y, Z,color='r')
ax.plot_wireframe(X, Y, -Z,color='r')
ax.set_title('Suggested Sphere')
plt.show()

# Creating a Report

    
