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
        test_word = input("Enter a word to autocomplete: (exit to stop)")
        print(trie.autocomplete(test_word))
