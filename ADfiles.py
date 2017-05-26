"""
File related modules, classes, and functions, from AstroDev v1.07
"""

def getFile():
    """
    Console interaction for feedback from file browsing
    
    Returns: 
        string myFile
    """
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
    
    
def browse():
    """
    GUI interaction for selecting input files to run on
    
    Returns:
        nothing, becuase everything's a global even when it shouldn't be
    """
    console.config(state=NORMAL)         
    console.delete(1.0, END)     
    console.insert(END, "Waiting for input file...\n")
    console.config(state=DISABLED)
    print("browse")
    Tk().withdraw()
    
    filename = easygui.fileopenbox(filetypes = ["*.txt", "*.out", "*.dat"])  

    global e 
    e = filename
    getFile()