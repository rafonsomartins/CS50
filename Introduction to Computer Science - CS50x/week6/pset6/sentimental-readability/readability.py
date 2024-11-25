# TODO
from cs50 import get_string

text = get_string("Text: ")
letters= 0
words = 1
sentences = 0
for c in text:
    if c.isalpha():
        letters += 1
    if c == ' ':
        words += 1
    if c == '.' or c == '!' or c == '?':
        sentences += 1
L = (letters/words)*100
S = (sentences/words)*100
CL = round(0.0588*L - 0.296*S - 15.8)
if CL < 1:
    print("Before Grade 1")
    exit()
if CL >= 16:
    print("Grade 16+")
    exit()
print(f"Grade {CL}")