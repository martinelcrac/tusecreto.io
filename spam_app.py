import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

class TusecretoBot:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("start-maximized")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.base_url = 'https://tusecreto.io/'

    def _nav(self, url):
        self.driver.get(url)
        time.sleep(3)

    def post(self, age, post_text, nsfw):
        self._nav(self.base_url)
        self.driver.find_element(By.XPATH, "//*[contains(text(), 'Escribir')]").click()
        time.sleep(3)
        self.driver.find_element(By.XPATH, """//*[@id="post_submit_form"]/div[1]/div/input""").send_keys(str(age))
        self.driver.find_element(By.XPATH, """//*[@id="post_submit_form"]/div[1]/div/select/option[2]""").click()
        self.driver.find_element(By.XPATH, """//*[@id="post_submit_form"]/textarea""").send_keys(post_text)
        
        # Activar el checkbox si es necesario
        if nsfw:
            checkbox = self.driver.find_element(By.XPATH, """//*[@id="post_submit_nsfw"]""")
            if not checkbox.is_selected():
                checkbox.click()

        self.driver.find_element(By.XPATH, "//*[contains(text(), 'Enviar')]").click()

def enviar_mensajes():
    try:
        num_veces = int(veces_entry.get())
        age = int(age_entry.get())
        post_text = texto_entry.get()
        nsfw = checkbox_var.get()

        bot = TusecretoBot()

        for i in range(num_veces):
            bot.post(age, post_text, nsfw)
            age += 1

        bot.driver.quit()
        messagebox.showinfo("Finalizado", "Mensajes enviados correctamente.")
    except ValueError:
        messagebox.showerror("Error", "Ingrese valores válidos para la cantidad de veces y la edad.")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Tusecreto Bot")

# Etiqueta y entrada para la cantidad de veces
tk.Label(ventana, text="Cantidad de veces a enviar:").pack()
veces_entry = tk.Entry(ventana)
veces_entry.pack()

# Etiqueta y entrada para la edad
tk.Label(ventana, text="Edad:").pack()
age_entry = tk.Entry(ventana)
age_entry.pack()

# Etiqueta y entrada para el texto del mensaje
tk.Label(ventana, text="Texto del mensaje:").pack()
texto_entry = tk.Entry(ventana)
texto_entry.pack()

# Checkbox para activar/desactivar el NSFW
checkbox_var = tk.BooleanVar()
tk.Checkbutton(ventana, text="Activar NSFW", variable=checkbox_var).pack()

# Botón para enviar los mensajes
tk.Button(ventana, text="Enviar Mensajes", command=enviar_mensajes).pack(pady=20)

# Ejecutar el bucle principal de la aplicación
ventana.mainloop()
