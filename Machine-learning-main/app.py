import html
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

import utils
from utils import decimal, porcentaje

BASE = Path(__file__).parent

st.set_page_config(
    page_title="Genesis | Sistema de análisis preventivo de clientes",
    page_icon=str(BASE / "assets" / "icono.svg"),
    layout="wide",
    initial_sidebar_state="collapsed",
)

TINTA = "#1C2430"
MUTED = "#4F5B66"
BORDE = "#D3DADE"
ACENTO = "#0E5A6B"
OSCURO = "#0B3C49"
VERDE_ACENTO = "#6FBF9B"
BAJO, MEDIO, ALTO = utils.COLORES["Bajo"], utils.COLORES["Medio"], utils.COLORES["Alto"]
PERMANECE, ABANDONA = "#5E9AAD", "#0B3C49"
ESTADO_COLORES = {"Permanecen": PERMANECE, "Abandonaron": ABANDONA}
FUENTE = "IBM Plex Sans, Segoe UI, Arial, sans-serif"

NOMBRES = {
    "Regresión Logística": "Regresión logística (estándar)",
    "Regresión Logística balanceada": "Regresión logística (balanceada)",
    "Random Forest": "Random Forest (bosque aleatorio)",
    "K-Nearest Neighbors": "KNN (vecinos más cercanos)",
}
NOMBRES_GRAFICA = {
    "Regresión Logística": "Reg. logística<br>estándar",
    "Regresión Logística balanceada": "Reg. logística<br>balanceada",
    "Random Forest": "Random<br>Forest",
    "K-Nearest Neighbors": "KNN",
}

ICONOS = {
    "usuarios": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "alerta": '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
    "estable": '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
    "porcentaje": '<line x1="19" x2="5" y1="5" y2="19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/>',
    "lista": '<path d="M8 6h13"/><path d="M8 12h13"/><path d="M8 18h13"/><path d="M3 6h.01"/><path d="M3 12h.01"/><path d="M3 18h.01"/>',
    "reloj": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "objetivo": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    "barras": '<line x1="12" x2="12" y1="20" y2="10"/><line x1="18" x2="18" y1="20" y2="4"/><line x1="6" x2="6" y1="20" y2="16"/>',
    "base": '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14a9 3 0 0 0 18 0V5"/><path d="M3 12a9 3 0 0 0 18 0"/>',
    "modelo": '<path d="M3 3v18h18"/><path d="m7 15 4-4 3 3 5-6"/>',
}

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&display=swap');

:root {
    --tinta: #1C2430; --muted: #4F5B66; --tenue: #66717C; --borde: #CDD5DA;
    --acento: #0E5A6B; --oscuro: #0B3C49; --verde: #6FBF9B;
    --bajo: #1F6E43; --medio: #A85F00; --alto: #B4161B;
    --barra: #0A2A34;
}

.stApp, .stApp button, .stApp input, .stApp textarea, .stApp [data-baseweb] {
    font-family: 'IBM Plex Sans', 'Segoe UI', Arial, sans-serif;
}
[data-testid="stHeader"] { background: transparent; height: 0; }
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"], [data-testid="stExpandSidebarButton"] { display: none !important; }
.block-container { padding-top: 1.2rem; padding-bottom: 4rem; max-width: 1280px; }
footer { visibility: hidden; }

.stApp *, .stApp *::before, .stApp *::after,
[data-baseweb="popover"], [data-baseweb="popover"] * { border-radius: 0 !important; }
.stApp *, [data-baseweb="popover"] > div, [data-testid="stDialog"] div[role="dialog"],
[data-testid="stToast"], [data-testid="stNotification"] { box-shadow: none !important; }
[data-baseweb="popover"] > div, [data-testid="stDialog"] div[role="dialog"],
[data-testid="stToast"], [data-testid="stNotification"] { border: 1px solid var(--borde); }

.ico { width: 20px; height: 20px; fill: none; stroke: currentColor; stroke-width: 1.8; stroke-linecap: square; stroke-linejoin: miter; flex: none; }

