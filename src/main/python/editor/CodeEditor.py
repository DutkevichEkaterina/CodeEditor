from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from highlighter.HighlighterTreeSitterImpl import HighlighterTreeSitterImpl
from editor.TagAdd import TagAdd
from editor.TagRegistry import TagRegistry
from editor.Theme import Theme


class ModifiedMixin:
    '''
    Class to allow a Tkinter Text widget to notice when it's modified.

    To use this mixin, subclass from Tkinter.Text and the mixin, then write
    an __init__() method for the new class that calls _init().

    Then override the beenModified() method to implement the behavior that
    you want to happen when the Text is modified.
    '''

    def _init(self):
        '''
        Prepare the Text for modification notification.
        '''

        # Clear the modified flag, as a side effect this also gives the
        # instance a _resetting_modified_flag attribute.
        self.clearModifiedFlag()

        # Bind the <<Modified>> virtual event to the internal callback.
        self.bind_all('<<Modified>>', self._beenModified)

    def _beenModified(self, event=None):
        '''
        Call the user callback. Clear the Tk 'modified' variable of the Text.
        '''

        # If this is being called recursively as a result of the call to
        # clearModifiedFlag() immediately below, then we do nothing.
        if self._resetting_modified_flag: return

        # Clear the Tk 'modified' variable.
        self.clearModifiedFlag()

        # Call the user-defined callback.
        self.beenModified(event)

    def beenModified(self, event=None):
        '''
        Override this method in your class to do what you want when the Text
        is modified.
        '''
        pass

    def clearModifiedFlag(self):
        '''
        Clear the Tk 'modified' variable of the Text.

        Uses the _resetting_modified_flag attribute as a sentinel against
        triggering _beenModified() recursively when setting 'modified' to 0.
        '''

        # Set the sentinel.
        self._resetting_modified_flag = True

        try:

            # Set 'modified' to 0.  This will also trigger the <<Modified>>
            # virtual event which is why we need the sentinel.
            self.tk.call(self._w, 'edit', 'modified', 0)

        finally:
            # Clean the sentinel.
            self._resetting_modified_flag = False



class TextWithUpdates(ModifiedMixin, Text):
    '''
    Subclass both ModifiedMixin and Tkinter.Text.
    '''

    def __init__(self, update_highlight, *a, **b):
        # Create self as a Text.
        self.update_highlight = update_highlight
        Text.__init__(self, *a, **b)

        # Initialize the ModifiedMixin.
        self._init()

    def beenModified(self, event=None):
        self.update_highlight()

