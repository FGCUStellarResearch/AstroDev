# Authors: Andy Lezcano
# Date: 03/06/16
# Notes: This program is meant to give users a quick and efficient way to load
# specifically formatted text files from Kepler and K2 mission data for research.
# Version and Changelog: V1.07
# A) Added a ton of comments to clarify functionality
# B) Added some support for the BLS fortran to python plugin

# Package declerations
from Tkinter import *
import easygui
from scipy import signal
from scipy import sparse
import ttk
import tkMessageBox
import FileDialog
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import math
from scipy import signal
from scipy.interpolate import interp1d
import numpy as np   
import pylab     
import bls
    
# Global variable declerations for time and flux values
global times
global fluxes 
global timesNew
global fluxesNew
global subF
global fluxesHere
global dftTrigger
global fDFTMean
global BLSTrigger

# Global variable declerations for the canvases and other necessary arrays
subF = 0
global p
p = []
global f
global dftTrigger
global BLStrigger
BLSTrigger = 0
dftTrigger = 0
global canvas
f = plt.figure(figsize=(5,5), dpi=100)
times = []
fluxes = []
timesNew = np.array([])
fluxesNew = np.array([])
fluxesHere = np.array([])

# This function retrieves the file pointed to in the browse window
def getFile():
    global times
    global fluxes
    global timesNew
    global fluxesNew

    times = []
    fluxes = []
    timesNew = []
    fluxesNew = []
    
    global myFile 
    myFile = e   
    print(myFile)
    console.config(state=NORMAL)         
    console.delete(1.0, END)
    console.insert(END, "The file being worked on is: ")
    console.insert(END, myFile)
    console.insert(END, "\n")
    console.config(state=DISABLED)
    makeMat()
    return myFile

# This function opens the browser window and allows the user to choose a single
# file for input
def browse():
    console.config(state=NORMAL)         
    console.delete(1.0, END)     
    console.insert(END, "Waiting for input file...\n")
    console.config(state=DISABLED)
    print("browse")
    Tk().withdraw()
    

    # global top 
    # top = Toplevel(root)

    # Label(top, text="Value").pack()
    
    filename = easygui.fileopenbox(filetypes = ["*.txt", "*.out", "*.dat"])  

    global e 
    e = filename
    getFile()
    # e.pack(padx=5)

    # b = Button(top, text="OK", command=getFile)
    # b.pack(pady=5)
    
# This function generates the timeseries matrix
def makeMat():
    global subF
    subF = 0
    fluxInd = 1
    console.config(state=NORMAL)         
    console.delete(1.0, END)     
    
    console.insert(END, "Working on building data...")
    console.config(state=DISABLED)
    numLines = 0
    with open(myFile, 'rb') as f:
        for line in f:
            if numLines != 0:
                break
            for c in line:
                if c == "# ":
                    numLines = 2
                    fluxInd = 3
                    break
                else:
                    numLines = 14
                    break
                    
    with open(myFile, 'rb') as inf:
        lines = inf.read().splitlines()[numLines:]
        for line in lines:
            newEl = line.split(',')
            times.append(newEl[0])
            fluxes.append(newEl[fluxInd])
        inf.close

    console.config(state=NORMAL)         
    console.delete(1.0, END)         
    console.insert(END, "Done!\n")
    console.insert(END, "Waiting for submission...\n")
    console.config(state=DISABLED)
    
# This function tells the console in the GUI window to display text when the
# timeseries is graphed
def timeSeries():
    print("Orig Graph")
     
    console.config(state=NORMAL)         
    console.delete(1.0, END)
    console.insert(END, "Displaying Timeseries...\n")
    console.config(state=DISABLED)
    submit()

# This function performs the DFT on the original flux data
def DFFT(ti, xf, f):
    global timesNew
    global fluxesNew
    global X

    t = ti.astype(np.float)
    x = xf.astype(np.float)    
    
    shape = len(f)
    xMean = sum(x)/len(x)
    x = signal.detrend(x)
    x = x/xMean
    ttt = np.transpose(t)
    concArr = np.outer(f, ttt)
    w = np.exp(-2*np.pi*1j*concArr)

    xsize = np.size(f)
    ysize = np.size(ttt)
    
    sumArr = np.zeros((xsize, ysize))
    counterX = 0
    for xInd in range(1,xsize):
        counterY = 0
        print(xInd)
        for yInd in range(1,ysize):
            sumArr[counterX][counterY] = x[yInd]*w[xInd, yInd]
            counterY += 1
        counterX += 1

    X = sumArr.sum(axis = 1)
       
    X = np.reshape(X,shape)
    X = np.abs(X)**2
    return X

