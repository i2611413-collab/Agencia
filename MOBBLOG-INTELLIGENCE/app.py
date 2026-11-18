import os
from flask import Flask, jsonify, request, render_template
from agent import reply_to_message, calculate_score
from db import get_connection, init_check

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False


def json_error(message, status=400):
    return jsonify({"ok": False, "error": str(message)}), status


def db_rows(query, params=()):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/api/health")
def health():
    try:
        init_check()
        return jsonify({
            "ok": True,
            "service": "MOBBLOG INTELLIGENCE",
            "database": "connected"
        })
    except Exception as exc:
        app.logger.exception("Health check failed")
        return jsonify({
            "ok": False,
            "database": "unavailable",
            "detail": str(exc)
        }), 503


@app.get("/api/dashboard")
def dashboard():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) AS total FROM prospects")
                total = cur.fetchone()["total"]

                cur.execute(
                    "SELECT status, COUNT(*) AS total FROM prospects GROUP BY status"
                )
                statuses = cur.fetchall()

                cur.execute("SELECT COUNT(*) AS total FROM sales_outcomes WHERE converted = 1")
                won = cur.fetchone()["total"]

                cur.execute("SELECT COUNT(*) AS total FROM conversations")
                conversations = cur.fetchone()["total"]

                cur.execute("SELECT COUNT(*) AS total FROM proposals")
                proposals = cur.fetchone()["total"]

                cur.execute("""
                    SELECT prospect_id, full_name, business_name, business_sector,
                           status, created_at
                    FROM prospects
                    ORDER BY created_at DESC
                    LIMIT 8
                """)
                recent = cur.fetchall()

        return jsonify({
            "ok": True,
            "total_prospects": total,
            "won": won,
            "conversations": conversations,
            "proposals": proposals,
            "statuses": statuses,
            "recent_prospects": recent
        })
    except Exception as exc:
        app.logger.exception("Dashboard query failed")
        return json_error("No se pudo consultar el dashboard: " + str(exc), 503)


@app.get("/api/prospects")
def list_prospects():
    try:
        rows = db_rows("""
            SELECT prospect_id, full_name, email, phone, business_name,
                   business_sector, acquisition_channel, business_goal,
                   budget_range, digital_presence, status, created_at, updated_at
            FROM prospects
            ORDER BY created_at DESC
            LIMIT 250
        """)
        return jsonify({"ok": True, "prospects": rows})
    except Exception as exc:
        app.logger.exception("Prospect list failed")
        return json_error(exc, 503)


@app.post("/api/prospects")
def create_prospect():
    data = request.get_json(silent=True) or {}
    allowed = [
        "full_name", "email", "phone", "business_name", "business_sector",
        "acquisition_channel", "business_goal", "budget_range", "digital_presence"
    ]
    fields = [(key, data.get(key)) for key in allowed if data.get(key) not in (None, "")]
    if not fields:
        return json_error("Ingresa al menos un dato del prospecto.")

    try:
        columns = ", ".join(key for key, _ in fields)
        placeholders = ", ".join(["%s"] * len(fields))
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"INSERT INTO prospects ({columns}) VALUES ({placeholders})",
                    [value for _, value in fields]
                )
                prospect_id = cur.lastrowid
        return jsonify({"ok": True, "prospect_id": prospect_id}), 201
    except Exception as exc:
        app.logger.exception("Prospect creation failed")
        return json_error(exc, 503)


@app.patch("/api/prospects/<int:prospect_id>")
def update_prospect(prospect_id):
    data = request.get_json(silent=True) or {}
    allowed = [
        "full_name", "email", "phone", "business_name", "business_sector",
        "acquisition_channel", "business_goal", "budget_range",
        "digital_presence", "status"
    ]
    fields = [(key, data[key]) for key in allowed if key in data]
    if not fields:
        return json_error("No hay campos válidos para actualizar.")

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE prospects SET " +
                    ", ".join(f"{key}=%s" for key, _ in fields) +
                    " WHERE prospect_id=%s",
                    [value for _, value in fields] + [prospect_id]
                )
                if cur.rowcount == 0:
                    cur.execute(
                        "SELECT prospect_id FROM prospects WHERE prospect_id=%s",
                        (prospect_id,)
                    )
                    if not cur.fetchone():
                        return json_error("Prospecto no encontrado.", 404)
        return jsonify({"ok": True, "prospect_id": prospect_id})
    except Exception as exc:
        app.logger.exception("Prospect update failed")
        return json_error(exc, 503)


