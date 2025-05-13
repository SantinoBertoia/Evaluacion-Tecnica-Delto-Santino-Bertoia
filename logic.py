def calculate_loan(monto, plazo, interacciones=0):
    """
    Calcula un préstamo con sus detalles

    Args:
        monto: Monto solicitado
        plazo: Plazo en meses
        interacciones: Número de interacciones del usuario (para ajustar tasa)

    Returns:
        dict: Diccionario con detalles del préstamo
    """
    # Base: 55% TEA (Tasa Efectiva Anual)
    # Ajustamos según perfil (interacciones como proxy de fidelidad)
    tasa_base = 55.0

    # Ajuste por fidelidad (máximo 10% de descuento)
    descuento = min(interacciones * 0.5, 10.0)
    tasa_final = tasa_base - descuento

    # Convertir TEA a TEM (Tasa Efectiva Mensual)
    tem = ((1 + tasa_final / 100) ** (1 / 12) - 1) * 100

    # Calcular cuota mensual - Fórmula de amortización
    tem_decimal = tem / 100
    cuota = monto * (tem_decimal * (1 + tem_decimal) **
                     plazo) / ((1 + tem_decimal) ** plazo - 1)

    # Total a pagar
    total = cuota * plazo

    return {
        "monto": monto,
        "plazo": plazo,
        "tasa_anual": round(tasa_final, 2),
        "tasa_mensual": round(tem, 2),
        "cuota_mensual": round(cuota, 2),
        "total": round(total, 2)
    }


def format_currency(amount):
    """Formatea un número como moneda (pesos argentinos)"""
    return f"$ {amount:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
