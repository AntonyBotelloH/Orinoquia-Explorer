import json
import urllib.request
from datetime import datetime, date
from django.core.cache import cache

# Coordenadas geográficas representativas de los Llanos Orientales (Villavicencio / Meta)
LAT_LLANOS = 4.1420
LON_LLANOS = -73.6266

# Códigos meteorológicos WMO (World Meteorological Organization)
WMO_CODES = {
    0: ("Cielo despejado", "bi-sun-fill", "text-warning"),
    1: ("Mayormente despejado", "bi-brightness-high-fill", "text-warning"),
    2: ("Parcialmente nublado", "bi-cloud-sun-fill", "text-warning"),
    3: ("Nublado", "bi-cloud-fill", "text-secondary"),
    45: ("Neblina en la sabana", "bi-cloud-fog2-fill", "text-secondary"),
    48: ("Niebla húmeda", "bi-cloud-fog-fill", "text-secondary"),
    51: ("Llovizna ligera", "bi-cloud-drizzle-fill", "text-info"),
    53: ("Llovizna moderada", "bi-cloud-drizzle-fill", "text-info"),
    55: ("Llovizna densa", "bi-cloud-rain-fill", "text-info"),
    61: ("Lluvia ligera", "bi-cloud-rain-fill", "text-info"),
    63: ("Lluvia moderada", "bi-cloud-rain-heavy-fill", "text-primary"),
    65: ("Lluvia torrencial", "bi-cloud-rain-heavy-fill", "text-primary"),
    80: ("Chubascos ligeros", "bi-cloud-rain-fill", "text-info"),
    81: ("Chubascos moderados", "bi-cloud-rain-heavy-fill", "text-primary"),
    82: ("Aguacero llanero fuerte", "bi-cloud-lightning-rain-fill", "text-danger"),
    95: ("Tormenta eléctrica llanera", "bi-cloud-lightning-fill", "text-warning"),
    96: ("Tormenta eléctrica con granizo", "bi-cloud-lightning-fill", "text-danger"),
    99: ("Tormenta severa", "bi-cloud-lightning-rain-fill", "text-danger"),
}