# This function will call the DFFT
def DFFTCall():
    global fluxesNew
    global timesNew
    global fluxesDFT
    global fDFTMean
    global fluxesHere

    if analSave.get() == 1:
        fluxesHere = fluxesDFT
    else:
        fluxesHere = fluxesNew

    freq = np.arange(0.0225, 1.0, 0.001)
    
    global dftTrigger
    if dftTrigger == 0:
        tkMessageBox.showinfo(title="DFFT Initiating", message="Please Allow 5-10 seconds for DFT to complete.")
        DFFT(timesNew, fluxesHere, freq)
        dftTrigger = 1
            
    global X
    print("DFT Graph")
     
    console.config(state=NORMAL)         
    console.delete(1.0, END)
    console.insert(END, "Displaying Power Spectrum...\n")
    console.config(state=DISABLED)
    powah = np.array(X)
    plt.clf()
    plt.plot(freq, powah)
    
    maxDotInd = np.argmax(powah)
    plt.plot(freq[maxDotInd], powah[maxDotInd], "8r")

    plt.ylabel("Power")
    plt.xlabel("Frequency")
    plt.title(myFile)   
    canvas.show()
    canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

# Function for phasing the daata by period  
def Phase():
    global fluxesNew
    global timesNew
    global fluxesDFT
    global fluxesHere

    if analSave.get() == 1:
        fluxesHere = fluxesDFT
    else:
        fluxesHere = fluxesNew

    periodDefault = float(entryOne.get())
    period = 1/periodDefault
    time = timesNew.astype(np.float)
    phase = [np.remainder((x/period), 1) for x in time]
    phaseTwo = [x+1 for x in phase]
    print("Phase Graph")
     
    console.config(state=NORMAL)         
    console.delete(1.0, END)
    console.insert(END, "Displaying Phased Graph...\n")
    console.config(state=DISABLED)
    plt.clf()
    ax1 = f.add_subplot(111)
    ax1.scatter(phase, fluxesHere)
    ax1.scatter(phaseTwo, fluxesHere)
    plt.ylabel("Counts")
    plt.xlabel("Phase")
    plt.title(myFile)   
    canvas.show()
    canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)
    
# Function that sorts the data into bins for the filtering algorithm
def bindata(x,y,gx):
    xx = gx
    endxx = np.size(xx)
    binwidth = xx[1:]-xx[:-1]
    pre1 = xx[0]-binwidth[0]/2
    pre2 = xx[1:endxx]+binwidth/2
    pre3 = xx[endxx-1]+binwidth[endxx-2]/2
    xx = np.array(pre1)
    xx = np.append(xx, pre2)
    xx = np.append(xx, pre3)
    
    eps = np.spacing(1)
    t1 = eps*np.abs(xx)
    bins = xx + max(eps + t1)
    
    binMe = np.digitize(x, bins) # may need to change the axis selected as third int param
    
    count = 0
    nn = np.array([])
    while count <= 40:
        temp = sum(binMe == count)
        nn = np.append(nn, temp)
        count += 1
           
    b = np.array([])
    counterBin = 0
    for exii in xrange(0, 40):
        sumTemp = np.array([])
        tempBinArr = np.array([])
        counterr = 0
        for binNum in binMe:
            if binNum == exii:
                tempBinArr = np.append(tempBinArr, y[counterr])
            counterr += 1
        sumTemp = np.sum(tempBinArr)
        b = np.append(b, sumTemp/nn[counterBin]) 
        counterBin += 1              
    
    return b
        
