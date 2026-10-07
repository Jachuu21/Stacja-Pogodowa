import customtkinter
import tkinter
import os
from PIL import Image
import serial
from datetime import datetime
import pandas as pd
from matplotlib import pyplot as plt

PORT="COM3"
BAUD_RATE=9600
try:
    arduino = serial.Serial(PORT, BAUD_RATE, timeout=0.1)
except Exception as e:
    print(f"Nie udało się połączyć: {e}")
    arduino = None

   
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Stacja Pogody")
        self.geometry("400x300")
        customtkinter.set_appearance_mode("dark")
        self.grid_columnconfigure(0, weight=1)
        self.temperatura = customtkinter.CTkTextbox(master=self, width=200, height=30, text_color="white", corner_radius=0)
        self.temperatura.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)
        self.temperatura.insert("0.0", "Temperatura: -- *C")
        self.temperatura.configure(state="normal", font=('arial', 20),fg_color="transparent", text_color="white")

        self.cisnienie=customtkinter.CTkTextbox(master=self, width=200, height=30, text_color="white", corner_radius=0)
        self.cisnienie.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.cisnienie.insert("0.0", "Ciśnienie: -- hPa")
        self.cisnienie.configure(state="normal", font=('arial', 20),fg_color="transparent", text_color="white")

        self.wysokosc=customtkinter.CTkTextbox(master=self, width=200, height=30, text_color="white", corner_radius=0)
        self.wysokosc.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)
        self.wysokosc.insert("0.0", "Wysokość: -- m")
        self.wysokosc.configure(state="normal", font=('arial', 20),fg_color="transparent", text_color="white")

        self.wilgotnosc=customtkinter.CTkTextbox(master=self, width=200, height=30, text_color="white", corner_radius=0)
        self.wilgotnosc.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)
        self.wilgotnosc.insert("0.0", "Wilgotność: -- %")
        self.wilgotnosc.configure(state="normal", font=('arial', 20),fg_color="transparent", text_color="white")

        self.rozpocznij=customtkinter.CTkButton(master=self, width=100, height=30, corner_radius=0, fg_color='green', text="Rozpocznij Pomiar", command=self.rozpocznij_pomiar)
        self.rozpocznij.place(relx=0.35, rely=0.8, anchor=tkinter.CENTER)
        
    def rozpocznij_pomiar(self):
        self.rozpocznij.place_forget()
        self.czy_mierzyc = True
        sciezka = "C:/pyton/CPLUS/Projekt2/Aplikacja_Pogoda/dane_pogoda.txt"
        if os.path.exists(sciezka):
            print("Plik dane_stacja.txt istnieje!")
            self.plik=open(sciezka, 'w', encoding='utf-8')
        else:
            print("Nie udało się znaleźć pliku do zapisu danych!")
            self.plik=open(sciezka, 'w', encoding='utf-8')
        if not hasattr(self, "zakoncz_przycisk"):
            self.zakoncz_przycisk=customtkinter.CTkButton(master=self, width=100, height=30, corner_radius=0, fg_color="red", text="Zakończ Pomiar", command=self.zakoncz_pomiar)
            
        self.zakoncz_przycisk.place(relx=0.65, rely=0.8, anchor=tkinter.CENTER)
        self.after(1000, self.aktualizuj_dane)
    def zakoncz_pomiar(self):
        self.czy_mierzyc=False
        if hasattr(self, 'plik') and not self.plik.closed:
            self.plik.close()
            print("Zakończono pomiar i zamknięto plik.")
        
        self.zakoncz_przycisk.place_forget()
        self.rozpocznij.place(relx=0.35, rely=0.8, anchor=tkinter.CENTER)
        sciezka2 = "C:/pyton/CPLUS/Projekt2/Aplikacja_Pogoda/dane_pogoda.txt"
        kolumny=["Temperatura", "Ciśnienie", "Wysokość", "Wilgotność", "Czas"]
        df=pd.read_csv(sciezka2, names=kolumny)

        fig, axes=plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle("Wyniki pomiarów", fontsize=16, fontweight='bold')
        y_wartosc_temp=df["Temperatura"]
        y_wartosc_cis=df["Ciśnienie"]
        y_wartosc_wys=df["Wysokość"]
        y_wartosc_wil=df["Wilgotność"]
        axes[0,0].plot(y_wartosc_temp, 'b-*')
        axes[0,0].set_title('Temperatura [*C]')
        axes[0,0].grid(True, alpha=0.3)

        axes[0,1].plot(y_wartosc_cis, 'g-*')
        axes[0,1].set_title('Ciśnienie [hPa]')
        axes[0,1].grid(True, alpha=0.3)

        axes[1,0].plot(y_wartosc_wys, 'r-*')
        axes[1,0].set_title('Wysokość [m]')
        axes[1,0].grid(True, alpha=0.3)

        axes[1,1].plot(y_wartosc_wil, 'y-*')
        axes[1,1].set_title('Wilgotność [%]')
        axes[1,1].grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
    def aktualizuj_dane(self):
        if self.czy_mierzyc:
            if arduino and arduino.in_waiting > 0:
                linia = arduino.readline().decode('utf-8').strip()
                if linia:
                    dane=linia.split(',')
                    if len(dane)==4:
                        self.temperatura.delete("0.0", "end")
                        self.cisnienie.delete("0.0", "end")
                        self.wysokosc.delete("0.0", "end")
                        self.wilgotnosc.delete("0.0", "end")

                        self.temperatura.insert("0.0",f"Temperatura: {dane[0]} *C")
                        self.cisnienie.insert("0.0",f"Ciśnienie: {dane[1]} hPa")
                        self.wysokosc.insert("0.0",f"Wysokość: {dane[2]} m")
                        self.wilgotnosc.insert("0.0",f"Wilgotność: {dane[3]} %")
                        aktualny_czas = datetime.now().strftime("%H:%M:%S")
                        temp=str(dane[0])
                        cis=str(dane[1])
                        wys=str(dane[2])
                        wil=str(dane[3])
                        self.plik.write(temp)
                        self.plik.write(",")
                        self.plik.write(cis)
                        self.plik.write(",")
                        self.plik.write(wys)
                        self.plik.write(",")
                        self.plik.write(wil)
                        self.plik.write(",")
                        self.plik.write(aktualny_czas)
                        self.plik.write("\n") 
                    
            self.after(2000, self.aktualizuj_dane)   
app=App()
app.mainloop()

