# ---------------- Lógica de la calculadora ----------------

historial = []


def add_to_expression(expr, value):
    """Agrega un valor a la expresión"""
    return expr + str(value)


def clear_all():
    """Borra todo el contenido"""
    return ""


def clear_one(expr):
    """Borra el último carácter"""
    return expr[:-1]


def calculate(expr):
    """Evalúa la expresión y guarda en historial"""
    global historial
    try:
        result = float(eval(expr))
        result_formatted = "{:.2f}".format(result) 
        historial.append(expr + " = " + result_formatted)
        return result_formatted
    except ZeroDivisionError:
        return "Error: ÷0"
    except Exception:
        return "Error"


def get_historial():
    """Devuelve el historial de operaciones"""
    return historial

# ---------------- Memoria ----------------
def memory_clear():
    """Limpia la memoria"""
    global memoria
    memoria = 0.0


def memory_recall():
    """Devuelve el valor almacenado"""
    return memoria


def memory_add(value):
    """Suma a la memoria"""
    global memoria
    try:
        memoria += float(value)
    except:
        pass


def memory_subtract(value):
    """Resta de la memoria"""
    global memoria
    try:
        memoria -= float(value)
    except:
        pass
