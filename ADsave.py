"""
Saving related modules, classes, and functions, from AstroDev v1.07
"""


def saveAs():
    """
    Saves the graph in the window (As what though?)
    """
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

        

def saveTxt():
    """
    Saves selected data to a text file (why though?)
    TODO: There is a whole mess of elif statements down there, which should be cleaned up
    """
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
        
        
"""
Mini functions that set things that should be checked over
"""

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
        