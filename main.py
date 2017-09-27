import sqlite3
from tkinter import *
from tkinter import messagebox

import os
from PIL import Image, ImageTk

categories = ('Place value',
'Order and compare numbers',
'Negative numbers',
'Number sequences',
'Estimation and Rounding',
'Roman Numerals',
'Solve problems on Number and Place Value',
'Mental addition/subtraction',
'Addition/subtraction with decimals',
'Addition/Subtraction via column method',
'Estimation to check answers',
'Solve problems on addition and subtraction',
'Timetables',
'Multiples',
'Mental/Basic multiplication',
'Long multiplication',
'Long multiplication including decimals',
'Mental/Basic division',
'Short division',
'Short division with decimals',
'Testing divisibility',
'Long division' ,
'Long division with decimals',
'Prime numbers',
'HCF and LCM',
'Questions and Problems on factors and multiples',
'Square and cube numbers',
'Questions and Problems on square and cube numbers',
'Mental mixed calculations',
'BIDMAS',
'Questions and Problems on BIDMAS and mixed calculations',
'Basic fraction questions (like fraction addition / simple mult.)',
'Addition and Subtraction of fractions',
'Multiplication and division of fractions',
'Mixed and improper fractions',
'Mixture of fraction questions',
'Simplifying fractions',
'Equivalent fractions',
'Comparing and ordering fractions',
'Unit and non-unit fractions',
'Complex fraction questions',
'Solve fraction problems',
'Equivalent decimals to fractions',
'Decimal place value',
'Order decimal fractions',
'Percentage/decimal/fraction equivalents',
'Questions on percentages/decimals/fractions',
'Solve problems on fractions/decimals/percentages',
'Ratio and proportion',
'Solve problems on ratio and proportion',
'Algebra',
'Solve problems on algebra',
'Measure and compare',
'Add and subtract measurements',
'Convert between units',
'Convert between metric and imperial',
'Solve problems on measurement',
'Solve problems on money',
'Time including Analogue and digital clocks (12hr/24hr)',
'Estimating times',
'Calenders, months and dates',
'Solve problems involing times or dates',
'Perimeter',
'Area',
'Area of parallelograms and triangles',
'Solve problems on area and perimeter',
'Volume',
'Solve volume problems',
'2D shapes',
'Compare and classify 2D shapes',
'Draw 2-D shapes',
'Questions on shapes',
'Name parts of circle, radius, diameter, circumference',
'Solve problems on 2D shapes',
'3D shapes',
'Features of a 3D shape',
'Solve problems on 3D shapes',
'Angles',
'Solve problems on angles',
'Symmetry in 2D shapes',
'Coordinates',
'Drawing shapes on a coordinates graph',
'Solve problems on coordinates',
'Bar Charts, Bar graphs, tally chart, pictograms and tables, time graphs',
'Questions and interpreting statistical data visualisations (eg. Bar chart)',
'Solve problems on interpreting statistical data visualisations (eg. Bar chart)',
'Venn and Carroll diagrams',
'Pie charts and line graphs',
'Solve problems on Venn and Caroll diagrams',
'Mean, Median and Mode',
'Solve problems on mean, median and mode',
)

difficulty = ('3','4','5','6','7')