# Perfil bioclimático y estacional mensual de la Orinoquía colombiana
CLIMA_MENSUAL = {
    1: {
        "mes": "Enero",
        "temporada": "Verano Llanero (Época Seca)",
        "rango_temp": "24°C - 34°C",
        "precipitacion": "Muy baja (15-30 mm)",
        "descripcion": "Cielos abiertos, brisa constante y esteros concentrados.",
        "recomendacion": "Temporada cumbre para safaris fotográficos en Hato La Aurora, avistamiento de chigüiros, osos y aves.",
        "icono": "bi-sun-fill",
        "icono_color": "text-warning",
        "badge_color": "bg-warning text-dark"
    },
    2: {
        "mes": "Febrero",
        "temporada": "Verano Llanero (Plena Sequía)",
        "rango_temp": "25°C - 35°C",
        "precipitacion": "Mínima (10-25 mm)",
        "descripcion": "Máxima concentración de fauna en bebederos y atardeceres rojizos.",
        "recomendacion": "Ideal para aviturismo masivo, cabalgatas sabaneras extensas y festivales folclóricos.",
        "icono": "bi-brightness-high-fill",
        "icono_color": "text-warning",
        "badge_color": "bg-warning text-dark"
    },
    3: {
        "mes": "Marzo",
        "temporada": "Transición Verano - Invierno",
        "rango_temp": "24°C - 33°C",
        "precipitacion": "Baja a moderada",
        "descripcion": "Comienzan las primeras lluvias refrescantes sobre la sabana.",
        "recomendacion": "Excelente para safaris mixtos, turismo de hacienda y navegación en ríos caudalosos.",
        "icono": "bi-cloud-sun-fill",
        "icono_color": "text-warning",
        "badge_color": "bg-warning text-dark"
    },
    4: {
        "mes": "Abril",
        "temporada": "Invierno Llanero (Inicio de Lluvias)",
        "rango_temp": "23°C - 31°C",
        "precipitacion": "Alta (200-350 mm)",
        "descripcion": "El llano florece con un verde intenso y los caños aumentan su caudal.",
        "recomendacion": "Apertura de temporada de rafting en el Río Güejar y senderismo en serranías.",
        "icono": "bi-cloud-rain-fill",
        "icono_color": "text-info",
        "badge_color": "bg-success text-white"
    },
    5: {
        "mes": "Mayo",
        "temporada": "Invierno Llanero (Sabana Verde)",
        "rango_temp": "23°C - 30°C",
        "precipitacion": "Muy alta (350-450 mm)",
        "descripcion": "Morichales en su máximo esplendor, ríos navegables con rápidos emocionantes.",
        "recomendacion": "Excelente para deportes de aventura fluvial, avistamiento de toninas y cascadas.",
        "icono": "bi-water",
        "icono_color": "text-primary",
        "badge_color": "bg-success text-white"
    },
    6: {
        "mes": "Junio",
        "temporada": "Invierno Llanero (Apertura Caño Cristales)",
        "rango_temp": "22°C - 29°C",
        "precipitacion": "Alta (300-400 mm)",
        "descripcion": "Apertura oficial de Caño Cristales: la Macarenia clavigera comienza a vestirse de colores.",
        "recomendacion": "Temporada imperdible para Caño Cristales, travesías 4x4 y cascadas de Mesetas.",
        "icono": "bi-rainbow",
        "icono_color": "text-danger",
        "badge_color": "bg-info text-dark"
    },
    7: {
        "mes": "Julio",
        "temporada": "Invierno Llanero (Pico de Caño Cristales)",
        "rango_temp": "22°C - 29°C",
        "precipitacion": "Alta (300-380 mm)",
        "descripcion": "Caño Cristales en su mayor colorido. Sabanas navegables en canoa y curiara.",
        "recomendacion": "Época dorada para fotografía de naturaleza, expedición Caño Cristales y pesca deportiva con devolución.",
        "icono": "bi-palette-fill",
        "icono_color": "text-danger",
        "badge_color": "bg-info text-dark"
    },
    8: {
        "mes": "Agosto",
        "temporada": "Invierno Llanero (Veranillo de San Juan)",
        "rango_temp": "23°C - 30°C",
        "precipitacion": "Moderada a alta",
        "descripcion": "Período con días intercalados de sol radiante y lluvias dispersas.",
        "recomendacion": "Condiciones óptimas para combinar rafting, Caño Cristales y avistamiento de fauna.",
        "icono": "bi-cloud-sun-fill",
        "icono_color": "text-warning",
        "badge_color": "bg-success text-white"
    },
    9: {
        "mes": "Septiembre",
        "temporada": "Invierno Llanero (Aguas Altas)",
        "rango_temp": "23°C - 31°C",
        "precipitacion": "Moderada (250-320 mm)",
        "descripcion": "Gran riqueza biológica en caños y lagunas. Formaciones nubosas espectaculares.",
        "recomendacion": "Ideal para avistamiento de aves acuáticas, toninas en Puerto Gaitán y Caño Cristales.",
        "icono": "bi-compass-fill",
        "icono_color": "text-primary",
        "badge_color": "bg-success text-white"
    },
    10: {
        "mes": "Octubre",
        "temporada": "Invierno Llanero (Últimas Grandes Lluvias)",
        "rango_temp": "23°C - 31°C",
        "precipitacion": "Moderada (200-280 mm)",
        "descripcion": "Caudales en nivel óptimo para ecoturismo, vegetación tupida y morichales exuberantes.",
        "recomendacion": "Excelente para visitas a reservas naturales, aviturismo y rafting de aventura.",
        "icono": "bi-tree-fill",
        "icono_color": "text-success",
        "badge_color": "bg-success text-white"
    },
    11: {
        "mes": "Noviembre",
        "temporada": "Retirada de Aguas (Transición al Verano)",
        "rango_temp": "24°C - 32°C",
        "precipitacion": "Baja a moderada",
        "descripcion": "Las aguas descienden y la fauna silvestre comienza a agruparse en sabanas secas.",
        "recomendacion": "Últimas semanas de Caño Cristales. Inician condiciones excelentes para safaris terrestres.",
        "icono": "bi-sunset-fill",
        "icono_color": "text-warning",
        "badge_color": "bg-warning text-dark"
    },
    12: {
        "mes": "Diciembre",
        "temporada": "Verano Llanero (Inicio de Temporada Alta)",
        "rango_temp": "24°C - 33°C",
        "precipitacion": "Baja (30-60 mm)",
        "descripcion": "Comienza el verano llanero con brisas secas, cielos estrellados y parrandos navideños.",
        "recomendacion": "Temporada alta para cabalgatas, safaris, rutas del joropo y gastronomía de ternera a la llanera.",
        "icono": "bi-sun-fill",
        "icono_color": "text-warning",
        "badge_color": "bg-warning text-dark"
    }
}

def obtener_clima_mes_actual():
    """Retorna la ficha climática estacional del mes en curso."""
    mes_actual = datetime.now().month
    return CLIMA_MENSUAL.get(mes_actual, CLIMA_MENSUAL[1])