@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    if not message:
        return json_error("Escribe un mensaje.")

    prospect_id = data.get("prospect_id")
    conversation_id = data.get("conversation_id")

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                # 1. Recuperar o crear el prospecto.
                if prospect_id:
                    cur.execute(
                        "SELECT * FROM prospects WHERE prospect_id=%s",
                        (prospect_id,)
                    )
                    prospect = cur.fetchone()
                    if not prospect:
                        return json_error("Prospecto no encontrado.", 404)
                else:
                    cur.execute("""
                        INSERT INTO prospects (acquisition_channel, status)
                        VALUES ('web', 'new')
                    """)
                    prospect_id = cur.lastrowid
                    cur.execute(
                        "SELECT * FROM prospects WHERE prospect_id=%s",
                        (prospect_id,)
                    )
                    prospect = cur.fetchone()

                # 2. Recuperar o crear la conversación.
                if conversation_id:
                    cur.execute("""
                        SELECT conversation_id
                        FROM conversations
                        WHERE conversation_id=%s AND prospect_id=%s
                    """, (conversation_id, prospect_id))
                    if not cur.fetchone():
                        return json_error("Conversación no encontrada.", 404)
                else:
                    cur.execute("""
                        INSERT INTO conversations (prospect_id, channel)
                        VALUES (%s, 'web')
                    """, (prospect_id,))
                    conversation_id = cur.lastrowid

                # 3. Cargar contexto anterior ANTES de guardar el mensaje actual.
                cur.execute("""
                    SELECT role, message_text
                    FROM conversation_messages
                    WHERE conversation_id=%s
                    ORDER BY message_id DESC
                    LIMIT 20
                """, (conversation_id,))
                previous_messages = list(reversed(cur.fetchall()))
                history = [
                    {"role": row["role"], "content": row["message_text"]}
                    for row in previous_messages
                ]

                # 4. Guardar mensaje del usuario.
                cur.execute("""
                    INSERT INTO conversation_messages
                        (conversation_id, role, message_text)
                    VALUES (%s, 'user', %s)
                """, (conversation_id, message))

                # 5. Ejecutar el agente con los datos del prospecto y su historial.
                answer, extracted = reply_to_message(
                    message,
                    context={"prospect": prospect or {}, "history": history}
                )

                # 6. Persistir los campos detectados por el agente.
                valid_fields = {
                    "full_name", "email", "phone", "business_name",
                    "business_sector", "acquisition_channel", "business_goal",
                    "budget_range", "digital_presence"
                }
                updates = [
                    (key, value) for key, value in extracted.items()
                    if key in valid_fields and value not in (None, "")
                ]
                if updates:
                    cur.execute(
                        "UPDATE prospects SET " +
                        ", ".join(f"{key}=%s" for key, _ in updates) +
                        ", status='diagnosed' WHERE prospect_id=%s",
                        [value for _, value in updates] + [prospect_id]
                    )

                # 7. Guardar respuesta del agente.
                cur.execute("""
                    INSERT INTO conversation_messages
                        (conversation_id, role, message_text)
                    VALUES (%s, 'assistant', %s)
                """, (conversation_id, answer))

                # 8. Recuperar prospecto actualizado para calcular el scoring.
                cur.execute(
                    "SELECT * FROM prospects WHERE prospect_id=%s",
                    (prospect_id,)
                )
                updated_prospect = cur.fetchone()

        score, reasons = calculate_score(updated_prospect or {})
        return jsonify({
            "ok": True,
            "reply": answer,
            "prospect_id": prospect_id,
            "conversation_id": conversation_id,
            "score": score,
            "score_reasons": reasons
        })

    except Exception as exc:
        app.logger.exception("Chat processing failed")
        return json_error("No se pudo procesar el mensaje: " + str(exc), 503)


@app.get("/api/conversations")
def conversations():
    try:
        rows = db_rows("""
            SELECT c.conversation_id, c.prospect_id, c.channel, c.started_at,
                   c.ended_at, p.full_name, p.business_name
            FROM conversations c
            JOIN prospects p ON p.prospect_id = c.prospect_id
            ORDER BY c.started_at DESC
            LIMIT 100
        """)
        return jsonify({"ok": True, "conversations": rows})
    except Exception as exc:
        app.logger.exception("Conversation list failed")
        return json_error(exc, 503)


@app.get("/api/conversations/<int:conversation_id>/messages")
def conversation_messages(conversation_id):
    try:
        rows = db_rows("""
            SELECT message_id, conversation_id, role, message_text, created_at
            FROM conversation_messages
            WHERE conversation_id=%s
            ORDER BY message_id ASC
        """, (conversation_id,))
        return jsonify({"ok": True, "messages": rows})
    except Exception as exc:
        app.logger.exception("Conversation messages failed")
        return json_error(exc, 503)


@app.get("/api/proposals")
def proposals():
    try:
        rows = db_rows("""
            SELECT pr.*, p.full_name, p.business_name
            FROM proposals pr
            JOIN prospects p ON p.prospect_id = pr.prospect_id
            ORDER BY pr.created_at DESC
            LIMIT 100
        """)
        return jsonify({"ok": True, "proposals": rows})
    except Exception as exc:
        app.logger.exception("Proposal list failed")
        return json_error(exc, 503)


@app.post("/api/proposals")
def create_proposal():
    data = request.get_json(silent=True) or {}
    prospect_id = data.get("prospect_id")
    if not prospect_id:
        return json_error("prospect_id es obligatorio.")

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT prospect_id FROM prospects WHERE prospect_id=%s",
                    (prospect_id,)
                )
                if not cur.fetchone():
                    return json_error("Prospecto no encontrado.", 404)

                cur.execute("""
                    INSERT INTO proposals
                        (prospect_id, proposal_summary, proposed_amount,
                         currency, proposal_status)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    prospect_id,
                    data.get("proposal_summary"),
                    data.get("proposed_amount"),
                    data.get("currency", "PEN"),
                    data.get("proposal_status", "draft")
                ))
                proposal_id = cur.lastrowid

        return jsonify({"ok": True, "proposal_id": proposal_id}), 201
    except Exception as exc:
        app.logger.exception("Proposal creation failed")
        return json_error(exc, 503)


@app.get("/api/scoring/<int:prospect_id>")
def scoring(prospect_id):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT full_name, email, phone, business_name, business_sector,
                           business_goal, budget_range, digital_presence,
                           acquisition_channel, status
                    FROM prospects
                    WHERE prospect_id=%s
                """, (prospect_id,))
                prospect = cur.fetchone()

        if not prospect:
            return json_error("Prospecto no encontrado.", 404)

        score, reasons = calculate_score(prospect)
        return jsonify({
            "ok": True,
            "prospect_id": prospect_id,
            "score": score,
            "reasons": reasons,
            "method": "heurística comercial; no es una probabilidad ML"
        })
    except Exception as exc:
        app.logger.exception("Scoring failed")
        return json_error(exc, 503)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