.st-key-topbar { background: var(--barra); border-bottom: 3px solid var(--verde); padding: .7rem 1.2rem; margin-bottom: 1.6rem; }
.st-key-topbar .brand { padding: 0; margin: 0; border: 0; }
.stApp .st-key-topbar label p { color: #9DB5BE; font-size: .66rem; font-weight: 600; letter-spacing: .1em; text-transform: uppercase; text-align: center; width: 100%; }
.st-key-topbar [data-testid="stWidgetLabel"] { justify-content: center; }
.st-key-topbar [data-baseweb="select"] > div { background: #fff; border: 1px solid #fff; min-height: 2.6rem; cursor: pointer; }
.st-key-topbar [data-baseweb="select"] > div:hover, .st-key-topbar [data-baseweb="select"] > div:focus-within { border-color: var(--verde); }
.st-key-topbar [data-baseweb="select"] div[value], .st-key-topbar [data-baseweb="select"] span { font-weight: 600; color: var(--tinta); }
.top-info { text-align: right; font-size: .74rem; line-height: 1.6; color: #9DB5BE; }
.top-info b { color: #fff; font-weight: 600; font-variant-numeric: tabular-nums; }

.page-head { border-bottom: 1px solid var(--borde); margin: 0 0 1.4rem; padding-bottom: .9rem; }
.page-head h1 { font-size: 1.65rem; font-weight: 700; color: var(--tinta); margin: 0; padding: 0; letter-spacing: -.01em; }
.page-head p { color: var(--muted); margin: .35rem 0 0; font-size: .95rem; max-width: 62rem; }

.kpi-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 16px; margin: 0 0 20px; }
.kpi { background: #fff; border: 1px solid var(--borde); border-top: 4px solid var(--c, var(--acento)); padding: 14px 18px 16px; display: flex; flex-direction: column; }
.kpi-top { display: flex; justify-content: space-between; align-items: flex-start; gap: 8px; color: var(--c, var(--acento)); }
.kpi-label { font-size: .72rem; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: .07em; }
.kpi-value { font-size: 2.6rem; font-weight: 700; color: var(--tinta); line-height: 1.1; margin-top: 8px; font-variant-numeric: tabular-nums; letter-spacing: -.02em; }
.kpi-value.corto { font-size: 1.35rem; line-height: 1.25; letter-spacing: 0; padding: .35rem 0 .2rem; }
.kpi-sub { font-size: .78rem; color: var(--tenue); margin-top: auto; padding-top: 8px; border-top: 1px solid #E4E9EC; }

[class*="st-key-panel"] { background: #fff; border: 1px solid var(--borde); padding: 1.1rem 1.3rem 1rem; }
.panel-title { font-weight: 600; font-size: .95rem; color: var(--tinta); margin: 0; }
.panel-sub { font-size: .8rem; color: var(--tenue); margin: 0 0 .5rem; }
.panel-text { font-size: .9rem; color: #2B3440; line-height: 1.55; margin: 0 0 .7rem; }

.grupo { margin: 1rem 0 .25rem; padding-bottom: .35rem; border-bottom: 1px solid #E4E9EC; }
.grupo:first-child { margin-top: 0; }
.grupo b { display: block; font-size: .78rem; font-weight: 600; letter-spacing: .06em; text-transform: uppercase; color: var(--acento); }
.grupo span { font-size: .78rem; color: var(--tenue); }

.stApp label p { font-weight: 500; font-size: .84rem; color: #2B3440; }
[data-testid="stBaseButton-primaryFormSubmit"], [data-testid="stBaseButton-primary"] {
    background: var(--acento); border: 1px solid var(--acento); color: #fff;
    font-weight: 500; padding: .6rem 1rem; box-shadow: none;
}
[data-testid="stBaseButton-primaryFormSubmit"]:hover, [data-testid="stBaseButton-primary"]:hover {
    background: var(--oscuro); border-color: var(--oscuro); color: #fff;
}
[data-testid="stBaseButton-secondary"] { background: #fff; border: 1px solid #9FAAB3; color: var(--tinta); font-weight: 500; box-shadow: none; padding: .4rem .5rem; }
[data-testid="stBaseButton-secondary"] p { font-size: .84rem; white-space: nowrap; }
[data-testid="stBaseButton-secondary"]:hover { border-color: var(--acento); color: var(--acento); }

.result-card { background: #fff; border: 1px solid var(--borde); border-left: 5px solid var(--c); padding: 20px 24px; }
.result-top { display: flex; justify-content: space-between; align-items: center; gap: 10px; flex-wrap: wrap; }
.tag { font-size: .7rem; font-weight: 600; letter-spacing: .08em; text-transform: uppercase; color: var(--c); border: 1px solid var(--c); padding: .2rem .55rem; }
.result-name { font-weight: 500; color: var(--muted); font-size: .92rem; }
.result-title { font-size: 1.4rem; font-weight: 600; color: var(--tinta); margin: 14px 0 2px; }
.result-prob { color: var(--muted); font-size: .9rem; }
.result-prob span { font-size: 3.2rem; font-weight: 700; color: var(--c); margin-right: 8px; font-variant-numeric: tabular-nums; letter-spacing: -.02em; }
.bar { position: relative; height: 12px; background: #E3E8EB; margin: 16px 0 4px; }
.bar-fill { height: 100%; background: var(--c); }
.bar-tick { position: absolute; top: -4px; bottom: -4px; width: 1px; background: #5C6772; }
.bar-scale { position: relative; height: 1.1rem; font-size: .72rem; color: var(--muted); font-variant-numeric: tabular-nums; }
.bar-scale span { position: absolute; transform: translateX(-50%); white-space: nowrap; }
.bar-scale .ini { transform: none; }
.bar-scale .fin { transform: translateX(-100%); }
.bar-bands { position: relative; height: 1.1rem; font-size: .7rem; font-weight: 600; letter-spacing: .06em; text-transform: uppercase; color: var(--tenue); }
.bar-bands span { position: absolute; transform: translateX(-50%); }
.result-reco { margin: 16px 0 0; padding-top: 12px; border-top: 1px solid var(--borde); color: #2B3440; font-size: .92rem; }
.result-nota { margin: 8px 0 0; font-size: .76rem; color: var(--tenue); }

.tabla-wrap { overflow-x: auto; }
.tabla { width: 100%; border-collapse: collapse; font-size: .82rem; }
.tabla th { text-align: left; font-weight: 500; color: var(--muted); font-size: .68rem; text-transform: uppercase; letter-spacing: .03em; border-bottom: 1px solid var(--borde); padding: .45rem .35rem; vertical-align: bottom; }
.tabla td { padding: .5rem .35rem; border-bottom: 1px solid #E9EDF0; color: var(--tinta); font-variant-numeric: tabular-nums; }
.tabla th.num, .tabla td.num { text-align: right; }
.tabla tr:last-child td { border-bottom: 0; }
.tabla tr.sel td { background: #EEF5F6; font-weight: 600; }
.tabla tr.sel td:first-child { border-left: 3px solid var(--acento); }
.tabla td.lect-mal { color: var(--alto); font-weight: 600; white-space: nowrap; }
.tabla td.lect-bien { color: var(--bajo); font-weight: 600; white-space: nowrap; }
.tabla td.lect-neu { color: var(--tenue); }
.en-uso { display: inline-block; margin-left: .4rem; font-size: .62rem; font-weight: 600; letter-spacing: .06em; text-transform: uppercase; color: var(--acento); border: 1px solid var(--acento); padding: 0 .35rem; vertical-align: middle; }

.vacio { text-align: center; padding: 2.4rem 1rem; color: var(--muted); font-size: .92rem; }
.vacio b { display: block; color: var(--tinta); font-size: 1rem; font-weight: 600; margin-bottom: .25rem; }

.def-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 14px; }
.def { border-top: 3px solid var(--acento); background: #F7F9FA; padding: 10px 14px 12px; }
.def b { display: block; font-size: .88rem; color: var(--tinta); }
.def p { margin: .3rem 0 0; font-size: .82rem; color: #2B3440; line-height: 1.5; }
.def small { display: block; margin-top: .4rem; color: var(--tenue); font-size: .76rem; }

.lista-lim { margin: 0; padding-left: 1.1rem; font-size: .88rem; color: #2B3440; line-height: 1.6; }
.lista-lim li { margin-bottom: .35rem; }

.brand { display: flex; align-items: center; gap: 12px; }
.brand-name { font-size: 1.35rem; font-weight: 700; color: #fff; line-height: 1.1; letter-spacing: -.01em; }
.brand-sub { font-size: .7rem; color: #9DB5BE; margin-top: 3px; letter-spacing: .02em; }

@media (max-width: 1000px) {
    .kpi-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
@media (max-width: 640px) {
    .block-container { padding: 1rem .8rem 3rem; }
    .st-key-topbar { padding: .7rem .8rem; }
    .top-info { display: none; }
    .page-head h1 { font-size: 1.4rem; }
    .tabla { font-size: .74rem; }
    .tabla th { letter-spacing: 0; font-size: .62rem; }
    .kpi-grid { gap: 10px; }
    .kpi { padding: 12px 12px 14px; }
    .kpi-value { font-size: 1.8rem; }
    .result-prob span { font-size: 2.4rem; }
    .result-title { font-size: 1.2rem; }
    [class*="st-key-panel"] { padding: .9rem .9rem .8rem; }
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

MARCA = (
    '<div class="brand">'
    '<svg width="40" height="40" viewBox="0 0 48 48" role="img" aria-label="Genesis">'
    '<rect width="48" height="48" fill="#15535F"/>'
    '<polyline points="9,36 19,27 27,31 38,14" fill="none" stroke="#FFFFFF" stroke-width="3.5" stroke-linecap="square"/>'
    '<rect x="33" y="9" width="10" height="10" fill="#6FBF9B"/></svg>'
    '<div><div class="brand-name">Genesis</div><div class="brand-sub">Análisis preventivo de clientes</div></div>'
    '</div>'
)


@st.cache_resource
def get_modelo():
    return utils.cargar_modelo()


@st.cache_data
def get_metricas():
    return utils.cargar_metricas()


@st.cache_data
def get_datos():
    df = utils.puntuar_dataset(get_modelo(), utils.cargar_datos())
    df["estado"] = df["abandono"].map({0: "Permanecen", 1: "Abandonaron"})
    return df


utils.init_db()


def cabecera(titulo: str, subtitulo: str) -> None:
    st.markdown(
        f'<div class="page-head"><h1>{titulo}</h1><p>{subtitulo}</p></div>',
        unsafe_allow_html=True,
    )


def icono(nombre: str) -> str:
    return f'<svg class="ico" viewBox="0 0 24 24" aria-hidden="true">{ICONOS[nombre]}</svg>'


def tarjetas(items: list[tuple]) -> None:
    cuerpo = ""
    for color, ico, etiqueta, valor, sub in items:
        cuerpo += (
            f'<div class="kpi" style="--c:{color}"><div class="kpi-top"><div class="kpi-label">{etiqueta}</div>{icono(ico)}</div>'
            f'<div class="kpi-value{" corto" if len(str(valor)) > 11 else ""}">{valor}</div><div class="kpi-sub">{sub}</div></div>'
        )
    st.markdown(f'<div class="kpi-grid">{cuerpo}</div>', unsafe_allow_html=True)


def titulo_panel(titulo: str, sub: str = "") -> None:
    st.markdown(f'<p class="panel-title">{titulo}</p><p class="panel-sub">{sub}</p>', unsafe_allow_html=True)


def parrafo(texto: str) -> None:
    st.markdown(f'<p class="panel-text">{texto}</p>', unsafe_allow_html=True)


def tabla_html(cabeceras: list[str], filas: list[list], numericas: set[int] | None = None, seleccion: int | None = None) -> str:
    numericas = numericas or set()
    cab = "".join(f'<th class="{"num" if i in numericas else ""}">{c}</th>' for i, c in enumerate(cabeceras))
    cuerpo = ""
    for n, fila in enumerate(filas):
        celdas = ""
        for i, celda in enumerate(fila):
            clase = "num" if i in numericas else ""
            if isinstance(celda, tuple):
                celda, extra = celda
                clase = f"{clase} {extra}".strip()
            celdas += f'<td class="{clase}">{celda}</td>'
        cuerpo += f'<tr class="{"sel" if n == seleccion else ""}">{celdas}</tr>'
    return f'<div class="tabla-wrap"><table class="tabla"><thead><tr>{cab}</tr></thead><tbody>{cuerpo}</tbody></table></div>'


def estilo(fig: go.Figure, alto: int = 300, leyenda: bool = False) -> go.Figure:
    fig.update_layout(
        height=alto,
        margin=dict(l=4, r=8, t=40 if leyenda else 10, b=4),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FUENTE, size=13, color="#2B3440"),
        showlegend=leyenda,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0, xanchor="left", title=None, font=dict(size=12.5)),
        hoverlabel=dict(bgcolor="white", bordercolor=BORDE, font=dict(family=FUENTE, color=TINTA)),
    )
    fig.update_xaxes(showgrid=False, zeroline=False, linecolor="#9FAAB3", ticks="outside", tickcolor="#9FAAB3")
    fig.update_yaxes(gridcolor="#E4E9EC", zeroline=False, showline=False)
    return fig


def mostrar(fig: go.Figure) -> None:
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})


def vacio(titulo: str, texto: str) -> None:
    st.markdown(f'<div class="vacio"><b>{titulo}</b>{texto}</div>', unsafe_allow_html=True)


def pagina_panel():
    datos = get_datos()
    historial = utils.leer_historial()

    cabecera(
        "Panel principal",
        "Genesis centraliza la evaluación de clientes para ayudar al equipo a identificar casos que podrían requerir seguimiento.",
    )

    total = len(datos)
    n_alto = int((datos["riesgo"] == "Alto").sum())
    n_bajo = int((datos["riesgo"] == "Bajo").sum())
    promedio = datos["probabilidad"].mean()

    tarjetas([
        (ACENTO, "usuarios", "Clientes evaluados", f"{total:,}".replace(",", "."),
         f"Base de clientes. {len(historial)} evaluaciones nuevas en el historial"),
        (ALTO, "alerta", "Requieren atención alta", f"{n_alto}", f"{porcentaje(n_alto / total, 1)} de los clientes evaluados"),
        (BAJO, "estable", "Con atención baja", f"{n_bajo}", f"{porcentaje(n_bajo / total, 1)} de los clientes evaluados"),
        (ACENTO, "porcentaje", "Prob. promedio de abandono", porcentaje(promedio, 1),
         f"Abandono real en la base: {porcentaje(datos['abandono'].mean(), 1)}"),
    ])

    c1, c2 = st.columns(2)
    with c1, st.container(key="panel_riesgo"):
        titulo_panel("Clientes por nivel de atención",
                     "Bajo: probabilidad menor a 40 %. Medio: de 40 a 70 %. Alto: 70 % o más.")
        conteo = datos["riesgo"].value_counts().reindex(["Bajo", "Medio", "Alto"]).fillna(0).astype(int).reset_index()
        conteo.columns = ["riesgo", "clientes"]
        conteo["texto"] = conteo["clientes"].map(lambda n: f"{n} ({porcentaje(n / total)})")
        conteo["nivel"] = conteo["riesgo"].map(lambda r: f"Atención {r.lower()}")
        fig = px.bar(conteo, x="nivel", y="clientes", color="riesgo", text="texto",
                     color_discrete_map=utils.COLORES, labels={"nivel": "Nivel de atención", "clientes": "Clientes"})
        fig.update_traces(textposition="outside", cliponaxis=False, marker_line_width=0)
        fig.update_layout(bargap=0.5, yaxis_range=[0, conteo["clientes"].max() * 1.2])
        mostrar(estilo(fig))

    with c2, st.container(key="panel_satisfaccion"):
        titulo_panel("Satisfacción: clientes que permanecen y clientes que abandonaron",
                     "Cantidad de clientes en cada nivel de satisfacción, de 1 (muy baja) a 10 (muy alta)")
        fig = px.histogram(datos, x="satisfaccion", color="estado", barmode="group", nbins=10,
                           color_discrete_map=ESTADO_COLORES, category_orders={"estado": ["Permanecen", "Abandonaron"]},
                           pattern_shape="estado", pattern_shape_map={"Permanecen": "", "Abandonaron": "/"},
                           labels={"satisfaccion": "Nivel de satisfacción (1 a 10)", "estado": ""})
        fig.update_traces(marker_line_width=0)
        fig.update_layout(bargap=0.25, yaxis_title="Clientes")
        fig.update_xaxes(dtick=1)
        mostrar(estilo(fig, leyenda=True))

    st.write("")
    c3, c4 = st.columns(2)
    with c3, st.container(key="panel_edades"):
        titulo_panel("Distribución de edades", "Cantidad de clientes por rango de edad")
        fig = px.histogram(datos, x="edad", nbins=14, color_discrete_sequence=[ACENTO], labels={"edad": "Edad (años)"})
        fig.update_traces(marker_line_width=0)
        fig.update_layout(bargap=0.08, yaxis_title="Clientes")
        mostrar(estilo(fig))

    with c4, st.container(key="panel_antiguedad"):
        titulo_panel("Abandono según antigüedad", "Porcentaje de clientes que abandonaron, por tiempo como cliente")
        tramos = pd.cut(datos["tiempo_cliente"], bins=[0, 6, 12, 24, 48, 1000],
                        labels=["0 a 6 meses", "6 a 12 meses", "1 a 2 años", "2 a 4 años", "Más de 4 años"])
        tasa = (datos.groupby(tramos, observed=True)["abandono"].mean() * 100).round(1).reset_index()
        tasa.columns = ["tramo", "tasa"]
        fig = px.bar(tasa, x="tramo", y="tasa", text="tasa", color_discrete_sequence=[ACENTO],
                     labels={"tramo": "Tiempo como cliente", "tasa": "% de clientes que abandonaron"})
        fig.update_traces(texttemplate="%{text:.0f} %", textposition="outside", marker_line_width=0, cliponaxis=False)
        fig.update_layout(bargap=0.4, yaxis_range=[0, max(tasa["tasa"]) * 1.2])
        mostrar(estilo(fig))

    st.write("")
    with st.container(key="panel_ultimas"):
        titulo_panel("Últimas evaluaciones realizadas", "Las 5 más recientes del historial")
        if historial.empty:
            vacio("Aún no hay evaluaciones", "Ve a Nueva evaluación para analizar al primer cliente.")
        else:
            tabla = historial.head(5)
            st.dataframe(
                pd.DataFrame({
                    "Cliente": tabla["nombre"],
                    "Fecha y hora": tabla["fecha"],
                    "Satisfacción": tabla["satisfaccion"],
                    "Nivel de atención": tabla["riesgo"].map(lambda r: f"Atención {r.lower()}"),
                    "Probabilidad de abandono": tabla["probabilidad"] * 100,
                }),
                hide_index=True, width="stretch",
                column_config={"Probabilidad de abandono": st.column_config.ProgressColumn(
                    "Probabilidad de abandono", format="%.0f %%", min_value=0, max_value=100)},
            )


EJEMPLOS = {
    "alto": dict(f_nombre="Laura Gómez", f_edad=27, f_ingresos=2_000_000, f_frecuencia=2,
                 f_productos=5, f_tiempo=10, f_satisfaccion=5),
    "medio": dict(f_nombre="Mariana Torres", f_edad=35, f_ingresos=3_000_000, f_frecuencia=3,
                  f_productos=8, f_tiempo=14, f_satisfaccion=6),
    "bajo": dict(f_nombre="Carlos Rodríguez", f_edad=45, f_ingresos=4_200_000, f_frecuencia=4,
                 f_productos=10, f_tiempo=36, f_satisfaccion=7),
}


def cargar_ejemplo(clave: str) -> None:
    for k, v in EJEMPLOS[clave].items():
        st.session_state[k] = v


def formatear(col: str, valor: float, decimales: int = 1) -> str:
    if col == "ingresos":
        return utils.formato_cop(valor)
    if decimales == 0:
        return f"{valor:g}"
    return decimal(valor, decimales)


def comparacion(datos: dict, df: pd.DataFrame, features: list[str]) -> list[list]:
    perm, aban = df[df["abandono"] == 0], df[df["abandono"] == 1]
    filas = []
    for col in features:
        desv = df[col].std()
        sentido = 1 if aban[col].mean() > perm[col].mean() else -1
        relevante = abs(aban[col].mean() - perm[col].mean()) / desv >= 0.15
        diferencia = (datos[col] - perm[col].mean()) / desv * sentido
        if relevante and diferencia > 0.5:
            lectura, clase = "En contra", "lect-mal"
        elif relevante and diferencia < -0.5:
            lectura, clase = "A favor", "lect-bien"
        else:
            lectura, clase = "Neutral", "lect-neu"
        filas.append([
            utils.ETIQUETAS[col],
            formatear(col, datos[col], 0),
            formatear(col, perm[col].mean()),
            formatear(col, aban[col].mean()),
            (lectura, clase),
        ])
    return filas


def grafica_perfil(datos: dict, df: pd.DataFrame, features: list[str]) -> go.Figure:
    def norm(valor, col):
        mn, mx = df[col].min(), df[col].max()
        return max(0.0, min(100.0, (valor - mn) / (mx - mn) * 100))

    nombres = [utils.ETIQUETAS[c] for c in features]
    cliente = [norm(datos[c], c) for c in features]
    perm = [norm(df.loc[df["abandono"] == 0, c].mean(), c) for c in features]
    aban = [norm(df.loc[df["abandono"] == 1, c].mean(), c) for c in features]

    fig = go.Figure()
    xs, ys = [], []
    for n, p, a in zip(nombres, perm, aban):
        xs += [p, a, None]
        ys += [n, n, None]
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color="#C3CCD2", width=3),
                             hoverinfo="skip", showlegend=False))
    for etiqueta, valores, simbolo, color, borde, grosor, tam in [
        ("Promedio de quienes permanecen", perm, "circle", PERMANECE, "white", 1.5, 11),
        ("Promedio de quienes abandonaron", aban, "diamond", ABANDONA, "white", 1.5, 12),
        ("Este cliente", cliente, "square", "white", TINTA, 2.5, 13),
    ]:
        fig.add_trace(go.Scatter(
            x=valores, y=nombres, mode="markers", name=etiqueta,
            marker=dict(symbol=simbolo, size=tam, color=color, line=dict(color=borde, width=grosor)),
            hovertemplate="%{y}: %{x:.0f} de 100<extra>" + etiqueta + "</extra>",
        ))
    fig.update_layout(xaxis=dict(range=[-3, 103], tickvals=[0, 25, 50, 75, 100],
                                 title="Posición en la base (0 a 100)",
                                 showgrid=True, gridcolor="#E4E9EC"),
                      yaxis=dict(autorange="reversed", showgrid=False),
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0, xanchor="left", title=None, font=dict(size=11.5)))
    return estilo(fig, 360, leyenda=True)


def grafica_efectos(efectos: dict) -> go.Figure:
    filas = sorted(((utils.ETIQUETAS[k], v * 100) for k, v in efectos.items()), key=lambda t: t[1])
    fig = go.Figure()
    for nombre, color, cond in [
        ("Aumenta la probabilidad", ALTO, lambda v: v > 0),
        ("Reduce la probabilidad", BAJO, lambda v: v <= 0),
    ]:
        sel = [f for f in filas if cond(f[1])]
        fig.add_trace(go.Bar(
            x=[f[1] for f in sel], y=[f[0] for f in sel], orientation="h", name=nombre,
            marker=dict(color=color, line_width=0),
            text=[f"{f[1]:+.1f}".replace(".", ",") for f in sel], textposition="outside", cliponaxis=False,
            hovertemplate="%{y}: %{x:+.1f} puntos porcentuales<extra></extra>",
        ))
    tope = max(abs(f[1]) for f in filas) * 2.6 or 1
    fig.update_layout(barmode="overlay", bargap=0.45,
                      xaxis=dict(range=[-tope, tope], zeroline=True, zerolinecolor="#5C6772",
                                 title="Cambio (puntos)", automargin=True,
                                 showgrid=True, gridcolor="#E4E9EC"),
                      yaxis=dict(showgrid=False, categoryorder="array", categoryarray=[f[0] for f in filas]))
    return estilo(fig, 360, leyenda=True)


def barra_resultado(prob: float) -> str:
    marcas = "".join(f'<div class="bar-tick" style="left:{p}%"></div>' for p in (40, 70))
    escala = (
        '<span class="ini" style="left:0">0 %</span><span style="left:40%">40 %</span>'
        '<span style="left:70%">70 %</span><span class="fin" style="left:100%">100 %</span>'
    )
    bandas = '<span style="left:20%">Bajo</span><span style="left:55%">Medio</span><span style="left:85%">Alto</span>'
    return (
        f'<div class="bar" role="progressbar" aria-label="Probabilidad estimada de abandono" aria-valuemin="0" '
        f'aria-valuemax="100" aria-valuenow="{prob * 100:.0f}"><div class="bar-fill" style="width:{prob * 100:.1f}%"></div>{marcas}</div>'
        f'<div class="bar-scale">{escala}</div><div class="bar-bands">{bandas}</div>'
    )


def pagina_evaluacion():
    modelo = get_modelo()
    df = get_datos()
    features = modelo["features"]

    cabecera("Nueva evaluación",
             "Ingrese los datos de un cliente para conocer el nivel de atención que requiere y la acción recomendada.")

    for k, v in dict(f_nombre="", f_edad=35, f_ingresos=3_000_000, f_frecuencia=3,
                     f_productos=8, f_tiempo=24, f_satisfaccion=6).items():
        st.session_state.setdefault(k, v)

    col_form, col_res = st.columns([1, 1.15], gap="large")

    with col_form, st.container(key="panel_form"):
        titulo_panel("Datos del cliente", "Complete los campos y presione Evaluar cliente")
        st.caption("Cargar un ejemplo de nivel de atención")
        b1, b2, b3 = st.columns(3)
        b1.button("Alta", on_click=cargar_ejemplo, args=("alto",), width="stretch")
        b2.button("Media", on_click=cargar_ejemplo, args=("medio",), width="stretch")
        b3.button("Baja", on_click=cargar_ejemplo, args=("bajo",), width="stretch")

        with st.form("form_cliente", border=False):
            st.markdown('<div class="grupo"><b>1. Identificación</b><span>Cliente y perfil básico</span></div>',
                        unsafe_allow_html=True)
            nombre = st.text_input("Nombre del cliente", key="f_nombre", placeholder="Ej. Laura Gómez",
                                   help="Nombre con el que quedará registrada la evaluación en el historial.")
            a, b = st.columns(2)
            edad = a.number_input("Edad (años)", min_value=18, max_value=100, step=1, key="f_edad",
                                  help="Edad actual del cliente, entre 18 y 100 años.")
            ingresos = b.number_input("Ingresos (COP)", min_value=0, max_value=100_000_000, step=100_000,
                                      key="f_ingresos", format="%d",
                                      help="Ingreso aproximado del cliente por mes, en pesos colombianos.")
            st.markdown('<div class="grupo"><b>2. Comportamiento de compra</b><span>Qué tanto compra el cliente</span></div>',
                        unsafe_allow_html=True)
            c, d = st.columns(2)
            frecuencia = c.number_input("Compras por mes", min_value=0, max_value=60, step=1, key="f_frecuencia",
                                        help="Frecuencia de compra: cuántas compras realiza el cliente en un mes típico.")
            productos = d.number_input("Productos adquiridos", min_value=0, max_value=500, step=1, key="f_productos",
                                       help="Cantidad de productos que el cliente ha comprado en los últimos 12 meses.")
            st.markdown('<div class="grupo"><b>3. Relación con la empresa</b><span>Antigüedad y experiencia</span></div>',
                        unsafe_allow_html=True)
            e, f = st.columns(2)
            tiempo = e.number_input("Tiempo como cliente (meses)", min_value=1, max_value=480, step=1, key="f_tiempo",
                                    help="Meses transcurridos desde que el cliente se vinculó a la empresa.")
            satisfaccion = f.slider("Nivel de satisfacción (1 a 10)", min_value=1, max_value=10, key="f_satisfaccion",
                                    help="1 significa muy insatisfecho y 10 significa muy satisfecho.")
            enviado = st.form_submit_button("Evaluar cliente", type="primary", width="stretch")

        if enviado:
            if not nombre.strip():
                st.error("Escriba el nombre del cliente para continuar.")
            else:
                datos = dict(edad=edad, ingresos=ingresos, frecuencia_compra=frecuencia,
                             cantidad_productos=productos, tiempo_cliente=tiempo, satisfaccion=satisfaccion)
                prob = utils.predecir(modelo, datos)
                utils.guardar_evaluacion(nombre.strip(), datos, prob)
                st.session_state["ultimo"] = dict(nombre=nombre.strip(), datos=datos, prob=prob)
                st.toast("Evaluación guardada en el historial")

    ultimo = st.session_state.get("ultimo")

    with col_res:
        if not ultimo:
            with st.container(key="panel_vacio"):
                vacio("El resultado aparecerá aquí",
                      "Complete el formulario o cargue un ejemplo y presione Evaluar cliente.")
        else:
            prob, nivel = ultimo["prob"], utils.nivel_riesgo(ultimo["prob"])
            color = utils.COLORES[nivel]
            st.markdown(
                f"""
                <div class="result-card" style="--c:{color}">
                  <div class="result-top"><span class="tag">Atención {nivel.lower()}</span>
                    <span class="result-name">{html.escape(ultimo['nombre'])}</span></div>
                  <div class="result-title">Nivel de atención: {nivel}</div>
                  <div class="result-prob"><span>{porcentaje(prob)}</span>probabilidad estimada de abandono</div>
                  {barra_resultado(prob)}
                  <div class="result-reco"><b>Recomendación.</b> {utils.RECOMENDACION[nivel]}</div>
                  <div class="result-nota">La probabilidad sirve para priorizar el seguimiento. No asegura lo que hará el cliente.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.write("")
            with st.container(key="panel_comparacion_cliente"):
                titulo_panel("Comparación con la base de clientes",
                             "Valor del cliente frente al promedio de quienes permanecen y de quienes abandonaron. En contra: el dato se parece al de quienes abandonan. A favor: se parece al de quienes permanecen.")
                st.markdown(
                    tabla_html(["Variable", "Cliente", "Permanecen", "Abandonaron", "Lectura"],
                               comparacion(ultimo["datos"], df, features), numericas={1, 2, 3}),
                    unsafe_allow_html=True,
                )

    if ultimo:
        st.write("")
        g1, g2 = st.columns(2)
        with g1, st.container(key="panel_efectos"):
            titulo_panel("Factores que influyeron en esta evaluación",
                         "Cuánto cambiaría la probabilidad (en puntos porcentuales) si cada dato tuviera el valor típico de la base. "
                         "Son asociaciones que encontró el modelo, no causas comprobadas.")
            mostrar(grafica_efectos(utils.efecto_variables(modelo, ultimo["datos"], df)))
        with g2, st.container(key="panel_perfil"):
            titulo_panel("Perfil del cliente frente a la base",
                         "Dónde se ubica cada dato del cliente dentro del rango de la base, junto con el promedio de cada grupo.")
            mostrar(grafica_perfil(ultimo["datos"], df, features))


@st.dialog("Eliminar historial")
def confirmar_borrado():
    st.write("Se borrarán todas las evaluaciones guardadas. Esta acción no se puede deshacer.")
    a, b = st.columns(2)
    if a.button("Cancelar", width="stretch"):
        st.rerun()
    if b.button("Sí, eliminar", type="primary", width="stretch"):
        utils.borrar_historial()
        st.session_state.pop("ultimo", None)
        st.rerun()


def pagina_historial():
    cabecera("Historial", "Cada evaluación realizada queda registrada con los datos del cliente, el nivel de atención y la recomendación.")
    hist = utils.leer_historial()

    if hist.empty:
        with st.container(key="panel_hvacio"):
            vacio("El historial está vacío", "Las evaluaciones que realice aparecerán aquí automáticamente.")
        return

    tarjetas([
        (ACENTO, "lista", "Evaluaciones registradas", f"{len(hist)}", "Total en el historial"),
        (ALTO, "alerta", "Con atención alta", f"{int((hist['riesgo'] == 'Alto').sum())}", "Requieren una acción de retención"),
        (BAJO, "estable", "Con atención baja", f"{int((hist['riesgo'] == 'Bajo').sum())}", "Mantienen el seguimiento habitual"),
        (ACENTO, "porcentaje", "Probabilidad promedio", porcentaje(hist["probabilidad"].mean(), 1), "De los clientes evaluados"),
    ])

    with st.container(key="panel_historial"):
        f1, f2 = st.columns([2, 3])
        buscar = f1.text_input("Buscar por nombre", placeholder="Escriba un nombre")
        niveles = f2.multiselect("Nivel de atención", ["Bajo", "Medio", "Alto"], default=["Bajo", "Medio", "Alto"])

        vista = hist[hist["riesgo"].isin(niveles)]
        if buscar:
            vista = vista[vista["nombre"].str.contains(buscar, case=False, na=False)]

        tabla = pd.DataFrame({
            "Nombre": vista["nombre"],
            "Fecha y hora": vista["fecha"],
            "Nivel de atención": vista["riesgo"].map(lambda r: f"Atención {r.lower()}"),
            "Probabilidad": vista["probabilidad"] * 100,
            "Recomendación": vista["recomendacion"],
            "Edad": vista["edad"],
            "Ingresos": vista["ingresos"].map(utils.formato_cop),
            "Satisfacción": vista["satisfaccion"],
            "Compras/mes": vista["frecuencia_compra"],
            "Productos": vista["cantidad_productos"],
            "Meses": vista["tiempo_cliente"],
        })
        st.dataframe(
            tabla, hide_index=True, width="stretch",
            column_config={
                "Probabilidad": st.column_config.ProgressColumn("Probabilidad", format="%.0f %%", min_value=0, max_value=100),
                "Recomendación": st.column_config.TextColumn("Recomendación", width="large"),
            },
        )
        st.caption(f"Mostrando {len(vista)} de {len(hist)} evaluaciones")

        exportar = pd.DataFrame({
            "nombre": hist["nombre"],
            "fecha_hora": hist["fecha"],
            "edad": hist["edad"],
            "ingresos": hist["ingresos"],
            "compras_por_mes": hist["frecuencia_compra"],
            "productos": hist["cantidad_productos"],
            "meses_como_cliente": hist["tiempo_cliente"],
            "satisfaccion": hist["satisfaccion"],
            "nivel_de_atencion": hist["riesgo"],
            "probabilidad_de_abandono": hist["probabilidad"].round(4),
            "recomendacion": hist["recomendacion"],
        })
        d1, d2, _ = st.columns([1, 1, 2])
        d1.download_button("Descargar CSV", data=exportar.to_csv(index=False).encode("utf-8-sig"),
                           file_name="historial_genesis.csv", mime="text/csv", width="stretch")
        if d2.button("Eliminar historial", width="stretch"):
            confirmar_borrado()


def pagina_analisis():
    m = get_metricas()
    res = m["resultados"]
    mejor = m["modelo_seleccionado"]
    r = res[mejor]
    tn, fp = r["matriz_confusion"][0]
    fn, tp = r["matriz_confusion"][1]
    abandonos = tp + fn

    cabecera("Análisis técnico",
             "Resultados del modelo de clasificación que usa Genesis para estimar la probabilidad de abandono, explicados paso a paso.")

    tarjetas([
        (ACENTO, "modelo", "Modelo seleccionado", NOMBRES[mejor], "Modelo de clasificación"),
        (BAJO, "objetivo", "Accuracy en prueba", porcentaje(r["accuracy"], 1), f"{int(round(r['accuracy'] * m['n_test']))} de {m['n_test']} clientes clasificados bien"),
        (MEDIO, "alerta", "Abandonos detectados", porcentaje(r["recall"], 1), f"{tp} de {abandonos} abandonos reales (recall)"),
        (ACENTO, "base", "Datos de entrenamiento y prueba", f"{m['n_train']} y {m['n_test']}", f"{m['n_total']} clientes en total, división 80 % y 20 %"),
    ])

    with st.container(key="panel_seleccion"):
        titulo_panel("Por qué se eligió este modelo", "El equilibrio entre detectar abandonos y evitar alertas innecesarias")
        parrafo(
            "Genesis busca avisar a tiempo cuando un cliente podría irse. Un modelo puede equivocarse de dos formas: "
            "<b>no detectar</b> a un cliente que sí se va, o <b>dar una alerta innecesaria</b> sobre uno que se queda. "
            "Perder a un cliente suele costar más que una llamada de seguimiento de más, por eso se da prioridad a detectar abandonos "
            "sin dejar que el accuracy baje de forma importante."
        )
        if "Regresión Logística balanceada" in res:
            est, bal = res["Regresión Logística"], res["Regresión Logística balanceada"]
            tp_e, fn_e, fp_e = est["matriz_confusion"][1][1], est["matriz_confusion"][1][0], est["matriz_confusion"][0][1]
            tp_b, fn_b, fp_b = bal["matriz_confusion"][1][1], bal["matriz_confusion"][1][0], bal["matriz_confusion"][0][1]
            filas = [
                ["Accuracy", porcentaje(est["accuracy"], 1), porcentaje(bal["accuracy"], 1)],
                ["Abandonos detectados (recall)", f"{tp_e} de {tp_e + fn_e} ({porcentaje(est['recall'])})",
                 f"{tp_b} de {tp_b + fn_b} ({porcentaje(bal['recall'])})"],
                ["Abandonos sin detectar", f"{fn_e}", f"{fn_b}"],
                ["Alertas innecesarias", f"{fp_e}", f"{fp_b}"],
                ["Precisión de las alertas", porcentaje(est["precision"]), porcentaje(bal["precision"])],
                ["F1 de la clase Abandona", decimal(est["f1"], 3), decimal(bal["f1"], 3)],
                ["Recall en validación cruzada", porcentaje(est["cv_recall_media"]), porcentaje(bal["cv_recall_media"])],
            ]
            st.markdown(
                tabla_html(["Resultado en el conjunto de prueba", "Regresión logística estándar", "Regresión logística balanceada"],
                           filas, numericas={1, 2}),
                unsafe_allow_html=True,
            )
            parrafo(
                f"<b>Decisión.</b> La versión balanceada detecta {tp_b} de los {tp_b + fn_b} clientes que abandonaron, frente a {tp_e} de los "
                f"{tp_e + fn_e} de la versión estándar. A cambio, el accuracy baja {decimal((est['accuracy'] - bal['accuracy']) * 100, 0)} puntos "
                f"y aparecen {fp_b - fp_e} alertas innecesarias más. Para una aplicación preventiva de retención ese intercambio es razonable, "
                "así que Genesis usa la versión balanceada."
            )
            parrafo(f"<b>Regla de selección.</b> {m['criterio']}")
        else:
            parrafo(f"<b>Regla de selección.</b> {m['criterio']}")

    st.write("")
    with st.container(key="panel_comparacion"):
        titulo_panel("Comparación de los modelos entrenados",
                     "Todos se entrenaron con los mismos 400 clientes y se evaluaron con los mismos 100. Precisión, recall y F1 corresponden a la clase Abandona.")
        filas = []
        for k in res:
            nombre = NOMBRES[k] + ('<span class="en-uso">En uso</span>' if k == mejor else "")
            filas.append([nombre, porcentaje(res[k]["accuracy"], 1), porcentaje(res[k]["precision"], 1),
                          porcentaje(res[k]["recall"], 1), decimal(res[k]["f1"], 3),
                          porcentaje(res[k]["cv_accuracy_media"], 1), porcentaje(res[k]["cv_recall_media"], 1)])
        st.markdown(
            tabla_html(["Modelo", "Accuracy", "Precisión", "Recall", "F1", "Accuracy val. cruzada", "Recall val. cruzada"],
                       filas, numericas={1, 2, 3, 4, 5, 6}, seleccion=list(res).index(mejor)),
            unsafe_allow_html=True,
        )
        st.caption("La validación cruzada repite el entrenamiento y la prueba 5 veces con el conjunto de entrenamiento. Es una estimación más estable que una sola prueba de 100 clientes.")
        largo = pd.DataFrame([
            {"Modelo": NOMBRES_GRAFICA[k], "Métrica": etiqueta, "Valor": res[k][clave]}
            for k in res for etiqueta, clave in [("Accuracy", "accuracy"), ("Recall (Abandona)", "recall"), ("F1 (Abandona)", "f1")]
        ])
        fig = px.bar(largo, x="Modelo", y="Valor", color="Métrica", barmode="group",
                     color_discrete_sequence=[ACENTO, "#7FB5A0", "#8A99A6"], labels={"Modelo": "", "Valor": "Valor (de 0 a 1)"},
                     text=largo["Valor"].map(lambda v: decimal(v, 2)))
        fig.update_traces(marker_line_width=0, textposition="outside", cliponaxis=False)
        fig.update_layout(yaxis_range=[0, 1], bargap=0.35, yaxis_tickformat=".1f")
        mostrar(estilo(fig, 320, leyenda=True))

    st.write("")
    with st.container(key="panel_metricas"):
        titulo_panel("Qué significa cada métrica", "Explicadas con los resultados del modelo en uso")
        st.markdown(
            f"""
            <div class="def-grid">
              <div class="def"><b>Accuracy</b><p>De cada 100 clientes, cuántos clasifica bien el modelo, tanto los que se quedan como los que se van.</p>
                <small>Aquí: {int(round(r['accuracy'] * m['n_test']))} de {m['n_test']}.</small></div>
              <div class="def"><b>Precisión</b><p>Cuando el modelo avisa que un cliente podría irse, qué tan seguido acierta. Mide las alertas innecesarias.</p>
                <small>Aquí: {tp} de {tp + fp} alertas fueron abandonos reales.</small></div>
              <div class="def"><b>Recall</b><p>De todos los clientes que sí abandonaron, cuántos logró detectar el modelo. Mide los abandonos que se escapan.</p>
                <small>Aquí: {tp} de {abandonos} clientes detectados.</small></div>
              <div class="def"><b>F1</b><p>Un solo número que combina precisión y recall. Sube cuando ambas son buenas a la vez.</p>
                <small>Aquí: {decimal(r['f1'], 3)} en una escala de 0 a 1.</small></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    with st.container(key="panel_detalle"):
        titulo_panel("Matriz de confusión y reporte de clasificación",
                     "Cuenta los aciertos y errores del modelo con clientes que no vio al entrenar. Las filas son lo que ocurrió en realidad y las columnas lo que predijo el modelo.")
        pestanas = st.tabs([NOMBRES[k] for k in res])
        for pestana, nombre in zip(pestanas, res):
            with pestana:
                x, y = st.columns([1, 1.1])
                with x:
                    cm = res[nombre]["matriz_confusion"]
                    fig = px.imshow(cm, text_auto=True, aspect="auto",
                                    x=["Predicho: Permanece", "Predicho: Abandona"], y=["Real: Permanece", "Real: Abandona"],
                                    color_continuous_scale=[[0, "#F0F4F5"], [1, ACENTO]])
                    fig.update_traces(textfont_size=22, xgap=3, ygap=3)
                    fig.update_layout(coloraxis_showscale=False)
                    fig.update_xaxes(side="bottom", ticks="")
                    fig.update_yaxes(ticks="")
                    mostrar(estilo(fig, 300))
                with y:
                    rep = res[nombre]["reporte"]
                    filas = [
                        [etiqueta, decimal(rep[clave]["precision"]), decimal(rep[clave]["recall"]),
                         decimal(rep[clave]["f1-score"]), f"{int(rep[clave]['support'])}"]
                        for etiqueta, clave in [("Permanece", "Permanece"), ("Abandona", "Abandona"),
                                                ("Promedio simple", "macro avg"), ("Promedio ponderado", "weighted avg")]
                    ]
                    st.markdown(tabla_html(["Clase", "Precisión", "Recall", "F1", "Casos"], filas, numericas={1, 2, 3, 4}),
                                unsafe_allow_html=True)
                    st.caption(f"Accuracy global: **{porcentaje(res[nombre]['accuracy'], 1)}**")

    st.write("")
    c1, c2 = st.columns([1.2, 1])
    with c1, st.container(key="panel_importancia"):
        titulo_panel("Variables más importantes", f"Cuánto empeora el accuracy de {NOMBRES[mejor].lower()} al desordenar cada variable")
        imp = pd.DataFrame({"Variable": [utils.ETIQUETAS[k] for k in m["importancias"]], "Importancia": list(m["importancias"].values())})
        fig = px.bar(imp.sort_values("Importancia"), x="Importancia", y="Variable", orientation="h", color_discrete_sequence=[ACENTO],
                     labels={"Importancia": "Pérdida de accuracy al desordenar la variable"})
        fig.update_traces(marker_line_width=0)
        fig.update_layout(bargap=0.4, yaxis_title=None)
        fig.update_xaxes(showgrid=True, gridcolor="#E4E9EC")
        fig.update_yaxes(showgrid=False)
        mostrar(estilo(fig, 300))
    with c2, st.container(key="panel_proceso"):
        titulo_panel("Proceso seguido")
        st.markdown(
            f"""
1. **Datos:** {m['n_total']} clientes con 6 variables y el campo abandono (sí o no).
2. **Limpieza con Pandas:** duplicados, valores imposibles y nulos (mediana).
3. **X e y:** 6 variables de entrada y `abandono` como objetivo.
4. **Entrenamiento y prueba:** 80 % y 20 %, con la misma proporción de abandonos en ambos.
5. **Modelos:** regresión logística (estándar y balanceada), Random Forest y KNN.
6. **Evaluación:** accuracy, matriz de confusión, reporte y validación cruzada.
7. **Selección:** se guarda en `ml/modelo.pkl` junto con su escalador y lo usa esta aplicación.
            """
        )

    st.write("")
    with st.container(key="panel_limites"):
        titulo_panel("Limitaciones", "Qué tener en cuenta al interpretar los resultados")
        st.markdown(
            f"""
            <ul class="lista-lim">
              <li><b>Los datos son sintéticos.</b> Se generaron con una regla de negocio y ruido aleatorio para este proyecto. No son clientes reales, así que las cifras sirven para demostrar el método y no para decisiones comerciales.</li>
              <li><b>La prueba es pequeña.</b> Con {m['n_test']} clientes de prueba, cada cliente mal clasificado mueve el accuracy un punto. Por eso se muestra también la validación cruzada.</li>
              <li><b>El modelo se equivoca.</b> Con el modelo en uso, {fn} de {abandonos} abandonos no se detectan y {fp} clientes que se quedan reciben una alerta innecesaria.</li>
              <li><b>La probabilidad es orientativa.</b> Al balancear las clases, el modelo tiende a asignar probabilidades más altas que la frecuencia real de abandono ({porcentaje(m['tasa_abandono'], 1)} en la base). Úsela para ordenar y priorizar clientes, no como una cifra exacta.</li>
              <li><b>Los niveles son una convención.</b> Los cortes de 40 % y 70 % se definieron como regla de negocio y no los aprendió el modelo.</li>
              <li><b>Asociación no es causa.</b> Los factores que influyeron muestran qué datos se relacionan con el abandono en la base, no por qué se va un cliente concreto.</li>
              <li><b>Pocas variables.</b> Solo se usan 6 datos del cliente. Un caso real incluiría reclamos, pagos, uso del servicio y contacto con soporte.</li>
            </ul>
            """,
            unsafe_allow_html=True,
        )


paginas = [
    st.Page(pagina_panel, title="Panel principal", icon=":material/dashboard:", url_path="panel", default=True),
    st.Page(pagina_evaluacion, title="Nueva evaluación", icon=":material/person_search:", url_path="evaluacion"),
    st.Page(pagina_historial, title="Historial", icon=":material/history:", url_path="historial"),
    st.Page(pagina_analisis, title="Análisis técnico", icon=":material/analytics:", url_path="analisis"),
]
navegacion = st.navigation(paginas, position="hidden")
por_titulo = {p.title: p for p in paginas}


def elegir_seccion() -> None:
    st.session_state["destino"] = st.session_state["nav"]


destino = st.session_state.pop("destino", None)
if destino and destino != navegacion.title:
    st.switch_page(por_titulo[destino])
st.session_state["nav"] = navegacion.title

_m = get_metricas()
with st.container(key="topbar"):
    izq, centro, der = st.columns([1, 1, 1], vertical_alignment="center")
    izq.markdown(MARCA, unsafe_allow_html=True)
    centro.selectbox("Sección", list(por_titulo), key="nav", on_change=elegir_seccion)
    der.markdown(
        f'<div class="top-info">Modelo <b>{NOMBRES[_m["modelo_seleccionado"]]}</b><br>'
        f'Accuracy <b>{porcentaje(_m["resultados"][_m["modelo_seleccionado"]]["accuracy"], 1)}</b>'
        f' · Clientes en la base <b>{_m["n_total"]}</b></div>',
        unsafe_allow_html=True,
    )

navegacion.run()
