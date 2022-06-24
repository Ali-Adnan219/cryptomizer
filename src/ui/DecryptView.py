import crypto
import ui.AbstractView
import ui.SelectView

import customtkinter as ctk
import tkinter as tk

from typing import NoReturn
from translation.Translator import translate


class DecryptView(ui.AbstractView.AbstractView):
    def __init__(self, container, storage) -> NoReturn:
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        super().__init__(container, storage)
        self.grid(column=2, row=2, rowspan=96, columnspan=96, sticky=tk.NSEW)
        self.columnconfigure(tuple(range(10)), weight=1)
        self.rowconfigure(tuple(range(10)), weight=1)

        # back button
        back_button = ctk.CTkButton(master=self, text=translate("back"), command=self.back)
        back_button.grid(column=0, row=0, columnspan=10, sticky="NW")
        # password input field
        self.entry = ctk.CTkEntry(master=self, placeholder_text=translate("password") + "...")
        self.entry.grid(column=1, row=1, columnspan=8, sticky=tk.NSEW)
        # file list box
        self.file_list = tk.Listbox(master=self, height=1, selectmode="multiple")
        self.file_list.grid(column=1, row=3, columnspan=7, rowspan=4, sticky=tk.NSEW)
        # remove file from list-box button
        self.remove_item_button = ctk.CTkButton(
            master=self,
            text=translate("remove.selected.elements"),
            command=self.remove_items,
            fg_color="red",
            hover_color="#ff5555"
        )
        self.remove_item_button.grid(column=8, row=3, rowspan=2, sticky=tk.NSEW)
        # add files button
        self.add_item_button = ctk.CTkButton(
            master=self,
            text=translate("add.files"),
            command=self.add_items
        )
        self.add_item_button.grid(column=8, row=5, rowspan=2, sticky=tk.NSEW)
        # start decryption button
        button = ctk.CTkButton(master=self, text=translate("decrypt.now"), command=self.decrypt)
        button.grid(column=1, row=8, rowspan=1, columnspan=8, sticky=tk.NSEW)

    def start(self) -> NoReturn:
        for path in self.storage.get("files"):
            self.file_list.insert(tk.END, path)

    def decrypt(self) -> NoReturn:
        paths = list(self.file_list.get(0, tk.END))

        password = str(self.entry.get())
        if len(password) < 4:
            raise Exception(translate("password.not.long.enough"))

        if not (dir := tk.filedialog.askdirectory()):
            return

        crypto.decrypt_files_by_path(paths, dir, password)
        tk.messagebox.showinfo(title=translate("decryption.finished"), message=translate("the.decryption.has.been.finished"))
        self.container.switch_frame(ui.SelectView.SelectView)

    def back(self) -> NoReturn:
        self.container.switch_frame(ui.SelectView.SelectView)

    def remove_items(self) -> NoReturn:
        for entry in self.file_list.curselection():
            # do not delete the last item
            if self.file_list.size() > 1:
                self.file_list.delete(entry)


    def add_items(self) -> NoReturn:
        files = tk.filedialog.askopenfilenames(filetypes=[("CRYPT", ".crypt")], title=translate("select.files.for.decryption"))
        if len(files) > 0:
            for file_path in files:
                paths = list(self.file_list.get(0, tk.END))
                if file_path not in paths:
                    self.file_list.insert(tk.END, file_path)