def obtener_clima_actual():
    """
    Consulta el clima en tiempo real desde la API de Open-Meteo para los Llanos Orientales.
    Utiliza caché de Django (30 minutos) para máxima velocidad y evitar peticiones excesivas.
    Si la API falla, utiliza como respaldo el perfil estacional del mes actual.
    """
    cache_key = "clima_llanos_tiempo_real"
    clima_cached = cache.get(cache_key)
    if clima_cached:
        return clima_cached

    clima_mes = obtener_clima_mes_actual()
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={LAT_LLANOS}&longitude={LON_LLANOS}"
        f"&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m"
        f"&timezone=America%2FBogota"
    )

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "OrinoquiaExplorer/1.0"})
        with urllib.request.urlopen(req, timeout=4) as response:
            data = json.loads(response.read().decode("utf-8"))
            current = data.get("current", {})
            
            temp = round(current.get("temperature_2m", 28.0))
            humedad = round(current.get("relative_humidity_2m", 75))
            viento = round(current.get("wind_speed_10m", 10.0))
            wmo = current.get("weather_code", 1)
            
            condicion, icono, icono_color = WMO_CODES.get(wmo, ("Buen tiempo en sabana", "bi-sun-fill", "text-warning"))

            resultado = {
                "temperatura": temp,
                "humedad": humedad,
                "viento": viento,
                "condicion": condicion,
                "icono": icono,
                "icono_color": icono_color,
                "origen": "en_vivo",
                "mes_info": clima_mes,
                "actualizado": datetime.now().strftime("%H:%M")
            }
            # Guardar en caché por 30 minutos (1800 segundos)
            cache.set(cache_key, resultado, 1800)
            return resultado

    except Exception:
        # Respaldo robusto con el modelo climático estacional
        resultado = {
            "temperatura": 28,
            "humedad": 75,
            "viento": 12,
            "condicion": clima_mes["descripcion"],
            "icono": clima_mes["icono"],
            "icono_color": clima_mes["icono_color"],
            "origen": "estacional",
            "mes_info": clima_mes,
            "actualizado": datetime.now().strftime("%H:%M")
        }
        cache.set(cache_key, resultado, 600)
        return resultado


def consultar_pronostico_fecha(fecha_objetivo):
    """
    Dada una fecha (cadena YYYY-MM-DD o date), consulta el pronóstico meteorológico
    para esa fecha exacta (si está dentro de la ventana de 14 días de Open-Meteo)
    o el perfil climático estacional para ese mes en los Llanos Orientales.
    """
    if isinstance(fecha_objetivo, str):
        try:
            fecha_dt = datetime.strptime(fecha_objetivo, "%Y-%m-%d").date()
        except ValueError:
            return {"valido": False, "error": "Formato de fecha inválido"}
    elif isinstance(fecha_objetivo, date):
        fecha_dt = fecha_objetivo
    else:
        return {"valido": False, "error": "Tipo de fecha no compatible"}

    hoy = date.today()
    dias_diferencia = (fecha_dt - hoy).days
    mes = fecha_dt.month
    info_mes = CLIMA_MENSUAL.get(mes, CLIMA_MENSUAL[1])

    # Si la fecha está en el rango de pronóstico de Open-Meteo (0 a 14 días futuros)
    if 0 <= dias_diferencia <= 14:
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={LAT_LLANOS}&longitude={LON_LLANOS}"
            f"&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max"
            f"&timezone=America%2FBogota"
        )
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "OrinoquiaExplorer/1.0"})
            with urllib.request.urlopen(req, timeout=4) as response:
                data = json.loads(response.read().decode("utf-8"))
                daily = data.get("daily", {})
                times = daily.get("time", [])
                
                fecha_str = fecha_dt.strftime("%Y-%m-%d")
                if fecha_str in times:
                    idx = times.index(fecha_str)
                    wmo = daily.get("weather_code", [])[idx]
                    t_max = round(daily.get("temperature_2m_max", [])[idx])
                    t_min = round(daily.get("temperature_2m_min", [])[idx])
                    prob_lluvia = daily.get("precipitation_probability_max", [])[idx]
                    
                    condicion, icono, icono_color = WMO_CODES.get(wmo, ("Buen tiempo", "bi-sun-fill", "text-warning"))

                    return {
                        "valido": True,
                        "tipo": "pronostico_en_vivo",
                        "fecha": fecha_str,
                        "temperatura": f"{t_max}°C",
                        "temperatura_min": f"{t_min}°C",
                        "rango": f"{t_min}°C a {t_max}°C",
                        "probabilidad_lluvia": f"{prob_lluvia}%" if prob_lluvia is not None else "Baja",
                        "condicion": condicion,
                        "icono": icono,
                        "icono_color": icono_color,
                        "temporada": info_mes["temporada"],
                        "mes": info_mes["mes"],
                        "recomendacion": info_mes["recomendacion"],
                        "es_pronostico_preciso": True,
                        "alerta_lluvia": prob_lluvia > 50 if prob_lluvia is not None else False
                    }
        except Exception:
            pass

    # Si la fecha es posterior a 14 días o la API no respondió, usamos el modelo estacional
    return {
        "valido": True,
        "tipo": "modelo_estacional",
        "fecha": fecha_dt.strftime("%Y-%m-%d"),
        "temperatura": f"Promedio {info_mes['rango_temp']}",
        "rango": info_mes["rango_temp"],
        "probabilidad_lluvia": info_mes["precipitacion"],
        "condicion": info_mes["descripcion"],
        "icono": info_mes["icono"],
        "icono_color": info_mes["icono_color"],
        "temporada": info_mes["temporada"],
        "mes": info_mes["mes"],
        "recomendacion": info_mes["recomendacion"],
        "es_pronostico_preciso": False,
        "alerta_lluvia": "Alta" in info_mes["precipitacion"]
    }
