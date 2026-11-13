"""Genera docs/report.html: un informe autocontenido, con filtros, sin dependencias.

Un solo archivo: se abre desde el repo y desde GitHub Pages, sin CDN ni servidor.
Las cifras salen de las filas que calcula el script del proyecto, así que el
informe no puede desincronizarse de los datos.

`filas` son dicts {"a": valor del filtro, "g": grupo, "k": clave, "v": valor, "u": unidad}.
El grupo es la dimensión que dibuja cada gráfico ("mes", "ccaa", "ingresos"...).
"""
import html
import json
from pathlib import Path

CSS = """:root{--t:#1f2328;--g:#57606a;--l:#d0d7de;--a:#0f62fe;--r:#da1e28;--f:#f6f8fa}
*{box-sizing:border-box}
body{margin:0;color:var(--t);font:15px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
.w{max-width:1000px;margin:0 auto;padding:40px 24px 64px}
header{border-bottom:1px solid var(--l);padding-bottom:24px}
.eb{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--a);font-weight:700}
h1{font-size:30px;line-height:1.25;margin:10px 0 12px;letter-spacing:-.02em}
h2{font-size:19px;margin:0 0 4px}
.pq{color:var(--g);font-size:16px;max-width:70ch;margin:0}
.k{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin:28px 0 8px}
.k div{background:var(--f);border:1px solid var(--l);border-radius:10px;padding:14px 16px}
.k b{display:block;font-size:24px;letter-spacing:-.02em}
.k span{font-size:12px;color:var(--g);text-transform:uppercase;letter-spacing:.06em}
.k em{display:block;font-size:12px;color:var(--g);font-style:normal}
.fl{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:28px 0 4px}
.fl i{font-size:12px;color:var(--g);text-transform:uppercase;letter-spacing:.06em;font-style:normal;margin-right:4px}
button{font:inherit;font-size:13px;padding:6px 14px;border-radius:999px;border:1px solid var(--l);background:#fff;color:var(--g);cursor:pointer;transition:.15s}
button:hover{border-color:var(--a);color:var(--a)}
button[aria-pressed=true]{background:var(--a);border-color:var(--a);color:#fff}
section{margin:36px 0}
.s{color:var(--g);font-size:13px;margin:0 0 18px}
.b{display:grid;gap:9px}
.f{display:grid;grid-template-columns:132px 1fr 92px;gap:12px;align-items:center}
.f u{font-size:13px;color:var(--g);text-align:right;text-decoration:none;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.p{background:var(--f);border-radius:4px;height:22px;overflow:hidden}
.p div{height:100%;background:var(--a);border-radius:4px;transition:width .35s}
.p .neg{background:var(--r)}
.f s{font-size:13px;font-variant-numeric:tabular-nums;font-weight:600;text-align:right;text-decoration:none}
table{width:100%;border-collapse:collapse;font-size:13.5px}
th,td{text-align:left;padding:9px 10px;border-bottom:1px solid var(--l)}
th{font-size:11.5px;text-transform:uppercase;letter-spacing:.06em;color:var(--g)}
td.n{text-align:right;font-variant-numeric:tabular-nums}
ul,ol{color:var(--g);font-size:13.5px;padding-left:20px}
li{margin:6px 0}
footer{border-top:1px solid var(--l);margin-top:44px;padding-top:16px;font-size:12px;color:var(--g)}
code{background:var(--f);padding:2px 5px;border-radius:4px;font-size:12.5px}"""

JS = """const D=DATOS;let act='todos';
const num=(v,u)=>{const n=Math.abs(v).toLocaleString('es-ES',{maximumFractionDigits:u==='%'?1:0});return (v<0?'-':'')+n+(u==='%'?' %':'')};
function pinta(){D.graficos.forEach(g=>{const c=document.getElementById('g-'+g.id);
const fs=D.filas.filter(f=>f.g===g.grupo&&(act==='todos'||f.a===act));
if(!fs.length){c.innerHTML='<p class="s">Sin datos para este filtro.</p>';return}
const o={};fs.forEach(f=>{o[f.k]=(o[f.k]||0)+f.v});
const ks=(g.orden||Object.keys(o)).filter(k=>k in o),vs=ks.map(k=>o[k]);
const max=Math.max(...vs.map(Math.abs),1),u=g.unidad||fs[0].u||'';
c.innerHTML=ks.map((k,i)=>{const v=vs[i];
return '<div class="f"><u>'+k+'</u><div class="p"><div class="'+(v<0?'neg':'')+'" style="width:'+Math.max(Math.abs(v)/max*100,.6)+'%"></div></div><s>'+num(v,u)+'</s></div>'}).join('')})}
document.querySelectorAll('button').forEach(b=>b.addEventListener('click',()=>{act=b.dataset.v;
document.querySelectorAll('button').forEach(o=>o.setAttribute('aria-pressed',o===b));pinta()}));
pinta();"""

