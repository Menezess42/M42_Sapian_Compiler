from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import numpy as np
from lexerv2 import Lexer
from my_parser import Parser


class App(Tk):
    LINES_ABOVE_BELOW = 2

    def __init__(self):
        super().__init__()
        self.mainframe = None
        self.mainWindow_config()
        self.Frames()
        self.menu_bar = Menu(self)
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Abrir", command=self.open_file)
        self.file_menu.add_command(label="Salvar", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Sair", command=self.quit)
        self.menu_bar.add_cascade(label="Arquivo", menu=self.file_menu)
        self.menu_bar.add_command(label="Compilar", command=self.compile_code)
        self.config(menu=self.menu_bar)

    def mainWindow_config(self):
        self.title("Sapian Compile")
        self.iconbitmap("./images/sapians.ico")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.geometry("1200x750")
        self.tk.call("source", "./themes/Azure-ttk-theme-main/azure.tcl")
        self.tk.call("set_theme", "dark")

    def Frames(self):
        self.mainframe = ttk.Frame(self)
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.mainframe.grid_columnconfigure(1, weight=1)
        self.mainframe.grid_rowconfigure(0, weight=1)
        self.textArea()
        self.errorArea()
        self.tokenArea()

    def get_text_matrix(self):
        text = self.text_area.get("1.0", "end-1c")
        lines = text.split("\n")
        content = [line.strip() for line in lines]
        content = np.array(content).reshape(-1, 1)
        return content

    def update_line_numbers(self, event=None):
        lines = len(self.text_area.get("1.0", "end-1c").split("\n"))
        current_line = int(self.text_area.index("insert").split(".")[0])
        line_numbers = np.arange(1, lines + 1)
        self.line_number_bar.config(state="normal")
        self.line_number_bar.delete("1.0", "end")
        self.line_number_bar.insert("end", "\n".join(str(i) for i in line_numbers))
        self.line_number_bar.config(state="disabled")
        if current_line == 1:
            self.line_number_bar.yview_moveto(current_line / lines - 1)
        else:
            self.line_number_bar.yview_moveto(current_line / lines)

    def textArea(self):
        self.line_number_bar = Text(
            self.mainframe,
            width=3,
            padx=4,
            takefocus=0,
            border=3,
            state="disabled",
            font=("Hack NF", 14),
        )
        self.line_number_bar.grid(column=0, row=0, sticky=(N, W, E, S))
        self.text_area = Text(
            self.mainframe,
            bd=2,
            wrap="word",
            width=125,
            height=35,
            font=("Hack NF", 14),
            yscrollcommand=self.on_scroll,
        )
        self.text_area.grid(column=1, row=0, sticky=(N, W, E, S))
        self.text_area.bind("<Key>", self.update_line_numbers)
        self.text_area.bind("<Button-1>", self.update_line_numbers)

    def errorArea(self):
        self.error_area = Text(
            self.mainframe,
            bd=0,
            wrap="word",
            width=130,
            height=7,
            border=3,
            state="disable",
            font=("Hack NF", 14),
        )
        self.error_area.grid(columnspan=2, row=1, sticky=(N, W, E, S))

    def tokenArea(self):
        self.token_area = Text(
            self.mainframe,
            bd=2,
            wrap="word",
            width=35,
            height=33,
            border=3,
            state="disable",
            font=("Hack NF", 14),
        )
        self.token_area.grid(column=2, row=0, rowspan=2, sticky=(N, W, E, S))

    def on_scroll(self, *args):
        self.line_number_bar.yview_moveto(args[0])

    def open_file(self):
        file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[
                ("Sapians Files", "*.sap"),
                ("Text Files", "*.txt"),
                ("Python Files", "*.py"),
                ("All Files", "*.*"),
            ],
        )
        if file_path:
            self.text_area.delete(1.0, END)
            with open(file_path, "r") as f:
                self.text_area.insert(END, f.read())
                self.update_line_numbers()

    def save_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Sapians Files", "*.sap"),
                ("Text Files", "*.txt"),
                ("Python Files", "*.py"),
                ("All Files", "*.*"),
            ],
        )
        if file_path:
            with open(file_path, "w") as f:
                f.write(self.text_area.get(1.0, END))

    def compile_code(self):
        text_matrix = self.get_text_matrix()
        lista = np.array(text_matrix)
        y, x = lista.shape
        lex = Lexer(lista)
        flag, lexer_list, error_list = lex.lexer()
        token = ""
        errors = ""
        for i in range(len(lexer_list)):
            token += f"line: {i+1}\n"
            for l in range(len(lexer_list[i])):
                x, y = lexer_list[i][l]
                token += f"\t token: {x} word: {y}\n\n"

        self.token_area.config(state="normal")
        self.token_area.delete("1.0", "end")
        self.token_area.insert("end", "".join(token))
        self.token_area.config(state="disable")
        self.token_area.config(state="disabled")

        if not flag:
            self.error_area.config(state="normal")  #
            self.error_area.delete("1.0", "end")  #
            self.error_area.insert(
                "end",
                "".join(
                    "Infelizmente existem alguns erros lexicos e nao podemos continuar para o parcer, corrija os erros abaixo para continuarmos:\n\n"
                ),
            )
            for i in range(len(error_list)):
                if error_list[i] != []:
                    for j in range(len(error_list[i])):
                        w = error_list[i][j]
                        print(w)
                        x, y = w
                        errors += x + "\n"
                        errors += f"\t{y}\n"

            self.error_area.insert("end", "".join(errors))
            self.error_area.config(state="disabled")
        else:
            pars = Parser(lexer_list)
            msg = pars.parser()
            self.error_area.config(state="normal")
            self.error_area.delete("1.0", "end")
            if '0' in msg:
                pass
            else:
                msg = "Infelizmente existem alguns erros sintatios e nao podemos continuar a compilacao, corrija os erros abaixo para continuarmos:\n\n" + msg
            self.error_area.insert("end", "".join(str(msg)))
            self.error_area.config(state="disabled")

app = App()
app.mainloop()