# Function for time series filtering
def filtering():
    global fluxesNew
    global timesNew
    global fluxesDFT
    global fDFTMean
    global tempTime
    global tempFlux
    
    dataF = fluxesNew.astype(np.float)
    dataT = timesNew.astype(np.float)
    

    tempFlux = dataF
    tempTime = dataT

    numcorr = len(tempTime)
    while numcorr > 0:

         # Create time bins
         lIndexT = np.size(tempTime)-1
         bTime = np.linspace(tempTime[0], tempTime[lIndexT], 40)
         bFlux = bindata(tempTime, tempFlux, bTime)   

         fMean = np.mean(dataF)
         bFlux[np.isnan(bFlux)]=fMean
    
         pflux = interp1d(bTime, bFlux, kind = "cubic", bounds_error = FALSE)
         pOut = pflux(tempTime)

         fluxesDFT = tempFlux-pOut
         tsStd = np.std(fluxesDFT)

         numcorr = len(fluxesDFT[abs(fluxesDFT)>3*tsStd])
         tempTime = tempTime[np.where(abs(fluxesDFT)<3*tsStd)]
         tempFlux = tempFlux[np.where(abs(fluxesDFT)<3*tsStd)]
         
    pOut = pflux(dataT)
    fluxesDFT = dataF - pOut

    #fluxesDFT = dataF-pOut
    fDFTMean = np.nanmean(fluxesDFT)
    fluxesDFT[np.isnan(fluxesDFT)]=fDFTMean

    console.config(state=NORMAL)         
    console.delete(1.0, END)
    console.insert(END, "Displaying Detrended Graph...\n")
    console.config(state=DISABLED)
    
    plt.clf()
    plt.plot(dataT, fluxesDFT)
    # plt.plot(dataT,dataF)
    # plt.plot(bTime[1:39],bFlux)
    plt.ylabel("Counts")
    plt.xlabel("Time")
    plt.title(myFile)   
    canvas.show()
    canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)
    
# This function calls the BLS function and also prints the corresponding
# information in the GUI console as well as calling the BLS graphing function
def BLSed():
    global fluxesNew
    global timesNew
    global fluxesDFT
    global fluxesHere

    if analSave.get() == 1:
        fluxesHere = fluxesDFT
    else:
        fluxesHere = fluxesNew
     
    console.config(state=NORMAL)         
    console.delete(1.0, END)
    console.insert(END, "Displaying BLS timeseries...\n")
    console.config(state=DISABLED)
    
    global p 
    global bper
    global bpow
    global depth
    global qtran
    global in1
    global in2
    
    global BLSTrigger
    if BLSTrigger == 0:
        tkMessageBox.showinfo(title="BLS Initiating", message="Please Allow 5-10 seconds for BLS to complete.")
        timesNew = [float(i) for i in timesNew]
        fluxesNew = [float(i) for i in fluxesNew]
        result = bls.eebls(timesNew, fluxesNew, timesNew, fluxesNew, 3, 6, 1, 1, .5, .5)
        print(result);
        BLSPrint()
        BLSTrigger = 1
    else:
        BLSPrint()
    
# This function plots the BLS results    
def BLSPrint():
    print("Plotting BLS")
    global p
    global timesNew
    global fluxesDFT
    global fluxesHere

    if analSave.get() == 1:
        fluxesHere = fluxesDFT
    else:
        fluxesHere = fluxesNew
        
    p = np.array(p) 
    plt.clf()
    plt.plot(timesNew[1:], p, linestyle='--', marker='.')
    plt.ylabel("Flux")
    plt.xlabel("Time")
    plt.title(myFile)   
    canvas.show()
    canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)
    
