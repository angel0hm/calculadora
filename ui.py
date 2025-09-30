import customtkinter as ctk
import json
import calculator
import sys
import os 

def resource_path(relative_path):
    #Obtiene la ruta correcta de un recurso
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("Calculadora_v1")
    return os.path.join(base_path, relative_path)

# Abrir JSON
with open(resource_path("tema.json"), "r") as f:
    estilos = json.load(f)

# Fuente
font_path = resource_path("fonts/Roboto-VariableFont_wdth,wght.ttf")


# -------------------- Animación de transición de color --------------------
def fade_color(widget, end_color, steps=10, delay=10):
    """Transición suave de color de fondo, incluso con movimientos bruscos del mouse."""
    # Cancelar animación anterior
    if hasattr(widget, "_after_id") and widget._after_id:
        widget.after_cancel(widget._after_id)
        widget._after_id = None

    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def rgb_to_hex(rgb):
        return "#%02x%02x%02x" % rgb

    start_color = widget.cget("fg_color")
    start_rgb = hex_to_rgb(start_color)
    end_rgb = hex_to_rgb(end_color)

    def step(i=1):
        if i > steps:
            widget._current_color = end_color
            widget._after_id = None
            widget.configure(fg_color=end_color)
            return
        r = int(start_rgb[0] + (end_rgb[0]-start_rgb[0])*i/steps)
        g = int(start_rgb[1] + (end_rgb[1]-start_rgb[1])*i/steps)
        b = int(start_rgb[2] + (end_rgb[2]-start_rgb[2])*i/steps)
        widget.configure(fg_color=rgb_to_hex((r,g,b)))
        widget._after_id = widget.after(delay, lambda: step(i+1))

    step()