PLANTILLA = """<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{titulo}</title><style>{css}</style></head><body><div class="w">
<header><p class="eb">{eyebrow}</p><h1>{titulo}</h1><p class="pq">{pregunta}</p></header>
<div class="k">{kpis}</div>{filtros}{secciones}
<section><h2>Cómo se calcula</h2><p class="s">{metodo_sub}</p><ol>{metodo}</ol></section>
<section><h2>Qué no dice este informe</h2><p class="s">{lim_sub}</p><ul>{limitaciones}</ul></section>
<footer>Generado por <code>src/report.py</code> a partir de <code>{fuente}</code>. Sin dependencias,
sin CDN: cada cifra de esta página sale de los datos del repositorio.{pie}</footer>
</div><script>const DATOS={datos};{js}</script></body></html>"""


def num(valor, dec=0):
    """Número en formato español: 2.261.537, no 2,261,537."""
    return f"{valor:,.{dec}f}".replace(",", "@").replace(".", ",").replace("@", ".")


def _json_lineas(filas, graficos):
    """JSON con una fila por línea: se lee en el diff y no rompe la revisión."""
    def compacto(o):
        return json.dumps(o, ensure_ascii=False, separators=(",", ":"))
    return ('{"filas":[\n' + ",\n".join(compacto(f) for f in filas)
            + '\n],"graficos":' + compacto(graficos) + "}")


def escribir(ruta, *, eyebrow, titulo, pregunta, kpis, filtros, graficos, filas,
             metodo, limitaciones, fuente, tabla=None, metodo_sub="", lim_sub="",
             pie="", filtro_etiqueta="Año"):
    """Escribe el informe. `kpis`: [(etiqueta, valor, nota)]."""
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    kpis_html = "".join(f"<div><span>{html.escape(e)}</span><b>{html.escape(v)}</b>"
                        f"<em>{html.escape(n)}</em></div>" for e, v, n in kpis)
    filtros_html = ""
    if filtros:
        botones = "".join(
            f"<button data-v='{html.escape(str(o))}' aria-pressed='{str(o) == 'todos'}'>"
            f"{html.escape(str(o))}</button>" for o in filtros)
        filtros_html = (f"<div class='fl'><i>{html.escape(filtro_etiqueta)}</i>{botones}</div>")
    secciones = [f"<section><h2>{html.escape(g['titulo'])}</h2>"
                 f"<p class='s'>{html.escape(g['subtitulo'])}</p>"
                 f"<div class='b' id='g-{g['id']}'></div></section>" for g in graficos]
    if tabla:
        cab = "".join(f"<th>{html.escape(c)}</th>" for c in tabla["cabeceras"])
        cuerpo = "".join("<tr>" + "".join(
            (f"<td class='n'>{html.escape(str(c))}</td>" if i else f"<td>{html.escape(str(c))}</td>")
            for i, c in enumerate(f)) + "</tr>" for f in tabla["filas"])
        secciones.append(f"<section><h2>{html.escape(tabla['titulo'])}</h2>"
                         f"<p class='s'>{html.escape(tabla['subtitulo'])}</p>"
                         f"<table><thead><tr>{cab}</tr></thead><tbody>{cuerpo}</tbody></table></section>")
    texto = PLANTILLA.format(
        titulo=html.escape(titulo), eyebrow=html.escape(eyebrow),
        pregunta=html.escape(pregunta), kpis=kpis_html, filtros=filtros_html,
        secciones="\n".join(secciones), css=CSS, js=JS,
        datos=_json_lineas(filas, graficos),
        metodo="".join(f"<li>{html.escape(m)}</li>" for m in metodo),
        limitaciones="".join(f"<li>{html.escape(m)}</li>" for m in limitaciones),
        metodo_sub=html.escape(metodo_sub), lim_sub=html.escape(lim_sub),
        fuente=html.escape(fuente), pie=(" " + html.escape(pie)) if pie else "")
    ruta.write_text(texto.rstrip("\n"), encoding="utf-8")
    return ruta
