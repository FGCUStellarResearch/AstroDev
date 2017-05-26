"""
Unrelated modules, classes, and functions, from AstroDev v1.07
I don't know that all of these are necessary
"""


def timeSeries():
    """
    Console interaction so the GUI reports status to users
    """
    print("Orig Graph")
     
    console.config(state=NORMAL)         
    console.delete(1.0, END)
    console.insert(END, "Displaying Timeseries...\n")
    console.config(state=DISABLED)
    submit()


def DFFTCall():
    """
    Some function thing that calls the DFFT instead of calling it directly? 
    Appears to also do some plotting inside the GUI
    """
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

    
def BLSPrint():
    """
    Console plotting the BLS results?
    """
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
    
    

# This function calls the BLS function and also prints the corresponding
# information in the GUI console as well as calling the BLS graphing function
def BLSed():
    """
    Function that, when called, calls another function and then another function
    Also has a print statement
    """
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

         