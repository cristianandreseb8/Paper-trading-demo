# Paper Desk · simulador de trading con precios reales

Simulador de *paper trading* (dinero ficticio) que opera sobre **precios reales
con retardo** obtenidos de Yahoo Finance. Empiezas con **100 €** y la idea es
aprender el mecanismo (spreads, comisiones, volatilidad y, sobre todo, tu propia
psicología) sin arriesgar dinero de verdad.

> No es asesoramiento de inversión. Yahoo Finance no es una API oficial: puede
> fallar o cambiar, y los datos van con retardo (no es tiempo real puro).

## Qué hace

- Un backend en **Flask** (`app.py`) pide los precios a Yahoo con `yfinance`.
- El frontend (`templates/index.html`) hace el *paper trading* sobre esos precios.
- El frontend habla solo con tu backend, nunca con Yahoo directamente (así se
  evita el problema de CORS).

## Cómo ejecutarlo en tu ordenador

Necesitas Python 3.9 o superior.

```bash
# 1. (recomendado) crea un entorno virtual
python -m venv venv
source venv/bin/activate        # en Windows:  venv\Scripts\activate

# 2. instala dependencias
pip install -r requirements.txt

# 3. arranca el servidor
python app.py
```

Abre el navegador en **http://127.0.0.1:5000**

Puedes añadir cualquier ticker desde la interfaz (ej. `AAPL`, `MSFT`, `TSLA`).
Los de por defecto cotizan en EUR (Xetra) para que el saldo de 100 € tenga
sentido; si añades tickers en USD, ten en cuenta que mezclarás divisas.

## Cómo subirlo a tu GitHub

GitHub solo **guarda el código** (no ejecuta Python por sí solo). Para subirlo:

```bash
git init
git add .
git commit -m "Paper trading demo con precios reales"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
git push -u origin main
```

Crea antes el repositorio vacío en github.com (tú, con tu cuenta) y sustituye
`TU_USUARIO/TU_REPO`.

> **Importante:** GitHub Pages NO sirve para esto, porque solo aloja webs
> estáticas y este proyecto necesita un backend de Python.

## Cómo ponerlo online gratis (Render)

Render ejecuta Python, se conecta a tu repo de GitHub y permite las llamadas a
Yahoo. Plan gratuito, sin tarjeta.

1. Sube el proyecto a GitHub (pasos arriba).
2. Crea una cuenta en https://render.com (botón "Get Started", entra con GitHub).
3. Dashboard → **New +** → **Web Service**.
4. Conecta y elige tu repositorio.
5. Render detecta Python. Confirma estos campos:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Instance Type:** Free
6. **Create Web Service** y espera al primer despliegue (unos minutos).
7. Tu app queda en una URL tipo `https://paper-desk.onrender.com`.

(El archivo `render.yaml` incluido ya trae esta configuración; si Render detecta
el "Blueprint", puedes aceptarlo y te rellena los campos solo.)

### Cosas que debes saber del plan gratis

- **Se duerme** tras ~15 min sin visitas. La primera carga después de dormir
  tarda 30-50 s en despertar. Normal en demos gratis.
- **Yahoo desde la nube:** Yahoo a veces limita las IPs compartidas de los
  hostings. Si ves precios vacíos en Render aunque en local funcionen, ese es
  el motivo. Solución robusta: cambiar a una API con clave gratuita (Alpha
  Vantage) tocando solo `fetch_quote` en `app.py`.

Alternativas que también ejecutan Python gratis: Replit o Koyeb. Evita
PythonAnywhere para *esta* app: su plan gratis restringe la salida a internet y
bloquearía las llamadas a Yahoo.

## Si Yahoo deja de responder

Es un riesgo conocido por usar un endpoint no oficial. Si pasa, lo más robusto
es cambiar a una API con clave gratuita (por ejemplo Alpha Vantage): se tocaría
solo la función `fetch_quote` en `app.py`, sin cambiar el frontend.
