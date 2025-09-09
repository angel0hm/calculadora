import customtkinter as ctk
import json
import calculator
import sys
import os 

def resource_path(relative_path):
    """Obtiene la ruta correcta de un recurso, incluso dentro del exe."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Abrir JSON
with open(resource_path("tema.json"), "r") as f:
    estilos = json.load(f)

# Fuente
font_path = resource_path("fonts/Roboto-VariableFont_wdth,wght.ttf")

def crear_ui(root):
    entrada = ctk.StringVar()

    # ---------------- Barra de título personalizada ----------------
    root.overrideredirect(True)  # quitar barra de Windows
    barra = ctk.CTkFrame(root, height=30, fg_color="#f9f9f9")
    barra.pack(fill="x", side="top")

    # Variables para almacenar posición del mouse
    mouse_pos = {"x": 0, "y": 0}

    def fade_color(widget, start_color, end_color, steps=10, delay=20):
        # Convierte colores hex a RGB
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip("#")
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Convierte RGB a hex
        def rgb_to_hex(rgb):
            return "#%02x%02x%02x" % rgb

        start_rgb = hex_to_rgb(start_color)
        end_rgb = hex_to_rgb(end_color)

        for i in range(1, steps+1):
            # Calcular color intermedio
            r = int(start_rgb[0] + (end_rgb[0]-start_rgb[0])*i/steps)
            g = int(start_rgb[1] + (end_rgb[1]-start_rgb[1])*i/steps)
            b = int(start_rgb[2] + (end_rgb[2]-start_rgb[2])*i/steps)
            widget.after(i*delay, lambda c=rgb_to_hex((r,g,b)): widget.configure(fg_color=c))

    # Uso con barra
    color_normal = "#f9f9f9"
    color_hover = "#E0F0FF"

    barra.bind("<Enter>", lambda e: fade_color(barra, color_normal, color_hover))
    barra.bind("<Leave>", lambda e: fade_color(barra, color_hover, color_normal))

    def guardar_pos(event):
        mouse_pos["x"] = event.x
        mouse_pos["y"] = event.y

    def mover_ventana(event):
        x = event.x_root - mouse_pos["x"]
        y = event.y_root - mouse_pos["y"]
        root.geometry(f"+{x}+{y}")

    barra.bind("<Button-1>", guardar_pos)
    barra.bind("<B1-Motion>", mover_ventana)

    # Botones de cerrar y minimizar
    def cerrar():
        root.destroy()
    btn_cerrar = ctk.CTkButton(barra, text="x", width=30, height=30, fg_color="#CFE7FF", font=("Roboto", 15, "bold"), corner_radius=0,
                               hover_color="#B7DBFF", text_color="#67B3FF", command=cerrar)
    btn_cerrar.pack(side="right", padx=0, pady=0)

    '''
    #-------------------- Minimizar --------------------
    def minimizar():
        root.iconify()

    btn_min = ctk.CTkButton(barra, text="—", width=30, height=30, fg_color="#CFE7FF", font=("Roboto", 15, "bold"), corner_radius=0,
                            hover_color="#B7DBFF", text_color="#67B3FF", command=minimizar)
    btn_min.pack(side="right", padx=0, pady=0)
    '''

    # ---------------- Pantalla ----------------
    pantalla_conf = estilos["pantalla"]
    pantalla = ctk.CTkEntry(
        root,
        textvariable=entrada,
        fg_color=pantalla_conf.get("fg_color"),
        text_color=pantalla_conf.get("text_color"),
        font=tuple(pantalla_conf.get("font", ["Roboto", 22])),
        corner_radius=pantalla_conf.get("corner_radius", 10),
        border_color=pantalla_conf.get("fg_color"),  # mismo color que fondo
        justify="right"
    )
    pantalla.pack(fill="x", padx=15, pady=20, ipady=10)

    # ---------------- Marco de botones ----------------
    marco_conf = estilos["marco"]
    frame = ctk.CTkFrame(root, fg_color=marco_conf.get("bg_color", "#f9f9f9"))
    frame.pack(expand=True, fill="both", padx=10, pady=10)

    # ---------------- Funciones de la calculadora ----------------
    def click_boton(valor):
        entrada.set(calculator.add_to_expression(entrada.get(), valor))

    def borrar_todo():
        entrada.set(calculator.clear_all())

    def borrar_uno():
        entrada.set(calculator.clear_one(entrada.get()))

    def calcular():
        expr = calculator.calculate(entrada.get())
        try:
            resultado = float(expr)
            entrada.set(f"{resultado:.2f}")
        except:
            entrada.set(expr)

    def mostrar_historial():
        data = calculator.get_historial()
        ventana_historial = ctk.CTkToplevel(root)
        ventana_historial.title("Historial")
        ventana_historial.geometry("300x400")
        ventana_historial.transient(root)
        ventana_historial.grab_set()
        ventana_historial.focus_force()
        ventana_historial.configure(fg_color="#f9f9f9")  # color de fondo de toda la ventana

        frame_hist = ctk.CTkFrame(ventana_historial, fg_color="#f9f9f9")
        frame_hist.pack(expand=True, fill="both", padx=10, pady=10)

        texto = ctk.CTkTextbox(frame_hist, font=("Roboto", 20), fg_color="#f9f9f9", text_color="#232931")
        texto.pack(expand=True, fill="both")
        texto.configure(state="normal")
        texto.delete("0.0", "end")

        if not data:
            texto.insert("end", "No hay operaciones aún.\n")
        else:
            for item in data:
                texto.insert("end", item + "\n")
        texto.configure(state="disabled")

    # ---------------- Botones ----------------
    botones = [
        ("Ac", borrar_todo), ("⌫", borrar_uno), ("÷", lambda: click_boton("/")), ("×", lambda: click_boton("*")),
        ("7", lambda: click_boton("7")), ("8", lambda: click_boton("8")), ("9", lambda: click_boton("9")), ("-", lambda: click_boton("-")),
        ("4", lambda: click_boton("4")), ("5", lambda: click_boton("5")), ("6", lambda: click_boton("6")), ("+", lambda: click_boton("+")),
        ("1", lambda: click_boton("1")), ("2", lambda: click_boton("2")), ("3", lambda: click_boton("3")), ("=", calcular),
        ("0", lambda: click_boton("0")), (".", lambda: click_boton(".")), ("H", mostrar_historial)
    ]

    row, col = 0, 0
    total_rows = 4
    for (text, cmd) in botones:
        if text in ["÷", "×", "-", "+"]:
            tipo = "info"
        elif text == "=":
            tipo = "primary"
        elif text == "H":
            tipo = "success"
        else:
            tipo = "secondary"

        style = estilos[tipo]
        rs = 2 if text == "=" else 1

        boton = ctk.CTkButton(
            frame,
            text=text,
            command=cmd,
            fg_color=style["fg_color"],
            hover_color=style["hover_color"],
            text_color=style["text_color"],
            corner_radius=style.get("corner_radius", 20),
            font=tuple(style.get("font", ["Roboto", 20, "bold"]))
        )
        boton.grid(row=row, column=col, rowspan=rs, padx=5, pady=5, ipadx=10, ipady=10, sticky="nsew")

        col += 1
        if col > 3:
            col = 0
            row += 1
            total_rows += rs - 1 if text == "=" else 0

    # Expansión de filas y columnas
    for i in range(4):
        frame.grid_columnconfigure(i, weight=1)
    for i in range(row + 1):
        frame.grid_rowconfigure(i, weight=1)

    return entrada

# ---------------- Inicialización ----------------
if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("350x500")
    crear_ui(root)
    root.mainloop()
