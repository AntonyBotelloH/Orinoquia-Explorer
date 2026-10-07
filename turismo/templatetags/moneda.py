from django import template
from decimal import Decimal

register = template.Library()

@register.filter(name='moneda_cop')
def moneda_cop(valor):
    """
    Formatea un número con puntos de miles y sin decimales para pesos colombianos (COP).
    Ejemplo: 150000 -> 150.000, 1500000.00 -> 1.500.000
    """
    if valor is None or valor == '':
        return '0'
    try:
        # Convertir a float y luego redondear a entero
        numero = int(round(float(valor)))
        return f"{numero:,}".replace(",", ".")
    except (ValueError, TypeError):
        return str(valor)

@register.filter(name='precio_cop')
def precio_cop(valor):
    """
    Formatea un número con signo de pesos, puntos de miles y sin decimales.
    Ejemplo: 150000 -> $ 150.000
    """
    return f"${moneda_cop(valor)}"

@register.filter(name='puntos_miles')
def puntos_miles(valor):
    """
    Alias amigable para separación de miles con punto.
    """
    return moneda_cop(valor)
