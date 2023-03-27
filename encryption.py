import re
from unicodedata import normalize

class Encrypter():
    def __init__(self, msg, key):
        self.alphabet = "abcdefghijklmnñopqrstuvwxyz"
        self.alphabet = list(self.alphabet)

        # Transform special characters
        # message
        self.msg = re.sub(
            r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
            normalize( "NFD", msg), 0, re.I
        )        
        self.msg = normalize( 'NFC', self.msg)
        self.msg = list(self.msg)
        # Key
        self.key = key.lower()
        self.key = self.key.replace(" ", "")
        self.key = re.sub(
            r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
            normalize( "NFD", self.key), 0, re.I
        )
        self.key = normalize( 'NFC', self.key)
        self.key = list(self.key)
        
        # Dictionaries
        self.dictionaries = []

    def ckey(self):
        # print(type(self.key))
        # print(self.key)
        # self.key = self.key.lower()
        # self.key = self.key.replace(" ", "")
        
        for letter in self.key:
            try:
                self.alphabet.index(letter)
                self.exist = True
            except ValueError:
                print("La llave contiene caracteres inválidos.")
                self.exist = False
                break
        return self.exist

    def dictionary(self, mode):

        for letter in self.key:
            abc = []
            dictionary = {}

            id = self.alphabet.index(letter)
            abc.extend(self.alphabet[id:])
            abc.extend(self.alphabet[:id])
            if mode == "C":
                count = 0
                for i in abc:
                    dictionary[self.alphabet[count]]=i
                    count += 1
                # self.dictionaries.append(dictionary)
            elif mode == "D":
                count = 0
                for i in abc:
                    dictionary[i]=self.alphabet[count]
                    count += 1
            self.dictionaries.append(dictionary)

        return self.dictionaries

    def cmsg(self):
        dic = self.dictionaries 
        tmsg = [self.msg[i:i+len(dic)] for i in range(0, len(self.msg), len(dic))]

        add_msg = []
        num_dic = 0

        for letter_set in tmsg:
            for letter in letter_set:
                if letter.isupper() == True:
                    upper = True
                    letter = letter.lower()
                else:
                    upper = False

                try:
                    use = self.dictionaries[num_dic]
                    add_letter = use[letter]

                    if upper == True:
                        add_letter = add_letter.upper()

                    add_msg.append(add_letter)
                    num_dic += 1
                    if num_dic == len(dic):
                        num_dic = 0
                except:
                    add_msg.append(letter)

        new_msg = ""

        for letter in add_msg:
            new_msg += letter
        return new_msg
                    



test = Encrypter("Hola, mi nombre es Nicolás, y esta es una prueba para confirmar el funcionamiento de este código.", "Mundo")

test.ckey()
test.dictionary("C")
print(test.cmsg())


