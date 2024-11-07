from TrieNode import TrieNode




class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.size = 0

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
                node.getChild(char).setText(node.text + char)
            node = node.children[char]
        node.setEndWord(True)
        self.size += 1
    def getSize(self):
        return self.size


    def autocomplete(self, prefix, limit=5):
        results = []
        node = self.root
        queue = []
        for char in prefix:
            if char not in node.getNextCharacters():
                return results
            node = node.getChild(char)
        queue.append(node)
        while queue and len(results) < limit:
            node = queue.pop(0)
            for c in node.getNextCharacters():
                child = node.getChild(c)
                if child.isWord() == True:
                    if len(results) < limit:
                        results.append(child.getText())
                queue.append(child)
        return results


    def oneAwayWords(self, word):
        node = self.root
        lim = 0
        results = []
        self.substitution(word, results)
        self.insertion(word, results)
        self.deletion(word, results)
        return results

    def insertion(self, word, retArray):
        for i in range(len(word)+1):
            for char in self.root.getNextCharacters():
                if self.isWord(''.join(word[:i] + char + word[i:])):
                    retArray.append(''.join(word[:i] + char + word[i:]))

    def isWord(self, word):
        node = self.root
        for char in word:
            if char not in node.getNextCharacters():
                return False
            node = node.getChild(char)
        if node.isWord() == True:
            return True
        return False
    def deletion(self, word, retArray):
        for i in range(len(word)):
            if self.isWord(''.join(word[:i] + word[i+1:])) and ''.join(word[:i] + word[i+1:]) not in retArray:
                retArray.append(''.join(word[:i] + word[i+1:]))
    def substitution(self, word, retArray):
        for i in range(len(word)):
            for char in self.root.getNextCharacters():
                if self.isWord(''.join(word[:i] + char + word[i+1:])):
                    retArray.append(''.join(word[:i] + char + word[i+1:]))



def read_file_to_trie(file_path):
    trie = Trie()
    with open(file_path, 'r') as file:
        for line in file:
            word = line.strip()
            trie.insert(word.lower())
    return trie

if __name__ == "__main__":
    trie = read_file_to_trie('dict.txt')
    print(trie.root.getNextCharacters())
    print("Words have been added to the trie.")
    test_word = ''
    while test_word != 'exit':
        print('For spelling suggestions, type 1, for autocomplete press 2:')
        input_Int = input()
        if input_Int == '1':
            test_word = input("Enter a word for spell suggestions: (exit to stop)")
            if trie.isWord(test_word):
                print("That is already a word")
            else:
                print(trie.oneAwayWords(test_word))
        elif input_Int == '2':
            test_word = input("Enter a word for autocomplete suggestions:")
            if trie.isWord(test_word):
                print("That is already a word")
            else:
                print(trie.autocomplete(test_word))
        else:
            print("Invalid input")
