import tkinter as tk
from project.PNGFileParser import *
import tkinter.font as font
from project.global_operations import *

class PNGParserGui():


    def __init__(self):
        self.img = 'exif.png'
        self.png_parser = PngFileParser()
        self.private_key = None
        self.size_of_block = None
        self.private_keyCBC = None
        self.size_of_blockCBC = None
        self.vector = None
        self.size = None

        window = tk.Tk()
        window.title('PNG Parser')
        frame = tk.Frame(master=window, width=300, height=600)
        background_button_color ='#778899'
        front_button_color = 'black'
        myFont = font.Font(family='Helvetica', size=14)

        frame = tk.Frame(
            master=window,
            relief=tk.RAISED,
        )
        frame.grid(row=1, column=1, pady=30)
        self.name_var = tk.StringVar()
        frame.grid(row=3, column=1, pady=0)
        fille = tk.Label(frame, text='File name', font=('calibre', 10, 'bold'))
        fille.pack(padx=0, pady=0)
        name_entry = tk.Entry(frame, textvariable=self.name_var, font=('calibre', 10, 'normal'))
        name_entry.pack(padx=0, pady=0)

        frame.grid(row=2, column=1, pady=30)
        button = tk.Button(
            master = frame,
            text="Read file",
            command= lambda: self.read(self.name_var.get()),
            bg=background_button_color,
            fg=front_button_color
        )


        button['font'] = myFont
        button.pack(padx=20, pady=20)

        frame.grid(row=3, column=1, padx=70, pady=30)
        button = tk.Button(
            master = frame,
            text="Display",
            command=lambda: display_image("img/" + self.img),
            bg=background_button_color,
            fg=front_button_color,
        )

        button['font'] = myFont
        button.pack(padx=20, pady=20)

        """
        frame.grid(row=5, column=1, padx=70, pady=30)
        button = tk.Button(
            master = frame,
            text="Fourier Transform",
            bg=background_button_color,
            command=lambda: fast_fourier_transformation("img/" + self.img),
            fg=front_button_color,
        )
        button['font'] = myFont
        button.pack(padx=20, pady=20)
        frame.grid(row=6, column=1, padx=70, pady=30)
        button = tk.Button(
            master = frame,
            text="Save with anonimization",
            command=lambda: self.png_parser.save_with_anonimization("after_test.png"),
            bg=background_button_color,
            fg=front_button_color,
        )
        button['font'] = myFont
        button.pack(padx=20, pady=20)

        frame.grid(row=7, column=1, padx=70, pady=30)
        button = tk.Button(
            master = frame,
            text="Show metadata",
            command=lambda: self.png_parser.meta_data.show_data(),
            bg=background_button_color,
            fg=front_button_color,
        )
        button['font'] = myFont
        button.pack(padx=20, pady=20)
        """

        frame.grid(row=8, column=1, padx=70, pady=30)
        button = tk.Button(
            master = frame,
            text="Encode casual ECB",
            command=lambda: self.encrypt(),
            bg=background_button_color,
            fg=front_button_color,
        )
        button['font'] = myFont
        button.pack(padx=20, pady=20)

        frame.grid(row=9, column=1, padx=70, pady=30)
        button = tk.Button(
            master = frame,
            text="Decrypt casual ECB",
            command=lambda: self.decrypt(),
            bg=background_button_color,
            fg=front_button_color,
        )
        button['font'] = myFont
        button.pack(padx=20, pady=20)



        frame.grid(row=9, column=1, padx=70, pady=30)
        button = tk.Button(
            master = frame,
            text="Encrypt CBC",
            command=lambda: self.encryptCBC(),
            bg=background_button_color,
            fg=front_button_color,
        )
        button['font'] = myFont
        button.pack(padx=20, pady=20)


        frame.grid(row=9, column=1, padx=70, pady=30)
        button = tk.Button(
            master = frame,
            text="Decrypt CBC",
            command=lambda:self.decryptCBC(),
            bg=background_button_color,
            fg=front_button_color,
        )
        button['font'] = myFont
        button.pack(padx=20, pady=20)

        frame.grid(row=9, column=1, padx=70, pady=30)
        button = tk.Button(
            master = frame,
            text="Encrypt compressed",
            command=lambda: self.encryptCompressed(),
            bg=background_button_color,
            fg=front_button_color,
        )
        button['font'] = myFont
        button.pack(padx=20, pady=20)


        frame.grid(row=9, column=1, padx=70, pady=30)
        button = tk.Button(
            master = frame,
            text="Decrypt compressed",
            command=lambda:self.decryptCompressed(),
            bg=background_button_color,
            fg=front_button_color,
        )
        button['font'] = myFont
        button.pack(padx=20, pady=20)

        frame.grid(row=9, column=1, padx=70, pady=30)
        button = tk.Button(
            master = frame,
            text="Encrypt library",
            command=lambda:self.encryptLib(),
            bg=background_button_color,
            fg=front_button_color,
        )
        button['font'] = myFont
        button.pack(padx=20, pady=20)



        window.mainloop()

    def encryptLib(self):
        self.png_parser.encryptLib()
        print("LOGGER: encrypted")
        self.read("after_encrypting.png")
        print("LOGGER: loaded enrypted")

    def read(self,text):
        self.png_parser = None
        self.png_parser = PngFileParser()
        self.img=text
        self.png_parser.readFile(text)
        self.png_parser.do_parsing()
        self.name_var.set("")

    def decrypt(self):
        print("LOGGER: started decryption")
        self.png_parser.decrypt(self.private_key, self.size_of_block)
        print("LOGGER: decrypted")
        self.read("after_decrypting.png")
        print("LOGGER: loaded decrypted")

    def decryptCBC(self):
        print("LOGGER: started decryption")
        self.png_parser.decryptCBC(self.private_keyCBC, self.size_of_blockCBC, self.vector)
        print("LOGGER: decrypted")
        self.read("after_decrypting.png")
        print("LOGGER: loaded decrypted")

    def encrypt(self):
        print("LOGGER: started encryption")
        self.private_key, self.size_of_block = self.png_parser.encrypt()
        print("LOGGER: encrypted")
        self.read("after_encrypting.png")
        print("LOGGER: loaded enrypted")

    def encryptCBC(self):
        print("LOGGER: started encryption")
        self.private_keyCBC, self.size_of_blockCBC, self.vector = self.png_parser.encryptCBC()
        print("LOGGER: encrypted")
        self.read("after_encrypting.png")
        print("LOGGER: loaded enrypted")

    def decryptCompressed(self):
        print("LOGGER: started decryption")
        self.png_parser.decrypt_compressed(self.private_key, self.size_of_block,self.size)
        print("LOGGER: decrypted")
        self.read("after_decrypting.png")
        print("LOGGER: loaded decrypted")

    def encryptCompressed(self):
        print("LOGGER: started encryption")
        self.private_key, self.size_of_block,self.size = self.png_parser.encrypt_compressed()
        print("LOGGER: encrypted")
        self.read("after_encrypting.png")
        print("LOGGER: loaded enrypted")

