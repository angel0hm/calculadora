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
