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
