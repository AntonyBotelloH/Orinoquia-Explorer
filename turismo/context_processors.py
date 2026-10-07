from .clima import obtener_clima_actual, obtener_clima_mes_actual

def clima_context(request):
    """
    Inyecta datos del clima en vivo y el clima estacional del mes
    en todas las plantillas que renderizan el contexto de la aplicación.
    """
    try:
        clima_live = obtener_clima_actual()
        clima_mensual = obtener_clima_mes_actual()
        return {
            'clima_actual': clima_live,
            'clima_mes': clima_mensual,
        }
    except Exception:
        return {
            'clima_actual': None,
            'clima_mes': None,
        }