# def BLS(timeIn, dataPIn, fN, fMin, sF, nB, qMax, qMin):
#     global p 
#     global bper
#     global bpow
#     global depth
#     global qtran
#     global in1
#     global in2        
#     
#     numP = len(timeIn)
# 
#     time = timeIn.astype(np.float)
#     dataP = dataPIn.astype(np.float)
# 
#     indSize = numP-1
#     global p
#     p = indSize*[0] 
#     
#     minBin = 5
#     nBMax = 2000
#     
#     y = [0]*nBMax
#     ibi = [0]*nBMax
#     
#     # These are just some matrix dimension checks to see if input
#     # is grossly incorrect:
#     if nB > nBMax:
#         print 'You have more bins than permitted [nB > nBMax]'
#         exit
# 
#     timeIndMax = numP-1        
#         
#     total = time[timeIndMax]-time[0]
# 
#     if fMin < 1/total:
#         print 'You have a lower minimum frquency than allowed [fMin < 1/T]'
#         exit
#     
#     rN = float(numP)
#     kmi = int(qMin*float(nB))
#     
#     if kmi < 1:
#         kmi = 1
#         exit
#         
#     kma = int(qMax*float(nB))+1
#     kkmi = int(rN*qMin)
#     
#     if kkmi < minBin:
#         kkmi = minBin
#         exit
#         
#     bPow = 0.0
#     
#     s = 0.0
#     t1= time[0]
#     temp1 = indSize*[0]  
#     i1 = 0    
#     
#     while i1 < (numP-1):
#         temp1[i1]=time[i1]-t1
#         s = s+dataP[i1]
#         i1 = i1 + 1
#         
#     s = s/rN
#     
#     i2 = 0
#     temp2 = indSize*[0] 
#     while i2 < (numP-1):
#         temp2[i2] = dataP[i2]-s
#         i2 = i2 + 1
#         j1 = 0    
#         i3 = 0
#         i4 = 0
#         while j1 < fN:
#             f0 = fMin+sF*(float(j1-1))
#             p0 = 1.0/f0
#             
#             while i3 < (numP-1):
#                 ph = temp1[i3]*f0
#                 ph = ph-int(ph)
#                 j2 = 1 + int(nB*ph)
#                 ibi[j2] = ibi[j2] + 1
#                 y[j2] = y[j2] + temp2[i3]
#                 i3 = i3 + 1
#                 
#             power = 0.0
#             
#             while i4 < nB:
#                 s = 0.0
#                 k = 0
#                 kk = 0
#                 nb2 = i4+kma
#                 
#                 if nb2 > nB:
#                     nb2 = nB
#                     
#                 j2 = i3
#                 while j2 < nb2:
#                     k = k+1
#                     kk = kk+ibi(j2)
#                     s = s+y(j2)
#                     
#                     if k > kmi & kk > kmi:
#                         rn1 = float(kk)
#                         powN = (s*s)/(rn1*(rN-rn1))
#                         if powN > power:
#                             power = powN
#                             jn1 = i4
#                             jn2 = j2
#                             rn3 = rn1
#                             s3 = s
#                     j2 = j2 + 1
#                 i4 = i4+1                
#             power = math.sqrt(power)
#             p[j1] = power
#             if power > bPow:
#                 bpow = power
#                 in1 = jn1
#                 in2 = jn2
#                 qtran = rn3/rN
#                 depth = (-s3*rN)/(rn3*(rN-rn3))
#                 bper = p0   
#             j1 = j1+1
#     return p   
    

# This function saves the graph that is currently displayed in the plot window
def saveAs():
    print("saveAs")
     
    console.config(state=NORMAL)         
    console.delete(1.0, END)
    console.insert(END, "Saving...")
    console.config(state=DISABLED)
    fileName = "Output_Plot_"
    myFilePTP = myFile.rsplit('/',10)[-1]
    myFilePT = myFilePTP.rsplit('.',1)[0]
    fileName += myFilePT
    if jpg.get() == 1:
        fileName += ".jpg"
        pylab.savefig(fileName)
         
        console.config(state=NORMAL)         
        console.delete(1.0, END)
        console.insert(END, "Done!\n")
        console.config(state=DISABLED)
    elif tiff.get() == 1:
        fileName += ".tiff"
        pylab.savefig(fileName)    
         
        console.config(state=NORMAL)         
        console.delete(1.0, END)
        console.insert(END, "Done!\n")
        console.config(state=DISABLED)
    elif png.get() == 1:
        fileName += ".png"
        pylab.savefig(fileName) 
         
        console.config(state=NORMAL)         
        console.delete(1.0, END)
        console.insert(END, "Done!\n")
        console.config(state=DISABLED)

