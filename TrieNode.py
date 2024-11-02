

class TrieNode(object):
    def __init__(self):
        self.children = dict()
        self.is_word = False
        self.text = ''
    def insert(self, char):
        if self.text + char in self.children:
            return None
        next = TrieNode()
        next.text = self.text + char
        self.children[char] = next
        return next
    def getText(self):
        return self.text

    def setText(self, text):
        self.text = text
    def setEndWord(self, end):
        self.is_word = end

    def isWord(self):
        return self.is_word

    def getNextCharacters(self):
        return self.children.keys()

    def getChild(self, child):
        return self.children[child]
    def getChildren(self):
        return self.children.items()