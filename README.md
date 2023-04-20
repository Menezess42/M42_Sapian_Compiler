# M42 Sapian Compiler
This is a compiler for the Sapian programming language. Sapian is a language I developed during my time in college for the compilers course, and it's named after my professor, whose last name is Sapia.

## What is Sapian?
Sapian is a simple programming language based on C, which is easy to learn. It includes basic data types such as integers, floats, characters, and strings, as well as conditional statements and for and while loops.
For now, I have only written the parser and lexer using Python, and the mainframe is also written in Python and uses Tkinter.
The mainframe is simple and includes two menu buttons, one for compiling and one for opening .sap files, as well as saving them.
- It also has three main areas:
  - The middle area is where you can write Sapian code.
  - The right area shows the code's tokens line by line (which was a requirement from my professor).
  - The bottom area shows any errors.
  ![image](https://user-images.githubusercontent.com/67249275/233231480-c6b9e3f7-1523-45f0-ae04-f118eafaa0a0.png)


## Installation
To use the Sapian compiler, you must have Python 3 installed on your system. You can download Python 3 from [official website](https://www.python.org/downloads/).

Once you have installed it, you can download the Sapian Compiler source code from this repository:
[Sapian Compiler](https://github.com/Menezess42/M42_Sapian_Compiler).

Numpy is required.

## Issue
I have a small bug with the column numbers. It's not something that interferes with using the compiler, but it's a bit annoying. I haven't been able to figure it out yet.
