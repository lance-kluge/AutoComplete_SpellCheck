import tkinter as tk
import AutoCompleteDict as acd
from tkinter import filedialog
from tkinter import messagebox


def open_file():

    filepath = filedialog.askopenfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if not filepath:
        return  # No file selected

    try:
        with open(filepath, "r") as f:
            text = f.read()
            text_edit.delete("1.0", tk.END)
            text_edit.insert(tk.END, text)
    except Exception as e:
        tk.messagebox.showerror("Error", f"Failed to open file: {e}")


def save_to_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        try:
            with open(file_path, 'w') as file:
                text_content = text_edit.get("1.0", "end-1c")
                file.write(text_content)
            tk.messagebox.showinfo(title="Saved Text", message=f"File saved: {file_path}")
        except Exception as e:
            tk.messagebox.showinfo(title="Saved Text", message=f"Error saving file: {str(e)}")


def main():
    global spellSuggestions
    global frame
    window = tk.Tk()
    global root
    root = acd.read_file_to_trie('dict.txt')
    window.title('Text Editor')
    window.rowconfigure(0, minsize=200)
    window.columnconfigure(1, minsize=300)
    global text_edit
    text_edit = tk.Text(window, font='Helvetica 18')
    text_edit.grid(row=0, column=1)

    frame = tk.Frame(window, relief=tk.RAISED, bd=2)

    menubar = tk.Menu(window)
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label='Open', command=open_file)
    file_menu.add_command(label='Save', command=save_to_file)
    file_menu.add_separator()
    file_menu.add_command(label='Exit', command=window.quit)
    menubar.add_cascade(label='File', menu=file_menu)
    window.config(menu=menubar)

    AutoComplete_button = tk.Button(frame, text='Autocomplete', command=autocomplete)
    spellCheck_button = tk.Button(frame, text='Spell Check', command=spellcheck)
    spell_Suggestions_button = tk.Button(frame, text='Spell Suggestions', command=spellSuggest)
    global var
    var = tk.StringVar()
    text_label = tk.Label(frame, textvariable=var)
    var.set("")
    global suggestions
    suggestions = []
    global suggestions_Text
    suggestions_Text = list()

    AutoComplete_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
    spellCheck_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
    spell_Suggestions_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
    text_label.grid(row=3, column=0, padx=5, pady=5, sticky="ew")
    for i in range(5):
        suggestions_Text.append(tk.StringVar())
        suggestions.append(tk.Button(frame, textvariable=suggestions_Text[i], command=lambda c=i: button_clicked(c)))
        suggestions[i].grid(row=i + 4, column=0, padx=5, pady=5, sticky="ew")
        suggestions[i].configure(state=tk.DISABLED)

    frame.grid(row=0, column=0, sticky="ns")
    scrollbar = tk.Scrollbar(window, command=text_edit.yview)
    text_edit.config(yscrollcommand=scrollbar.set)
    window.config(menu=menubar)
    window.mainloop()


def spellSuggest():
    global spellSuggestions
    if not text_edit.tag_ranges("sel"):
        var.set("Please select a word")
    else:
        text = text_edit.get('sel.first', 'sel.last')
        if (len(text) == 0) or len(text.replace(" ", "")) == 0 or len(text.replace("\n", "").replace(" ", "")) == 0:
            var.set("Please select a word")
        elif len(text.split(" ")) > 1:
            var.set("Must select only one word")
        elif root.isWord(text):
            var.set("Text is already a word")
        else:
            text = text.replace(" ", "").replace("\n", "")
            text = text.lower()
            spellSuggestions = root.oneAwayWords(text)
            var.set("Suggestions:")
            if len(spellSuggestions) == 0:
                var.set("No suggestions")
            else:
                for i in range(5):
                    if not (i >= len(spellSuggestions)):
                        suggestions_Text[i].set(spellSuggestions[i])
                        suggestions[i].configure(state=tk.NORMAL)


def button_clicked(i):
    global spellSuggestions
    text_edit.insert(tk.SEL_FIRST, spellSuggestions[i])
    text_edit.delete(tk.SEL_FIRST, tk.SEL_LAST)
    for i in range(5):
        suggestions_Text[i].set("")
        suggestions[i].configure(state=tk.DISABLED)


def autocomplete():
    global spellSuggestions
    if not text_edit.tag_ranges("sel"):
        var.set("Please select a word")
    else:
        text = text_edit.get('sel.first', 'sel.last')
        if (len(text) == 0) or len(text.replace(" ", "")) == 0 or len(text.replace("\n", "").replace(" ", "")) == 0:
            var.set("Please select a word")
        elif len(text.split(" ")) > 1:
            var.set("Must select only one word")
        else:
            text = text.replace(" ", "").replace("\n", "")
            text = text.lower()
            spellSuggestions = root.autocomplete(text)
            var.set("Suggestions:")
            if len(spellSuggestions) == 0:
                var.set("No suggestions")
            else:
                for i in range(5):
                    if not (i >= len(spellSuggestions)):
                        suggestions_Text[i].set(spellSuggestions[i])
                        suggestions[i].configure(state=tk.NORMAL)


def spellcheck():
    if not text_edit.get(1.0, tk.END):
        var.set("No text to spell check")
    else:
        line_list = text_edit.get(1.0, tk.END).lower().split('\n')
        line_index = 0
        for line in line_list:
            line_index += 1
            word_index = 0
            words = line.split()
            for word in words:
                if not root.isWord(word):
                    s = str(line_index) + '.' + str(word_index)
                    e = str(line_index) + '.' + str(word_index + len(word))
                    text_edit.tag_add("start", s, e)
                    text_edit.tag_config("start", background="red", foreground="black")
                word_index += len(word) + 1


main()
