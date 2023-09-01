import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk

# Domyślne wartości - takie na ktorych calkiem ok rysuje wykresy
default_T = 50
default_h = 0.001
default_M = 5
default_L = 2.5

def simulate_system():
    # uzycie defaultów z mozliwoscia wpisania
    T = float(T_entry.get() or default_T)
    h = float(h_entry.get() or default_h)
    M = float(M_entry.get() or default_M)
    L = float(L_entry.get() or default_L)

    # wczytanie parametrów G(s)
    A = float(a1_entry.get())
    B = float(a0_entry.get())
    C = float(b2_entry.get())
    D = float(b1_entry.get())
    E = float(b0_entry.get())
    #LEAD-LAG
    p1 = float(p1_entry.get())
    p2 = float(p2_entry.get())
    z1 = float(z1_entry.get())
    z2 = float(z2_entry.get())

    # obliczone parametry transmitancji recznie
    a3 = A
    a2 = B - A*z2 - A*z1
    a1 = A*z1*z2 - B*z2 - B*z1
    a0 = B*z1*z2
    b4 = C
    b3 = A + B - C*p2 - C*p1
    b2 = E + B + C*p1*p2 - D*p2 - D*p1 - A*z2 - A*z1
    b1 = D*p1*p2 - E*p2 - E*p1 + A*z1*z2 - B*z2 - B*z1
    b0 = E*p1*p2 + B*z1*z2

    # Zmienna czasowa - oś czasu (t - wektor kolumnowy)
    t = np.arange(0, T + h, h)

    signal_type = signal_type_var.get()

#ograniczone - przy losowych wartosciach sie nie sypie
    if signal_type == 'Kwadratowy':
        period_duration = T / L
        num_periods = 1
        u = np.clip(M * np.sign(np.sin(2 * np.pi * t / period_duration)), -100, 100)
        u[int(num_periods * period_duration / h):] = 0
    elif signal_type == 'Trojkatny':
        u = np.clip(M * np.abs((4 / L) * (t % (T / L) - (T / (2 * L)))), -100, 100)
    elif signal_type == 'Sin':
        u = np.clip(M * np.sin(2 * np.pi * t / (T / L)), -100, 100)
    else:
        print("Niepoprawny wybór sygnału wejściowego.")
        return

    y = np.zeros(len(t))

    # Euler
    for i in range(1, len(t)):
        y[i] = np.clip(y[i - 1] + h * (a3 * y[i - 1] ** 3 + a2 * y[i - 1] ** 2 + a1 * y[i - 1] + a0 * u[i - 1]) / (
                    b4 * y[i - 1] ** 4 + b3 * y[i - 1] ** 3 + b2 * y[i - 1] ** 2 + b1 * y[i - 1] + b0),-100,100)

    fig = plt.figure(figsize=(6, 6))
    plt.subplot(2, 1, 1)
    plt.plot(t, u, 'b-')
    plt.ylabel('Amplituda')
    plt.title('Sygnał wejściowy')
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.plot(t, y, 'r-')
    plt.xlabel('Czas')
    plt.ylabel('Amplituda')
    plt.title('Sygnał wyjściowy')
    plt.grid(True)

    plt.tight_layout()
    plt.show()

# GUI
window = tk.Tk()
window.title("Symulator systemu")

# co wpisac
T_label = tk.Label(window, text="całkowity czas symulacji = ")
h_label = tk.Label(window, text="krok symulacji na osi czasu = ")
M_label = tk.Label(window, text="amplituda pobudzenia = ")
L_label = tk.Label(window, text="liczba okresów pobudzenia w czasie symulacji = ")
a1_label = tk.Label(window, text="a1 = ")
a0_label = tk.Label(window, text="a0 = ")
b2_label = tk.Label(window, text="b2 = ")
b1_label = tk.Label(window, text="b1 = ")
b0_label = tk.Label(window, text="b0 = ")
p1_label = tk.Label(window, text="LEAD biegun p1 = ")
p2_label = tk.Label(window, text="LAG biegun p2 = ")
z1_label = tk.Label(window, text="LEAD zero z1 = ")
z2_label = tk.Label(window, text="LAG zero z2 = ")
signal_type_label = tk.Label(window, text="Wybierz sygnał wejściowy:")

T_label.grid(row=0, column=0, sticky=tk.E)
h_label.grid(row=1, column=0, sticky=tk.E)
M_label.grid(row=2, column=0, sticky=tk.E)
L_label.grid(row=3, column=0, sticky=tk.E)
a1_label.grid(row=4, column=0, sticky=tk.E)
a0_label.grid(row=5, column=0, sticky=tk.E)
b2_label.grid(row=6, column=0, sticky=tk.E)
b1_label.grid(row=7, column=0, sticky=tk.E)
b0_label.grid(row=8, column=0, sticky=tk.E)
p1_label.grid(row=9, column=0, sticky=tk.E)
p2_label.grid(row=10, column=0, sticky=tk.E)
z1_label.grid(row=11, column=0, sticky=tk.E)
z2_label.grid(row=12, column=0, sticky=tk.E)
signal_type_label.grid(row=13, column=0, sticky=tk.E)

# wpisywajka
T_entry = tk.Entry(window)
h_entry = tk.Entry(window)
M_entry = tk.Entry(window)
L_entry = tk.Entry(window)
a1_entry = tk.Entry(window)
a0_entry = tk.Entry(window)
b2_entry = tk.Entry(window)
b1_entry = tk.Entry(window)
b0_entry = tk.Entry(window)
p1_entry = tk.Entry(window)
p2_entry = tk.Entry(window)
z1_entry = tk.Entry(window)
z2_entry = tk.Entry(window)

T_entry.insert(tk.END, default_T)
h_entry.insert(tk.END, default_h)
M_entry.insert(tk.END, default_M)
L_entry.insert(tk.END, default_L)

T_entry.grid(row=0, column=1)
h_entry.grid(row=1, column=1)
M_entry.grid(row=2, column=1)
L_entry.grid(row=3, column=1)
a1_entry.grid(row=4, column=1)
a0_entry.grid(row=5, column=1)
b2_entry.grid(row=6, column=1)
b1_entry.grid(row=7, column=1)
b0_entry.grid(row=8, column=1)
p1_entry.grid(row=9, column=1)
p2_entry.grid(row=10, column=1)
z1_entry.grid(row=11, column=1)
z2_entry.grid(row=12, column=1)

# Lista rozwijana
signal_type_var = tk.StringVar(window)
signal_type_var.set("Sin")
signal_type_dropdown = tk.OptionMenu(window, signal_type_var, "Kwadratowy", "Trojkatny", "Sin")
signal_type_dropdown.grid(row=13, column=1, sticky=tk.W)

# Przycisk
simulate_button = tk.Button(window, text="Symuluj", command=simulate_system)
simulate_button.grid(row=14, column=0, columnspan=2)

window.mainloop()