def crear_ui(root):
    entrada = ctk.StringVar()
    expr_logica = ctk.StringVar(value="") 

    # ---------------- Barra de título ----------------
    root.overrideredirect(True)
    barra = ctk.CTkFrame(root, height=30, fg_color="#f9f9f9")
    barra.pack(fill="x", side="top")

    mouse_pos = {"x": 0, "y": 0}
    color_normal = "#f9f9f9"
    color_hover = "#E0F0FF"
    barra._current_color = color_normal

    barra.bind("<Enter>", lambda e: fade_color(barra, color_hover))
    barra.bind("<Leave>", lambda e: fade_color(barra, color_normal))

    def guardar_pos(event):
        mouse_pos["x"] = event.x
        mouse_pos["y"] = event.y

    def mover_ventana(event):
        x = event.x_root - mouse_pos["x"]
        y = event.y_root - mouse_pos["y"]
        root.geometry(f"+{x}+{y}")

    barra.bind("<Button-1>", guardar_pos)
    barra.bind("<B1-Motion>", mover_ventana)

    # Botón de cerrar
    def cerrar():
        root.destroy()
    btn_cerrar = ctk.CTkButton(barra, text="x", width=30, height=30, fg_color="#CFE7FF",
                               font=("Roboto", 15, "bold"), corner_radius=0,
                               hover_color="#B7DBFF", text_color="#67B3FF",
                               command=cerrar)
    btn_cerrar.pack(side="right", padx=0, pady=0)

    # ---------------- Pantalla ----------------
    pantalla_conf = estilos["pantalla"]
    pantalla = ctk.CTkEntry(
        root,
        textvariable=entrada,
        fg_color=pantalla_conf.get("fg_color"),
        text_color=pantalla_conf.get("text_color"),
        font=tuple(pantalla_conf.get("font", ["Roboto", 22])),
        corner_radius=pantalla_conf.get("corner_radius", 10),
        border_color=pantalla_conf.get("fg_color"),
        justify="right"
    )
    pantalla.pack(fill="x", padx=15, pady=20, ipady=10)
    pantalla.bind("<Key>", lambda e: "break")  # bloquear entrada por teclado

    # ---------------- Marco de botones ----------------
    marco_conf = estilos["marco"]
    frame = ctk.CTkFrame(root, fg_color=marco_conf.get("bg_color", "#f9f9f9"))
    frame.pack(expand=True, fill="both", padx=10, pady=10)

    # ---------------- Funciones de la calculadora ----------------
    def click_boton(valor_logico, valor_mostrar=None):

        if valor_mostrar is None:
            valor_mostrar = valor_logico
            
        # Mostrar en pantalla
        entrada.set(entrada.get() + valor_mostrar)
        
        # Guardar en la lógica
        expr_logica.set(expr_logica.get() + valor_logico)

    def borrar_todo():
        entrada.set("")
        expr_logica.set("")

    def borrar_uno():
        entrada.set(entrada.get()[:-1])
        expr_logica.set(expr_logica.get()[:-1])

    def calcular():
        expr = expr_logica.get()
        resultado = calculator.calculate(expr)
        entrada.set(resultado)
        expr_logica.set(str(resultado))
        
    def mostrar_historial():
        data = calculator.get_historial()
        ventana_historial = ctk.CTkToplevel(root)
        ventana_historial.title("Historial")
        ventana_historial.geometry("300x400")
        ventana_historial.transient(root)
        ventana_historial.grab_set()
        ventana_historial.focus_force()
        ventana_historial.configure(fg_color="#f9f9f9")

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

    # ---------------- Funciones de memoria ----------------
    def memoria_sumar():
        calculator.memory_add(expr_logica.get())

    def memoria_restar():
        calculator.memory_subtract(expr_logica.get())

    def memoria_recall():
        valor = calculator.memory_recall()
        entrada.set(str(valor))
        expr_logica.set(str(valor))

    def memoria_clear():
        calculator.memory_clear()

    # ---------------- Botones ----------------
    botones = [
        ("MC", memoria_clear), ("MR", memoria_recall), ("M+", memoria_sumar), ("M-", memoria_restar),
        ("Ac", borrar_todo), ("⌫", borrar_uno), ("÷", lambda: click_boton("/", "÷")), ("×", lambda: click_boton("*", "×")), ("%", lambda: click_boton("%")),
        ("7", lambda: click_boton("7")), ("8", lambda: click_boton("8")), ("9", lambda: click_boton("9")), ("-", lambda: click_boton("-")),
        ("4", lambda: click_boton("4")), ("5", lambda: click_boton("5")), ("6", lambda: click_boton("6")), ("+", lambda: click_boton("+")),
        ("1", lambda: click_boton("1")), ("2", lambda: click_boton("2")), ("3", lambda: click_boton("3")), ("=", calcular),
        ("0", lambda: click_boton("0")), (".", lambda: click_boton(".")), ("H", mostrar_historial)
    ]

    row, col = 0, 0
    for (text, cmd) in botones:
        if text in ["÷", "×", "-", "+", "%"]:
            tipo = "info"
        elif text == "=":
            tipo = "primary"
        elif text == "H":
            tipo = "success"
        elif text in ["MC", "MR", "M+", "M-"]:
            tipo = "emes"
        elif text in ["Ac", "⌫"]:
            tipo = "delete"
        else:
            tipo = "secondary"

        style = estilos[tipo]
        rs = 2 if text == "=" else 1

        base_color = style["fg_color"]
        hover_color = style["hover_color"]

        boton = ctk.CTkButton(
            frame,
            text=text,
            command=cmd,
            fg_color=base_color,
            text_color=style["text_color"],
            corner_radius=style.get("corner_radius", 20),
            font=tuple(style.get("font", ["Roboto", 20, "bold"]))
        )
        boton._current_color = base_color
        boton.grid(row=row, column=col, rowspan=rs, padx=5, pady=5, ipadx=10, ipady=10, sticky="nsew")

        boton.bind("<Enter>", lambda e, w=boton, h=hover_color: fade_color(w, h))
        boton.bind("<Leave>", lambda e, w=boton, b=base_color: fade_color(w, b))

        col += 1
        if col > 3:
            col = 0
            row += 1

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

