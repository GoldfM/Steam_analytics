from tk_in import main
main()

with open('bd.txt','r') as f:
    txt=f.read()
    f.close()
text=txt.split(';')
print(text)