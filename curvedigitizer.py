'''
Copyright (c) 2020 Pantelis Liolios

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from tkinter import Tk, filedialog, messagebox, simpledialog

from numpy import asarray, savetxt

import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def run():
    '''
    Main function of curve digitizer
    '''

    # open the dialog box
    # first hide the root window
    root = Tk()
    root.withdraw()
    # open the dialog
    filein = filedialog.askopenfilename(
        title = "Select image to digitize",
        filetypes = (
            ("jpeg files","*.jpg"),
            ("png files","*.png"))
        )
    if len(filein) == 0:
        # nothing selected, return
        return
    
    # show the image    
    img = mpimg.imread(filein)
    _, ax = plt.subplots()
    ax.imshow(img)
    ax.axis('off')  # clear x-axis and y-axis

    # get reference length in x direction
    xfactor = getReferenceLength(0)

    # get the reference length in y direction
    yfactor = getReferenceLength(1)
    
    # digitize curves until stoped by the user
    reply = True
    while reply:

        messagebox.showinfo("Digitize curve",
            "Please digitize the curve. The first point is the origin." +
            "Left click: select point; Right click: undo; Middle click: finish"
            )

        # get the curve points
        x = plt.ginput(
            -1,
            timeout=0,
            show_clicks=True
            )
        x = asarray(x)
        
        ax.plot(x[:,0],x[:,1],'g','linewidth',1.5)
        plt.draw()

        # convert the curve points from pixels to coordinates
        x[:,0] = (x[:,0]-x[0,0]) * xfactor
        x[:,1] = (x[:,1]-x[0,1]) * yfactor

        # write the data to a file
        # first get the filename
        validFile = False

        while not validFile:
            fileout = filedialog.asksaveasfilename(
                title = "Select file to save the data",
                filetypes = [ ("Simple text files (.txt)", "*.txt") ],
                defaultextension = 'txt'
            )
            if len(fileout) == 0:
                # nothing selected, pop up message to retry
                messagebox.showinfo("Filename error", "Please select a filename to save the data.")
            else:
                validFile = True

        # write the data to file
        savetxt(fileout, x, delimiter='\t')

        
        reply = messagebox.askyesno("Finished?",
            "Digitize another curve?"
            )
    
    # clear the figure
    plt.clf()

def getReferenceLength(index):
    '''
    Get the reference length in the requested direction

    USAGE: factor = getReferenceLength(index)
    index = 0 for x-direction or 1 for y-direction
    '''

    # define a 'direction' string
    direction = 'x' if index == 0 else 'y'

    # get the reference length
    reply = False
    while not reply:
        messagebox.showinfo("Select reference length",
            "Use the mouse to select the reference length in {:s} direction.".format(direction) +
            "Click the start and the end of the reference length."
            )
        coord = plt.ginput(
            2,
            timeout=0,
            show_clicks=True
            ) # capture only two points
        # ask for a valid length
        validLength = False
        while not validLength:
            reflength = simpledialog.askfloat("Enter reference length",
                "Enter the reference length in {:s} direction".format(direction))
            if isinstance(reflength, float):
                validLength = True
            else:
                messagebox.showerror("Error","Please provide a valid length.")
        
        # calculate scaling factor
        deltaref=coord[1][index]-coord[0][index]
        factor=reflength/deltaref

        reply = messagebox.askyesno("Length confirmation",
            "You selected {:4.0f} pixels in {:s} direction corresponding to {:4.4f} units. Is this correct?".format(deltaref, direction, reflength)
            )
    
    return factor

if __name__ == "__main__":
    '''
    Digitize curves from scanned plots
    '''
    
    # run the main function    
    run()