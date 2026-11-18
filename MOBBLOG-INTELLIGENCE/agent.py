import re

def calculate_score(p):
    score, reasons = 0, []
    if p.get("full_name"):
        score += 10; reasons.append("Tiene nombre de contacto (+10)")
    if p.get("email") or p.get("phone"):
        score += 20; reasons.append("Tiene un medio de contacto (+20)")
    if p.get("business_name"):
        score += 15; reasons.append("Identificó su negocio (+15)")
    if p.get("business_goal"):
        score += 20; reasons.append("Expresó un objetivo comercial (+20)")
    if p.get("budget_range"):
        score += 15; reasons.append("Compartió un rango de presupuesto (+15)")
    if p.get("digital_presence"):
        score += 10; reasons.append("Describió su presencia digital (+10)")
    if p.get("business_sector"):
        score += 10; reasons.append("Identificó su sector (+10)")
    return min(score, 100), reasons

def reply_to_message(message):
    text = message.strip()
    low = text.lower()
    extracted = {}
    email = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', text)
    phone = re.search(r'(?<!\w)(?:\+?51[\s-]?)?(?:9\d{8}|\d{7,9})(?!\w)', text)
    if email: extracted["email"] = email.group(0)
    if phone: extracted["phone"] = phone.group(0)
    if any(x in low for x in ["hola", "buenas", "buenos días", "buenas tardes"]):
        answer = ("¡Hola! Soy el asistente comercial de MOBBLOG Digital. "
                  "Puedo orientarte sobre páginas web, presencia digital y captación de clientes. "
                  "¿Cómo se llama tu negocio y qué te gustaría conseguir?")
    elif any(x in low for x in ["399", "xw4"]):
        answer = ("XW4 es nuestra landing page de 4 secciones, desde S/399. "
                  "¿Me cuentas qué negocio tienes y qué objetivo buscas?")
    elif any(x in low for x in ["650", "xw6"]):
        answer = ("XW6 es nuestra landing page de 6 secciones, desde S/650. "
                  "¿Qué productos o servicios necesitas presentar?")
    elif "xw+" in low or "web comercial" in low or "sitio web" in low:
        answer = ("XW+ corresponde a un sitio web comercial completo y se cotiza según el alcance. "
                  "¿Qué funcionalidades necesitas?")
    elif any(x in low for x in ["google ads", "publicidad", "anuncios"]):
        answer = ("Podemos evaluar campañas de Google Ads y una estrategia de captación. "
                  "Para orientarte bien, ¿qué producto o servicio quieres promocionar y en qué zona?")
    elif email or phone:
        answer = ("Gracias, ya registré el dato de contacto en esta conversación. "
                  "¿Cuál es el nombre de tu negocio y qué necesitas mejorar primero?")
    else:
        answer = ("Entiendo. Para recomendarte una solución adecuada necesito conocer tres cosas: "
                  "qué negocio tienes, qué objetivo comercial buscas y si ya cuentas con una web o redes sociales. "
                  "También puedes preguntarme por XW4 (S/399), XW6 (S/650) o XW+ (cotización).")
    return answer, extracted
