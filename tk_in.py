def main_tk():
    from tkinter import Tk, Button, Entry
    from tkinter.ttk import Combobox
    window=Tk()
    window["bg"] = "#362b2b"
    window.geometry("900x600")
    window.title("Steam analytics")
    window.resizable(False,False)
    class Weapon():
        def __init__(self,name,rare,color,price=0):
            self.name=name
            self.rare=rare
            self.color=color
            self.price=price
        def save(self):
            import sqlite3
            conn = sqlite3.connect('steam.db')
            cur = conn.cursor()
            list_db=(str(self.name), str(self.rare), str(self.color), int(self.price))
            cur.execute("""CREATE TABLE IF NOT EXISTS weapons(
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        rare TEXT,
                        color TEXT,
                        price INTEGER);
                        """)
            print(list_db)
            cur.execute("""INSERT INTO weapons (name, rare, color, price) VALUES (?, ?, ?, ?);""", list_db)
            conn.commit()


    def save_weap():
        name=combo_name.get()
        rare=combo_rare.get()
        rare={'После полевых испытаний':'Field-Tested','Немного поношенное':'Minimal Wear','Закалённое в боях':'Battle-Scarred','Поношенное':'Well-Worn','Прямо с завода':'Factory New'}[rare]
        color=ent_color.get()
        x = Weapon(name, rare, color)
        x.save()

    combo_name = Combobox(window,font="Calibri 23 bold")
    combo_name['values'] = ('Desert Eagle','R8 Revolver','Dual Berettas','Five-SeveN','Glock-18','P2000','USP-S','P250','CZ75','Tec-9','Mag-7','Nova','Sawed-Off','XM1014','PP-Bizon','MAC-10','MP7','MP5-SD','MP9','P90','UMP-45','AK-47','AUG','FAMAS','Galil AR','M4A4','SG 553','LMGs','M249','Negev','AWP','G3SG1','SCAR-20','SSG 08')
    combo_name.place(x=100,y=120, height=55)

    combo_rare = Combobox(window, font="Calibri 23 bold")
    combo_rare['values'] = ('После полевых испытаний','Немного поношенное','Закалённое в боях','Поношенное','Прямо с завода')
    combo_rare.place(x=100, y=230, height=55)

    ent_color = Entry(font="Calibri 23 bold")
    ent_color.place(x=100, y=340, height=55)


    btn_pow_2 = Button(text="Добавить", font="Calibri 43 bold", justify="center", bg="#362b2b", fg="#f67300", command=lambda: save_weap())
    btn_pow_2.place(x=290, y=440, height=70, width=260)
    window.mainloop()
if __name__ == '__main__':
    main_tk()