# Function which saves the selected data to a text file
def saveTxt():
    print("savetext")
     
    console.config(state=NORMAL)         
    console.delete(1.0, END)
    console.insert(END, "Saving...")
    console.config(state=DISABLED)
    fileName = "Output_"
    myFilePTP = myFile.rsplit('/',10)[-1]
    myFilePT = myFilePTP.rsplit('.',1)[0]
    fileName += myFilePT
    if txt.get() == 1:
        print ("txt")
        fileName += ".txt"
        fileOut = open(fileName, 'w')

        if time.get() == 1:
            for item in timesNew:
                fileOut.write("%s\n" % item)
                # fileOut.write(timesNew)
             
            console.config(state=NORMAL)         
            console.delete(1.0, END)
            console.insert(END, "Done!\n")
            console.config(state=DISABLED)

        if flux.get() == 1:
            for item in fluxesNew:
                fileOut.write("%s\n" % item)
                # fileOut.write(fluxesNew)
             
            console.config(state=NORMAL)         
            console.delete(1.0, END)
            console.insert(END, "Done!\n")
            console.config(state=DISABLED)

    elif csv.get() == 1:
        fileName += ".csv"
        fileOut = open(fileName, 'w')

        if time.get() == 1:
            fileOut.write(times)
             
            console.config(state=NORMAL)         
            console.delete(1.0, END)
            console.insert(END, "Done!\n")
            console.config(state=DISABLED)

        if flux.get() == 1:
            fileOut.write(fluxes)
             
            console.config(state=NORMAL)         
            console.delete(1.0, END)
            console.insert(END, "Done!\n")
            console.config(state=DISABLED)

    elif xls.get() == 1:
        fileName += ".xls"
        fileOut = open(fileName, 'w')

        if time.get() == 1:
            fileOut.write(times)
             
            console.config(state=NORMAL)         
            console.delete(1.0, END)
            console.insert(END, "Done!\n")
            console.config(state=DISABLED)

        if flux.get() == 1:
            fileOut.write(fluxes)
             
            console.config(state=NORMAL)         
            console.delete(1.0, END)
            console.insert(END, "Done!\n")
            console.config(state=DISABLED)

# Function which sets the saved image to jpgs
def setJPG():
    if jpg.get() == 0:
        jpg.set(1)
    else:
        jpg.set(0)
        
# Function which sets the saved image to tiffs        
def setTIFF():
    if tiff.get() == 0:
        tiff.set(1)
    else:
        tiff.set(0)
        
# Function which sets the saved image to pngs
def setPNG():
    if png.get() == 0:
        png.set(1)
    else:
        png.set(0)

# Function which sets the autosave feature, allowing graphs to quickly be saved
# as the user swaps between them
def setAutoSave():
    global autoToggle
    autoToggle = autoToggle + 1
    
    if autoToggle >= 1:
        if autoSave.get() == 0:
            autoSave.set(1)
        else:
            autoSave.set(0)
            
# Function that locks the current data set which will be used in all graphs
# to the detrended values of the flux
def detrendDataSave():
    global dftTrigger
    dftTrigger = 0
    global BLSTrigger
    BLSTrigger = 0

    global autoAnal
    autoAnal = autoAnal + 1
    
    if autoAnal >= 1:
        if analSave.get() == 0:
            analSave.set(1)
        else:
            analSave.set(0)

# Sets the format out of the data file to txt
def setTxt():
    if txt.get() == 0:
        txt.set(1)
    else:
        txt.set(0)

# Sets the format out of the data file to csv
def setCsv():
    if csv.get() == 0:
        csv.set(1)
    else:
        csv.set(0)

# Sets the format out of the data file to xls
def setXls():
    if xls.get() == 0:
        xls.set(1)
    else:
        xls.set(0)

# Sets if time will be saved to the data file
def setTime():
    if time.get() == 0:
        time.set(1)
    else:
        time.set(0)

# Sets if flux will be saved to the data file
def setFlux():
    if flux.get() == 0:
        flux.set(1)
    else:
        flux.set(0)

# Sets if epoch will be saved to the data file
def setEpoch():
    if epoch.get() == 0:
        epoch.set(1)
    else:
        epoch.set(0)

# Submits the currently loaded data to be graphed initially after selection
def submit():

    print("submit")

    if autoSave.get() == 1:
        saveAs()

    global subF
    
    if subF != 1:
         
        console.config(state=NORMAL)         
        console.delete(1.0, END)
        console.insert(END, "Submitted!\n")
        console.config(state=DISABLED)    
        subF = 1
        
    global timesNew
    global fluxesNew
    global fluxesDFT
    global fluxesHere
        
    timesNew = np.array(times)
    fluxesNew = np.array(fluxes)
    
    
    if analSave.get() == 1:
        fluxesHere = fluxesDFT
    else:
        fluxesHere = fluxesNew
        
        
    plt.clf()
    plt.plot(timesNew, fluxesHere)
    plt.ylabel("Counts")
    plt.xlabel("Time")
    plt.title(myFile)
    canvas.show()
    canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)


def cancel():
    print("Exit")
    sys.exit()

    
