from tkinter import *
from tkinter import messagebox
import copy
import numpy as np
from Data import *
from Objects import *
from Graphic import *

def display_score():
    global label_id
    C.delete(label_id)
    label_id = C.create_text(m*unit + 5*unit, n*unit/2, fill = "#f2ba0e", text = str(score), font=('Arial',20,'bold'))

def RunAlgorithm():
    print("Run")

Menu("random")