class CodeEditor:
    def __init__(self, root, highlighter: HighlighterTreeSitterImpl, styles_dict: dict):
        self.root = root
        self.highlighter = highlighter
        self.root.title("CODE EDITOR")
        self.root.geometry("700x1700+200+150")

        self.filename = None
        self.title = StringVar()
        self.status = StringVar()
        self.titlebar = Label(self.root, textvariable=self.title, font=("calibri", 11, "bold"), bd=2,
                              relief=GROOVE)
        self.titlebar.pack(side=TOP, fill=BOTH)
        self.settitle()
        self.statusbar = Label(self.root, textvariable=self.status, font=("calibri", 11, "bold"), bd=2,
                               relief=GROOVE)
        self.statusbar.pack(side=BOTTOM, fill=BOTH)
        self.status.set("Welcome To Text Editor")
        self.menubar = Menu(self.root, font=("calibri", 11, "bold"), activebackground="skyblue")
        self.root.config(menu=self.menubar)
        self.filemenu = Menu(self.menubar, font=("calibri", 11, "bold"), activebackground="skyblue", tearoff=0)
        self.filemenu.add_command(label="New", accelerator="Ctrl+N", command=self.newfile)
        self.filemenu.add_command(label="Open", accelerator="Ctrl+O", command=self.openfile)
        self.filemenu.add_command(label="Save", accelerator="Ctrl+S", command=self.savefile)
        self.filemenu.add_command(label="Save As", accelerator="Ctrl+A", command=self.saveasfile)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", accelerator="Ctrl+E", command=self.exit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.editmenu = Menu(self.menubar, font=("calibri", 11, "bold"), activebackground="skyblue", tearoff=0)
        self.editmenu.add_command(label="Cut", accelerator="Ctrl+X", command=self.cut)
        self.editmenu.add_command(label="Copy", accelerator="Ctrl+C", command=self.copy)
        self.editmenu.add_command(label="Paste", accelerator="Ctrl+V", command=self.paste)
        self.editmenu.add_separator()
        self.editmenu.add_command(label="Undo", accelerator="Ctrl+U", command=self.undo)
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)
        self.helpmenu = Menu(self.menubar, font=("calibri", 11, "bold"), activebackground="skyblue", tearoff=0)
        self.helpmenu.add_command(label="About", command=self.infoabout)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)
        scrol_y = Scrollbar(self.root, orient=VERTICAL)
        self.txtarea = TextWithUpdates(self.update_highlight, self.root, yscrollcommand=scrol_y.set, font=("calibri", 10, "bold"), state="normal")
        # self.txtarea.tag_configure("red", foreground ="red")

        scrol_y.pack(side=RIGHT, fill=Y)
        scrol_y.config(command=self.txtarea.yview)
        self.txtarea.pack(fill=BOTH, expand=1)
        #self.configure_tags()
        self.shortcuts()
        self.tag_registry = TagRegistry(styles_dict)
        self.styles_dict = styles_dict
        self.h_callback = TagAdd(self.tag_registry, self.txtarea)
        self.theme = Theme(styles_dict, self.txtarea)
        self.old_text = ""


    def settitle(self):
        if self.filename:
            self.title.set(self.filename)
        else:
            self.title.set("Untitled")

    def newfile(self, *args):
        self.txtarea.delete("1.0", END)
        self.filename = None
        self.settitle()
        self.status.set("New File Created")

    def openfile(self, *args):
        try:
            self.filename = filedialog.askopenfilename(title="Select file", filetypes=(
            ("All Files", "*.*"), ("Text Files", "*.txt"), ("Python Files", "*.py")))
            if self.filename:
                infile = open(self.filename, "r")
                self.txtarea.delete("1.0", END)
                for line in infile:
                    self.txtarea.insert(END, line)
                infile.close()
                self.settitle()
                self.status.set("Opened Successfully")
        except Exception as e:
            messagebox.showerror("Exception", e)
        s = self.txtarea.get("1.0", END)
        self.highlighter.highlight(self.txtarea.get("1.0", END), self.h_callback)

    def update_highlight(self):
        # if self.old_text == "":
        for tag in self.txtarea.tag_names():
            self.txtarea.tag_delete(tag)
        self.theme.update()
        self.highlighter.highlight(self.txtarea.get("1.0", END), self.h_callback)



    def savefile(self, *args):
        try:
            if self.filename:
                data = self.txtarea.get("1.0", END)
                outfile = open(self.filename, "w")
                outfile.write(data)
                outfile.close()
                self.settitle()
                self.status.set("Saved Successfully")
            else:
                self.saveasfile()
        except Exception as e:
            messagebox.showerror("Exception", e)

    # Defining Save As File Funtion
    def saveasfile(self, *args):
        try:
            untitledfile = filedialog.asksaveasfilename(title="Save file As", defaultextension=".txt",
                                                        initialfile="Untitled.txt", filetypes=(
                ("All Files", "*.*"), ("Text Files", "*.txt"), ("Python Files", "*.py")))
            data = self.txtarea.get("1.0", END)
            outfile = open(untitledfile, "w")
            outfile.write(data)
            outfile.close()
            self.filename = untitledfile
            self.settitle()
            self.status.set("Saved Successfully")
        except Exception as e:
            messagebox.showerror("Exception", e)

    # Defining Exit Funtion
    def exit(self, *args):
        op = messagebox.askyesno("WARNING", "Your Unsaved Data May be Lost!!")
        if op > 0:
            self.root.destroy()
        else:
            return

    # Defining Cut Funtion
    def cut(self, *args):
        self.txtarea.event_generate("<<Cut>>")

    # Defining Copy Funtion
    def copy(self, *args):
        self.txtarea.event_generate("<<Copy>>")

    # Defining Paste Funtion
    def paste(self, *args):
        self.txtarea.event_generate("<<Paste>>")

    # Defining Undo Funtion
    def undo(self, *args):
        # Exception handling
        try:
            if self.filename:
                self.txtarea.delete("1.0", END)
                infile = open(self.filename, "r")
                for line in infile:
                    self.txtarea.insert(END, line)
                infile.close()
                self.settitle()
                self.status.set("Undone Successfully")
            else:
                self.txtarea.delete("1.0", END)
                self.filename = None
                self.settitle()
                self.status.set("Undone Successfully")
        except Exception as e:
            messagebox.showerror("Exception", e)

    # Defining About Funtion
    def infoabout(self):
        messagebox.showinfo("About Text Editor", "A Simple Text Editor\nCreated using Python.")

    # Defining shortcuts Funtion
    def shortcuts(self):
        self.txtarea.bind("<Control-n>", self.newfile)
        self.txtarea.bind("<Control-o>", self.openfile)
        self.txtarea.bind("<Control-s>", self.savefile)
        self.txtarea.bind("<Control-a>", self.saveasfile)
        self.txtarea.bind("<Control-e>", self.exit)
        self.txtarea.bind("<Control-x>", self.cut)
        self.txtarea.bind("<Control-c>", self.copy)
        self.txtarea.bind("<Control-v>", self.paste)
        self.txtarea.bind("<Control-u>", self.undo)