# The following code segments are all part of building the GUI. The frames are
# declared first, the populated with the corresponding buttons, text boxes, and 
# drop down menus.    
root = Tk()
root.title("AstroDev V1.07")

# declare boolean variables
time = IntVar()
flux = IntVar()
epoch = IntVar()
global autoAnal
autoAnal = 0
txt = IntVar()
csv = IntVar()
xls = IntVar()
autoSave = BooleanVar()
autoSave.set(0)
global autoToggle
autoToggle = 0
analSave = BooleanVar()
jpg = IntVar()
tiff = IntVar()
png = IntVar()

jpg.set(0)
tiff.set(0)
png.set(0)

# declare frames
content = Frame(root, bg='gray15')
frame = Frame(content, borderwidth=5, relief="flat", width=800, height=400, bg='gray30')
frameBottom = Frame(content, borderwidth=5, relief="sunken", width=800, height=200, bg='black')
frameRight = Frame(content, borderwidth=5, relief='sunken', width=300, height=600, bg='gray30')
frameInnerRight = Frame(frameRight, borderwidth=5, relief='sunken', width=300, height=280, bg='gray45')
frameInnerRightB = Frame(frameRight, borderwidth=5, relief='sunken', width=300, height=280, bg='gray45')

input = Button(frameRight, text="Browse...", highlightbackground='gray30', command=browse)
input.grid(column=0, row=0, columnspan=3, sticky=(N, S, E, W))

space = 8

content.grid(column=0, row=0, sticky=(N, S, E, W))
frame.grid(column=0, row=0, columnspan=3, rowspan=2, sticky=(N, S, E, W), padx=space, pady=space)
frameBottom.grid(column=0, row=3, columnspan=3, rowspan=1, sticky=(N, S, E, W), padx=space, pady=space)
frameRight.grid(column=3, row=0, columnspan=2, rowspan=4, sticky=(N, S), padx=space, pady=space)
frameInnerRight.grid(column=0, row=1, columnspan=3, rowspan=4, sticky=(N, S, E, W), padx=space, pady=space)

outputParam = Label(frameInnerRight, text="  Output Parameters", bg='gray45',fg='white')
outputParam.grid(column=0, row=0, sticky=(N, S, W))


test = Frame(frameInnerRight, borderwidth=5, relief='flat', width=300, height=50, bg='gray45')
test.grid(column=0, row=1, columnspan=3, sticky='E, W')

inFrame3 = Frame(frameInnerRight, borderwidth=5, relief='flat', width=300, height=50, bg='gray45')
inFrame3.grid(column=0, row=2, columnspan=3, sticky='E, W')

check1 = Checkbutton(test, text="Time", bg='gray45', variable=time, command= setTime)
check2 = Checkbutton(test, text="Flux", bg='gray45', variable=flux, command= setFlux)
check4 = Checkbutton(inFrame3, text="Use Detrended Data", bg='gray45', variable=autoAnal, command=detrendDataSave)

check1.grid(column=0, row=0)
check2.grid(column=1, row=0)
check4.grid(column=0, row=0)


# outputFormat = Label(frameInnerRight, text="  Output Format", bg='gray45', fg='white')
# outputFormat.grid(column=0, row=3, sticky=(N, S, W))

entryTxt = Label(frameInnerRight, text="Phase Frequencys", bg='gray45', fg='white')
entryTxt.grid(column=0, row=3, sticky=(N, S, E, W))

inFrame = Frame(frameInnerRight, borderwidth=5, relief='flat', width=300, height=50, bg='gray45')
inFrame.grid(column=0, row=4, columnspan=3, sticky='E, W')

entryOne = Entry(inFrame)
entryOne.grid(column=3, row=0)

entryOne.insert(10, '5')

# check5 = Checkbutton(inFrame, text=".txt", bg='gray45', variable=txt, command=setTxt)
# check6 = Checkbutton(inFrame, text=".csv", bg='gray45', variable=csv, command=setCsv)
# check7 = Checkbutton(inFrame, text=".xls", bg='gray45', variable=xls, command=setXls)
# check5.grid(column=0, row=0)
# check6.grid(column=1, row=0)
# check7.grid(column=2, row=0)

graphSele = Label(frameRight, text="Graph Selector", bg='gray30', fg='white')
graphSele.grid(column=0, row=6, columnspan=3, sticky=(N, S, E, W))

