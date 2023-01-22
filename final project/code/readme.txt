Project Report

problem
The goal of this project is to create a program that will allow the user to input 
a symbol drawing and then ouput the symbol drawing in a new window as code staements for programing.
The program will help improve the user interface of programing by allowing the user to draw a symbol
and then have the program output the code for the symbol. This will allow the user to write code
faster, and provides greater accessability to programing. The full project coinsists of 3 parts.
The first part is the user interface, the second part is the compuetr vision used tgo detect symbols
and the third part is the code generation and execution.

approachs
The first part of the project is the user interface. The user interface will be created using the
Qtpy library. The user interface will have a canvas for the user to draw on, a button to enter the
symbol drawing. It also contains a menu, toolbar, text edtior and terminal. The menu will contain
acctions for handing files and editing the text editor.

The second part of the project is the computer vision. The computer vision will be created using
the OpenCV library. The computer vision will be used to detect the symbol drawing and then output
the code for the symbol drawing. The modee uses a CNN and applies a gaussian blur to the image as 
a preprocessing step. The CNN is trained on a dataset of 500 images for each symbols class. the model
has an accuracy of 84% on the test set. The model is then used to predict the symbol drawn by the user.

The third part of the project is the code generation and execution. The code generation and execution
will be created using the Qtpy library. This will be done by using a dictionary to map the symbol to 
replace then symbols with their common python code. The code will then be executed using the exec with 
the output displayed through the terminal widget.

The way top run and use the application is to run the main.py file. The user will then be able to draw
a symbol on the canvas and then press the enter button. The symbol will then be detected and the code
will be displayed in the text editor. The user can then press the run button to execute the code and
see the output in the terminal.

expected results
Images of the Application in action have been provided below. The first image shows the blank user interface
with the canvas, menu, toolbar, text editor and terminal. The second image shows the user drawing a if statenment
symbol and the correct value being outputted in the text editor. It dshould be noted that thought he model has an 
accuay of 84% the predictions maybe wrong and out ooutput the wroung statement The third image shows a script 
of commands and the expected output from the terminal. However due to a bug wityh using unicode the data the termal 
fuctionalty doesnt run but the logic is present in the code.

Conclusion
The limitations of the project are the accuracy of the model. The model has an accuracy of 84% on the test set.
However the model is not perfect and may output the wrong symbol. The model also has a hard time detecting the 
symbols when they are have a thin brush stroke aswell as when they are drawn in a small area. If i were to continue
this project i would try to improve the accuracy of the model by training it on more data and using a different
model. I would also try to improve the model by using a different preprocessing step. Overall i am happy with the
results of the project and i think it is a good start to a larger project. I think the project is a good example of
how computer vision can be used to improve the user interface of programing and help people in there day to day lives 
with comunicating with computers.