class App:
    def __init__(self, master):
        frame = Frame(master)
        self.master = master
        master.protocol("WM_DELETE_WINDOW", self.onClose)
        if not os.path.exists("./questions"):
            os.makedirs("./questions")
        self.setUpSQLite()

        #Setting up relevant variables for the entire program to use
        self.top_left_coord = (0, 0)
        self.bottom_right_coord = (0, 0)
        self.createScanList("./")
        self.currentPage = 0

        #Call relevant functions that sort layout and creating everything
        #Here BasicLayout refers to the drop-down menus, text etc
        #Canvas refers to the part of the GUI that has the scan displayed in it
        frame.grid()
        f1 = Frame(frame)
        f1.grid(row=0,column=1)
        self.createBasicLayout(f1)
        self.createCanvas(frame)

    def setUpSQLite(self):
        self.db = sqlite3.connect('data.db')
        self.cursor = self.db.cursor()
        #self.cursor.execute('SELECT * FROM information_schema.tables WHERE table_scheme = ? AND table_name = ?', ('data.db','Students'))
        self.cursor.execute('SELECT * FROM sqlite_master')
        #print(self.cursor.fetchall()[0])
        try:
            self.cursor.execute('CREATE TABLE questions(ID int NOT NULL, Category varchar(255),Difficulty int, OutOf int, Width int, Height int, Answer varchar(255),Location varchar(255), PRIMARY KEY (ID))')
        except:
            print('Questions table found')
        self.db.commit()


    #This function  places the text boxes, entry boxes, drop-down boxes and buttons
    def createBasicLayout(self, frame):
        #Create Labels
        L1 = Label(frame, text="Category")
        L2 = Label(frame, text="Difficulty")
        L3 = Label(frame, text="Answer")
        L4 = Label(frame, text="Out Of")

        #Creates drop-down boxes and entry box for answer
        self.O1var = StringVar(frame)
        self.O2var = StringVar(frame)
        self.Ansvar = StringVar(frame)
        self.OutOfVar = StringVar(frame)
        self.O1var.set(categories[0])
        self.O2var.set(difficulty[0])
        self.OutOfVar.set(1)
        O1 = OptionMenu(frame,self.O1var, *categories) #I don't know why a pointer is used here, but it works
        O2 = OptionMenu(frame,self.O2var, *difficulty)
        Ans = Entry(frame, textvariable=self.Ansvar)
        OutOf = Entry(frame, textvariable=self.OutOfVar)

        #Creates Buttons for going forward, going back and saving
        B1 = Button(frame, text="Previous Page", command=self.previousPage)
        B2 = Button(frame, text="Save", command=self.saveCurrent)
        B3 = Button(frame, text="Next Page", command=self.nextPage)

        #Places all elements in the grid
        L1.grid(row=0, column=1)
        L2.grid(row=1, column=1)
        L3.grid(row=2, column=1)
        O1.grid(row=0,column=2)
        O2.grid(row=1,column=2)
        Ans.grid(row=2,column=2)
        L4.grid(row=3,column=1)
        OutOf.grid(row=3,column=2)
        B1.grid(row=4,column=1)
        B2.grid(row=4,column=2)
        B3.grid(row=4,column=3)

    def previousPage(self):
        if(self.currentPage != 0):
            self.currentPage -= 1
            self.reloadImage(False)
    def nextPage(self):
        if self.currentPage < self.scanlist.__len__() - 1:
            self.currentPage += 1
            self.reloadImage(False)

    #This method saves the current image selected
    #The maths here deals with the scaling of picture
    def saveCurrent(self):
        if messagebox.askokcancel("CAREFUL","Are you sure you want to save this?"):
            try:
                x_scaling_ratio = self.canvas.imageraw.size[0]/500
                y_scaling_ratio = self.canvas.imageraw.size[1]/500

                absolute_top_left_x = x_scaling_ratio * self.top_left_coord[0]
                absolute_top_left_y = y_scaling_ratio * self.top_left_coord[1]
                absolute_bottom_right_x = x_scaling_ratio * self.bottom_right_coord[0]
                absolute_bottom_right_y = y_scaling_ratio * self.bottom_right_coord[1]

                #If a retard doesn't start a box from the top left - #RetardProofCode #AzharProof
                if(absolute_top_left_y > absolute_bottom_right_y):
                    temp = absolute_top_left_y
                    absolute_top_left_y = absolute_bottom_right_y
                    absolute_bottom_right_y = temp

                if(absolute_top_left_x > absolute_bottom_right_x):
                    temp = absolute_top_left_x
                    absolute_top_left_x = absolute_bottom_right_x
                    absolute_bottom_right_x = temp

                image = self.canvas.imageraw.crop((absolute_top_left_x, absolute_top_left_y,
                                                  absolute_bottom_right_x, absolute_bottom_right_y))


                self.cursor.execute('SELECT COUNT(*) FROM questions')
                #print(self.cursor.fetchall())
                id = self.cursor.fetchall()[0][0] + 1
                #print(id)
                self.cursor.execute('INSERT INTO questions (ID, Category, Difficulty, OutOf, Width, Height, Answer, Location) VALUES (?,?,?,?,?,?,?,?)',
                                    (str(id), self.O1var.get(), int(self.O2var.get()), self.OutOfVar.get() ,image.size[0], image.size[1],
                                     self.Ansvar.get(),"./questions/QID" + str(id) + ".jpg"))
                image.save("./questions/QID" + str(id) + ".jpg")
                self.db.commit()
            except:
                self.db.rollback()
                messagebox._show("ERROR","Error: " + str(sys.exc_info()))





    #This code loads the image stored in self.currentPage
    #The firstTime parameter indicates whether this is the first time the function has been called
    def reloadImage(self, firstTime):
        image = Image.open(self.scanlist[self.currentPage])
        image = image.resize((500,500), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        if firstTime == False:
            self.canvas.delete(self.currentImageOnScreen)
        self.currentImageOnScreen = self.canvas.create_image((0, 0), image=photo, anchor='nw')
        self.canvas.image = photo
        self.canvas.imageraw = Image.open(self.scanlist[self.currentPage])


    #This function creates the canvas (which the picture is on)
    #Then it binds events so we can draw a rectangle on it later
    def createCanvas(self, frame):

        self.canvas = Canvas(frame, width=500, height=500)
        self.reloadImage(True) #Loads first image (true paramater indicates this is for the first time)

        self.canvas.bind("<Button-1>", self.onMouseClick)
        self.canvas.bind("<B1-Motion>", self.onMouseMove)
        self.canvas.bind("<ButtonRelease-1>",self.onMouseRelease)

        self.canvas.grid(row=0,column=0)

    #These functions are for selecting the region you want to be in the question
    #They delete the previous rectangle, draw the new rectangle, and store the coordinate data
    def onMouseClick(self, event):
        self.top_left_coord = (event.x, event.y)
        #print(event.x)
        try:
            self.canvas.delete(self.currentrect)
        except:
            print ('Just created first Rect')

        self.currentrect = self.canvas.create_rectangle(event.x,event.y,event.x,event.y)
    def onMouseMove(self,event):
        self.bottom_right_coord = (event.x, event.y)

        self.canvas.delete(self.currentrect)
        self.currentrect = self.canvas.create_rectangle(self.top_left_coord[0],
                                                        self.top_left_coord[1],
                                                        self.bottom_right_coord[0],
                                                        self.bottom_right_coord[1])


    def onMouseRelease(self,event):
        self.bottom_right_coord = (event.x, event.y)
        self.canvas.delete(self.currentrect)
        self.currentrect = self.canvas.create_rectangle(self.top_left_coord[0],
                                                        self.top_left_coord[1],
                                                        self.bottom_right_coord[0],
                                                        self.bottom_right_coord[1])

    #Creates an array of all scans and store in self.pictureList
    def createScanList(self,path):

        self.scanlist = []
        for file in os.listdir(path):
            if file.endswith(".jpg"):
                self.scanlist.append(file)

        print(self.scanlist)
    def onClose(self):
        self.cursor.close()
        self.master.destroy()

#These 3 lines basically start the program
root = Tk()


app = App(root)
root.mainloop()


