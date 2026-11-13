"""Generador mínimo de gráficos SVG: una función, sin dependencias.

Los SVG son texto: se ven nítidos en GitHub, pesan ~2 KB y se pueden
versionar sin llenar el repositorio de binarios.
"""
from html import escape
from pathlib import Path

AZUL, ROJO, GRIS, TINTA = "#0f62fe", "#da1e28", "#8d8d8d", "#1f2328"
FUENTE = "font-family='-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif'"


def barras(datos, titulo, ruta, subtitulo=None, ancho=660, alto=300,
           formato="{:,.1f}", sufijo=""):
    """datos: lista de (etiqueta, valor, color|None)."""
    # Las etiquetas llevan <, > y % (">200 DM"), así que se escapan como XML.
    titulo = escape(titulo)
    subtitulo = escape(subtitulo) if subtitulo else None
    izq, der, arriba, abajo = 12, 12, 54 if subtitulo else 40, 46
    area_w = ancho - izq - der
    area_h = alto - arriba - abajo
    vmax = max(abs(v) for _, v, _ in datos) or 1
    paso = area_w / len(datos)
    bw = paso * 0.56
    partes = [
        f"<svg xmlns='http://www.w3.org/2000/svg' width='{ancho}' height='{alto}' "
        f"viewBox='0 0 {ancho} {alto}' role='img' aria-label='{titulo}'>",
        f"<rect width='{ancho}' height='{alto}' fill='#ffffff'/>",
        f"<text x='{izq}' y='24' {FUENTE} font-size='15' font-weight='600' "
        f"fill='{TINTA}'>{titulo}</text>",
    ]
    if subtitulo:
        partes.append(f"<text x='{izq}' y='42' {FUENTE} font-size='12' "
                      f"fill='{GRIS}'>{subtitulo}</text>")
    linea = arriba + area_h
    # Con valores negativos el gráfico es divergente: la línea base va al centro
    # y las barras crecen hacia arriba (positivo) o hacia abajo (negativo).
    divergente = any(v < 0 for _, v, _ in datos)
    base = arriba + area_h / 2 if divergente else linea
    alto_max = area_h / 2 if divergente else area_h
    partes.append(f"<line x1='{izq}' y1='{base:.1f}' x2='{ancho-der}' y2='{base:.1f}' "
                  f"stroke='#d0d7de' stroke-width='1'/>")
    for i, (label, valor, color) in enumerate(datos):
        h = alto_max * abs(valor) / vmax
        x = izq + paso * i + (paso - bw) / 2
        y = base - h if valor >= 0 else base
        partes.append(
            f"<rect x='{x:.1f}' y='{y:.1f}' width='{bw:.1f}' height='{h:.1f}' "
            f"rx='3' fill='{color or AZUL}'/>")
        y_texto = y - 7 if valor >= 0 else y + h + 15
        partes.append(
            f"<text x='{x + bw/2:.1f}' y='{y_texto:.1f}' {FUENTE} font-size='12' "
            f"font-weight='600' text-anchor='middle' fill='{TINTA}'>"
            f"{formato.format(valor)}{sufijo}</text>")
        partes.append(
            f"<text x='{x + bw/2:.1f}' y='{linea + 18:.1f}' {FUENTE} "
            f"font-size='11.5' text-anchor='middle' fill='#57606a'>{escape(label)}</text>")
    partes.append("</svg>")
    Path(ruta).parent.mkdir(parents=True, exist_ok=True)
    Path(ruta).write_text("\n".join(partes) + "\n", encoding="utf-8")
    return Path(ruta)
