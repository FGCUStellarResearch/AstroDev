"""
Math related modules, classes, and functions, from AstroDev v1.07
"""


def makeMat():
    """
    Generates the matrix in memory for the GUI to draw
    """
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
    
    
# This function performs the DFT on the original flux data
def DFFT(ti, xf, f):
    """
    Internally calculates the Discrete Fast Fourier Transform
    
    Args:
        times
        flux
        frequency
    
    Returns: 
        float(?) X (the result of the DFFT)
    """
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
    
    
 
def Phase():
    """
    Internally calculates the phase for the given data and period
    """
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
    """
    Internally calculates bins for the filtering algorithm
    
    Returns:
        list(matrix?) binnedData(?)
    """
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
               
               
 
def filtering():
    """
    Internally calculates some filtered something-or-other for the timeseries
    """
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
                   