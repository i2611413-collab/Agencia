"""
MOBBLOG INTELLIGENCE - Agente comercial contextual v2
Motor determinístico por etapas. No es IA generativa ni predice probabilidad de compra.
API: answer, extracted = reply_to_message(message, context=None)
context opcional: {"prospect": {...}, "history": [{"role":"user","content":"..."}]}
"""
import re
import unicodedata

SERVICES = {
    "XW4": ("Landing page de 4 secciones", "S/399"),
    "XW6": ("Landing page de 6 secciones", "S/650"),
    "XW+": ("Sitio web comercial completo", "cotización según alcance"),
}


def norm(value):
    value = str(value or "").lower().strip()
    value = unicodedata.normalize("NFD", value)
    value = "".join(c for c in value if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", value)


def extract_fields(message):
    text, low, data = str(message or "").strip(), norm(message), {}
    email = re.search(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+", text)
    phone = re.search(r"(?<!\w)(?:\+?51[\s-]?)?(?:9\d{8}|\d{7,9})(?!\w)", text)
    if email:
        data["email"] = email.group(0)
    if phone:
        data["phone"] = phone.group(0).strip()

    sectors = {
        "cevichería": ["cevicheria", "ceviche"],
        "restaurante": ["restaurante", "polleria", "comida"],
        "salón de belleza": ["salon de belleza", "peluqueria", "estetica"],
        "inmobiliaria": ["inmobiliaria", "bienes raices"],
        "tienda / comercio": ["tienda", "bodega", "minimarket", "comercio"],
        "servicios profesionales": ["abogado", "contador", "consultor", "asesoria"],
        "salud": ["clinica", "consultorio", "odontologia", "dentista"],
        "educación": ["colegio", "academia", "instituto", "escuela"],
        "turismo": ["hotel", "hospedaje", "turismo"],
        "automotriz": ["taller mecanico", "mecanica", "autos", "repuestos"],
    }
    for sector, words in sectors.items():
        if any(norm(w) in low for w in words):
            data["business_sector"] = sector
            break

    goals = [
        (["aumentar mis ventas", "aumentar ventas", "vender mas", "mas ventas"], "Aumentar ventas"),
        (["conseguir clientes", "captar clientes", "atraer clientes", "mas clientes"], "Conseguir más clientes"),
        (["dar a conocer", "visibilidad", "posicionar"], "Mejorar visibilidad y posicionamiento"),
        (["recibir consultas", "generar consultas", "generar contactos"], "Generar consultas y contactos"),
        (["vender por internet", "tienda virtual", "ecommerce"], "Vender por internet"),
        (["mostrar mis productos", "mostrar mis servicios"], "Presentar productos o servicios"),
    ]
    for phrases, goal in goals:
        if any(norm(p) in low for p in phrases):
            data["business_goal"] = goal
            break

    if any(norm(x) in low for x in [
        "no cuento con redes", "no tengo redes", "no tengo pagina", "no cuento con pagina",
        "no tengo web", "no cuento con web", "no tengo presencia digital", "ninguna red"
    ]):
        data["digital_presence"] = "No cuenta con presencia digital propia"
    else:
        web = any(x in low for x in ["tengo web", "pagina web", "sitio web", "mi web"])
        social = any(x in low for x in ["facebook", "instagram", "tiktok", "redes sociales"])
        if web and social:
            data["digital_presence"] = "Cuenta con página web y redes sociales"
        elif web:
            data["digital_presence"] = "Cuenta con página web"
        elif social:
            data["digital_presence"] = "Cuenta con redes sociales"

    if any(x in low for x in ["sin presupuesto", "no tengo presupuesto"]):
        data["budget_range"] = "Aún no definido"
    else:
        amount = re.search(r"(?:s/\.?\s*)?(\d{2,6})(?:\s*(?:soles|sol|s/))?", low)
        if amount:
            data["budget_range"] = "S/ " + amount.group(1)
        elif any(x in low for x in ["presupuesto bajo", "presupuesto limitado"]):
            data["budget_range"] = "Presupuesto limitado"
        elif "presupuesto moderado" in low:
            data["budget_range"] = "Presupuesto moderado"

    name = re.search(
        r"(?:mi negocio se llama|el negocio se llama|se llama|me llamo|soy)\s+([A-ZÁÉÍÓÚÑ][\wÁÉÍÓÚÑáéíóúñ&.' -]{1,45})",
        text, re.I
    )
    if name:
        data["full_name"] = name.group(1).strip(" .,!?:;")
    return data


def calculate_score(prospect):
    score, reasons = 0, []
    checks = [
        ("full_name", 10, "Tiene nombre de contacto"),
        ("email_or_phone", 20, "Tiene un medio de contacto"),
        ("business_identity", 15, "Identificó su negocio o sector"),
        ("business_goal", 20, "Expresó un objetivo comercial"),
        ("budget_range", 15, "Compartió información de presupuesto"),
        ("digital_presence", 10, "Describió su presencia digital"),
        ("acquisition_channel", 5, "Se identificó el canal de captación"),
    ]
    for key, points, label in checks:
        present = bool(prospect.get(key))
        if key == "email_or_phone":
            present = bool(prospect.get("email") or prospect.get("phone"))
        elif key == "business_identity":
            present = bool(prospect.get("business_name") or prospect.get("business_sector"))
        if present:
            score += points
            reasons.append(f"{label} (+{points})")
    return min(score, 100), reasons


def _next_stage(p):
    if not (p.get("business_name") or p.get("business_sector")):
        return "business"
    if not p.get("business_goal"):
        return "goal"
    if not p.get("digital_presence"):
        return "presence"
    if not p.get("budget_range"):
        return "budget"
    if not (p.get("email") or p.get("phone")):
        return "contact"
    return "recommendation"


def _recommend(p):
    goal, presence, sector = norm(p.get("business_goal")), norm(p.get("digital_presence")), norm(p.get("business_sector"))
    if "vender por internet" in goal or "presentar productos" in goal or sector in ("restaurante", "cevichería", "tienda / comercio"):
        service = "XW6"
    elif "no cuenta" in presence or "no tiene" in presence:
        service = "XW4"
    else:
        service = "XW4"
    title, price = SERVICES[service]
    score, _ = calculate_score(p)
    return (
        f"Con la información que me compartiste, mi recomendación inicial es {service}: {title}, {price}. "
        f"El objetivo es {p.get('business_goal', 'por definir').lower()}. "
        f"Tu negocio corresponde al rubro {p.get('business_sector', 'por precisar')}; "
        f"tu presencia digital: {p.get('digital_presence', 'por precisar')}. "
        f"Nivel de información comercial recopilada: {score}/100. "
        "Este puntaje mide la información disponible, no la probabilidad de compra. "
        "¿Quieres que prepare una propuesta con el alcance recomendado?"
    )


def reply_to_message(message, context=None):
    text = str(message or "").strip()
    if not text:
        return "Cuéntame qué negocio tienes y qué te gustaría conseguir.", {}

    context = context or {}
    prospect = dict(context.get("prospect") or {})
    history = context.get("history") or []

    # Recupera datos de mensajes anteriores del usuario si el controlador entrega historial.
    previous = " ".join(
        str(m.get("content", "")) for m in history
        if isinstance(m, dict) and m.get("role") == "user"
    )
    extracted = extract_fields(text)
    combined_fields = extract_fields(previous + " " + text)
    for key, value in combined_fields.items():
        if value and not prospect.get(key):
            prospect[key] = value

    low = norm(text)
    if any(x in low for x in ["precio", "cuanto cuesta", "cuanto vale"]):
        if "xw6" in low or "650" in low:
            return "XW6 es una landing page de 6 secciones y cuesta S/650. ¿Qué negocio necesitas presentar?", extracted
        if "xw+" in low:
            return "XW+ es un sitio web comercial completo; se cotiza según el alcance y las funcionalidades.", extracted
        return "Tenemos XW4 (4 secciones) desde S/399, XW6 (6 secciones) a S/650 y XW+ (sitio comercial completo) por cotización. ¿Qué necesitas que haga tu web?", extracted

    if any(x in low for x in ["hola", "buenas", "buenos dias", "buenas tardes"]) and len(low.split()) <= 5:
        return "¡Hola! Soy el asistente comercial de MOBBLOG Digital. Te ayudaré a encontrar una solución web para tu negocio. ¿Qué tipo de negocio tienes y cómo se llama?", extracted

    stage = _next_stage(prospect)
    questions = {
        "business": "Para empezar, ¿qué tipo de negocio tienes y cómo se llama?",
        "goal": "Entendido. ¿Qué resultado buscas principalmente: aumentar ventas, conseguir clientes, recibir consultas o mostrar mejor tus productos y servicios?",
        "presence": "¿Actualmente tienes página web, Facebook, Instagram u otras redes, o todavía no tienes presencia digital?",
        "budget": "¿Tienes un presupuesto aproximado para desarrollar tu presencia digital? Puede ser un rango o podemos dejarlo por definir.",
        "contact": "Para enviarte una recomendación y dar seguimiento, ¿me compartes tu nombre y un medio de contacto (correo o WhatsApp)?",
    }
    if stage == "recommendation":
        return _recommend(prospect), extracted

    intro = ""
    if stage == "goal" and prospect.get("business_sector"):
        intro = f"Entendido, un negocio del rubro {prospect['business_sector']}. "
    elif stage == "presence" and prospect.get("business_goal"):
        intro = f"Bien, tu objetivo es {prospect['business_goal'].lower()}. "
    elif stage == "budget":
        intro = "Ya tengo claro el negocio, el objetivo y tu situación digital. "
    elif stage == "contact":
        intro = "Con esos datos ya puedo orientarte. "
    return intro + questions[stage], extracted
