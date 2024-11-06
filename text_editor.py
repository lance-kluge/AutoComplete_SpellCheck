import tkinter as tk
import AutoCompleteDict as acd


def main():
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
    AutoComplete_button = tk.Button(frame, text='Autocomplete', command=autocomplete)
    spellCheck_button = tk.Button(frame, text='Spell Check', command = spellcheck)
    spell_Suggestions_button = tk.Button(frame, text= 'Spell Suggestions', command = spellSuggest)

    var = tk.StringVar()
    text_label = tk.Label(frame, textvariable=var)
    var.set("")

    AutoComplete_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
    spellCheck_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
    spell_Suggestions_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
    text_label.grid(row=3, column=0, padx=5, pady=5, sticky="ew")


    frame.grid(row=0, column=0, sticky="ns")
    scrollbar = tk.Scrollbar(window, command=text_edit.yview)
    text_edit.config(yscrollcommand=scrollbar.set)

    window.mainloop()


def spellSuggest():
    text = text_edit.get('sel.first', 'sel.last')
    if(len(text.split(" "))):
        print("too many words")
    print(text)

def autocomplete():
    return None
def spellcheck():
    line_list = text_edit.get(1.0, tk.END).split('\n')
    line_index = 0
    for line in line_list:
        line_index += 1
        word_index = 0
        words = line.split()
        for word in words:
            if not root.isWord(word):
                s = str(line_index)+'.' + str(word_index)
                e = str(line_index)+'.' + str(word_index+len(word))
                text_edit.tag_add("start", s, e)
                text_edit.tag_config("start", background="red", foreground="black")
            word_index+= len(word) + 1





main()