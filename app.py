"""
Paper Trading Demo · backend
-----------------------------
Pequeño servidor Flask que pide precios REALES (con retardo) a Yahoo Finance
usando la libreria yfinance, y se los sirve al frontend.

El frontend NUNCA llama a Yahoo directamente: lo hace este backend. Asi se
evita el problema de CORS y, si algun dia usaras una API con clave, la clave
se quedaria aqui en el servidor y no a la vista del usuario.

Aviso honesto: Yahoo Finance no es una API oficial. Funciona, pero puede
fallar o cambiar sin avisar, y los datos suelen ir con retardo (no es tiempo
real puro). Para aprender es mas que suficiente. No es asesoramiento.
"""

from flask import Flask, jsonify, request, render_template

try:
    import yfinance as yf
except ImportError:  # pragma: no cover
    raise SystemExit(
        "Falta yfinance. Instala las dependencias con:  pip install -r requirements.txt"
    )

app = Flask(__name__)

# Tickers por defecto: todos cotizan en EUR (Xetra / Amsterdam) para que el
# saldo de 100 EUR tenga sentido. Puedes anadir/quitar desde la interfaz.
DEFAULT_SYMBOLS = [
    "SAP.DE",    # SAP
    "ALV.DE",    # Allianz
    "SIE.DE",    # Siemens
    "BMW.DE",    # BMW
    "VOW3.DE",   # Volkswagen
    "EUNL.DE",   # iShares Core MSCI World (ETF)
]


def _get(fast_info, *names):
    """Lee un campo de fast_info tolerando distintas versiones de yfinance."""
    for n in names:
        try:
            v = getattr(fast_info, n)
            if v is not None:
                return v
        except Exception:
            pass
        try:
            v = fast_info[n]
            if v is not None:
                return v
        except Exception:
            pass
    return None


def fetch_quote(symbol):
    symbol = symbol.strip().upper()
    if not symbol:
        return None
    ticker = yf.Ticker(symbol)
    fi = ticker.fast_info
    price = _get(fi, "last_price", "lastPrice")
    prev = _get(fi, "previous_close", "previousClose")
    currency = _get(fi, "currency") or "?"
    name = symbol
    try:
        # get_info() puede ser lento; lo intentamos pero no es critico
        info = ticker.get_info()
        name = info.get("shortName") or info.get("longName") or symbol
    except Exception:
        pass
    if price is None:
        return {"symbol": symbol, "error": "sin datos (ticker mal escrito?)"}
    return {
        "symbol": symbol,
        "name": name,
        "price": round(float(price), 4),
        "prevClose": round(float(prev), 4) if prev else None,
        "currency": currency,
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/quotes")
def quotes():
    raw = request.args.get("symbols")
    symbols = raw.split(",") if raw else DEFAULT_SYMBOLS
    out = []
    for s in symbols:
        try:
            q = fetch_quote(s)
            if q:
                out.append(q)
        except Exception as e:  # nunca tumbamos el endpoint por un ticker
            out.append({"symbol": s.strip().upper(), "error": str(e)})
    return jsonify(out)


if __name__ == "__main__":
    # debug=True solo para desarrollo local
    app.run(host="127.0.0.1", port=5000, debug=True)