nextB = Button(frameRight, text="Timeseries", highlightbackground='gray30', command=timeSeries)
nextB.grid(column=0, row=7, columnspan=1, sticky=(N, S, E, W))

previousB = Button(frameRight, text="DFT", highlightbackground='gray30', command=DFFTCall)
previousB.grid(column=1, row=7, columnspan=1, sticky=(N, S, E, W))

previousC = Button(frameRight, text="Phase", highlightbackground='gray30', command=Phase)
previousC.grid(column=0, row=8, columnspan=1, sticky=(N, S, E, W))

previousC = Button(frameRight, text="Detrend", highlightbackground='gray30', command=filtering)
previousC.grid(column=1, row=8, columnspan=1, sticky=(N, S, E, W))

previousC = Button(frameRight, text="BLS", highlightbackground='gray30', command=BLSed)
previousC.grid(column=0, row=9, columnspan=2, sticky=(N, S, E, W))

frameInnerRightB.grid(column=0, row=10, columnspan=3, rowspan=3, sticky=(N, S, E, W), padx=space, pady=space)

graphOp = Label(frameInnerRightB, text="Graph Options", bg='gray45', fg='white')
graphOp.grid(column=0, row=0, sticky=(N, S, E, W))

autoSaveB = Checkbutton(frameInnerRightB, text="Auto Save", bg='gray45', variable=autoSave, command=setAutoSave)
autoSaveB.grid(column=0, row=1, sticky=(N, S, W))

# analSaveB = Checkbutton(frameInnerRightB, text="Analysis Save", bg='gray45', variable=analSave)
# analSaveB.grid(column=0, row=2, sticky=(N, S, W))

outputFor = Label(frameInnerRightB, text="Output Format", bg='gray45', fg='white')
outputFor.grid(column=0, row=3, sticky=(N, S, E, W))

inFrame2 = Frame(frameInnerRightB, borderwidth=5, relief='flat', width=300, height=50, bg='gray45')
inFrame2.grid(column=0, row=4, columnspan=3, sticky='E, W')

jpgB = Checkbutton(inFrame2, text=".jpg", bg='gray45', variable=jpg, command=setJPG)
jpgB.grid(column=0, row=0)

tiffB = Checkbutton(inFrame2, text=".tiff", bg='gray45', variable=tiff, command=setTIFF)
tiffB.grid(column=1, row=0)

figB = Checkbutton(inFrame2, text=".png", bg='gray45', variable=png, comman=setPNG)
figB.grid(column=2, row=0)

saveAsB = Button(frameInnerRightB, text="Save Plot", highlightbackground='gray45', command=saveAs)
saveAsB.grid(column=0, row=5, columnspan=3, sticky=(N, S, E, W))

outputName = Button(frameInnerRight, text="Save File...", highlightbackground='gray45', command=saveTxt)
outputName.grid(column=0, row=5, columnspan=3, sticky=(N, S, E, W))

submitB = Button(frameRight, text="Submit", highlightbackground='gray30', command=submit)
submitB.grid(column=0, row=14, sticky=(E, W))

cancelB = Button(frameRight, text="Exit", highlightbackground='gray30', command=cancel)
cancelB.grid(column=1, row=14, sticky=(E, W))


root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)


content.columnconfigure(0, weight=100)
content.columnconfigure(1, weight=100)
content.columnconfigure(2, weight=100)
content.columnconfigure(3, weight=1)
content.columnconfigure(4, weight=1)
content.rowconfigure(1, weight=1)


frameInnerRight.columnconfigure(0, minsize=60)
frameInnerRight.columnconfigure(1, minsize=60)
frameInnerRight.columnconfigure(2, minsize=60)

frameInnerRightB.columnconfigure(0, minsize=68)
frameInnerRightB.columnconfigure(1, minsize=68)
frameInnerRightB.columnconfigure(2, minsize=68)

frameRight.columnconfigure(0, minsize=130)
frameRight.columnconfigure(1, minsize=130)

console = Text(frameBottom, height=10, width=100, bg='black', fg='white', highlightbackground='black')
console.pack(fill=BOTH)
console.config(state=DISABLED)

canvas = FigureCanvasTkAgg(f, frame)
toolbar = NavigationToolbar2TkAgg( canvas, frame)

root.mainloop()
