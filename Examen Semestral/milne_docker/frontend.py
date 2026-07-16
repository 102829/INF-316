import httpx
import io
import base64
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from nicegui import ui

API_URL = "http://backend:8001"


def graficar(puntos):
    t  = [p['t']           for p in puntos]
    yl_e = [p['y_low_exacta'] for p in puntos]
    yu_e = [p['y_up_exacta']  for p in puntos]
    yl_m = [p['y_low_milne']  for p in puntos]
    yu_m = [p['y_up_milne']   for p in puntos]
    el   = [p['error_inf']    for p in puntos]
    eu   = [p['error_sup']    for p in puntos]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    fig.patch.set_facecolor('#111827')
    for ax in (ax1, ax2):
        ax.set_facecolor('#1f2937')
        ax.tick_params(colors='#9ca3af')
        for sp in ax.spines.values():
            sp.set_edgecolor('#374151')

    ax1.plot(t, yl_e, 'g-', lw=2,   label='Exacta inf')
    ax1.plot(t, yu_e, 'r-', lw=2,   label='Exacta sup')
    ax1.plot(t, yl_m, 'g--', lw=1.5, marker='o', ms=3, label='Milne inf')
    ax1.plot(t, yu_m, 'r--', lw=1.5, marker='o', ms=3, label='Milne sup')
    ax1.fill_between(t, yl_e, yu_e, alpha=0.1, color='#818cf8')
    ax1.set_title('Solucion difusa', color='white')
    ax1.set_xlabel('t', color='#9ca3af')
    ax1.set_ylabel('y(t)', color='#9ca3af')
    leg1 = ax1.legend(facecolor='#1f2937', edgecolor='#374151', fontsize=8)
    for tx in leg1.get_texts():
        tx.set_color('#d1d5db')
    ax1.grid(alpha=0.2)

    ax2.semilogy(t, [e + 1e-20 for e in el], 'g-', lw=1.8, label='Error inf')
    ax2.semilogy(t, [e + 1e-20 for e in eu], 'r-', lw=1.8, label='Error sup')
    ax2.set_title('Error absoluto (log)', color='white')
    ax2.set_xlabel('t', color='#9ca3af')
    ax2.set_ylabel('Error', color='#9ca3af')
    leg2 = ax2.legend(facecolor='#1f2937', edgecolor='#374151', fontsize=8)
    for tx in leg2.get_texts():
        tx.set_color('#d1d5db')
    ax2.grid(alpha=0.2)

    plt.tight_layout(pad=2)
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=120, bbox_inches='tight', facecolor='#111827')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()


@ui.page('/')
def page():
    ui.add_head_html('<style>body{background:#111827!important}.nicegui-content{background:#111827!important}</style>')

    with ui.column().classes('w-full p-6 gap-4').style('background:#111827;min-height:100vh'):

        # Titulo
        ui.label('Metodo de Milne - Predictor Corrector').style(
            'font-size:1.5rem;font-weight:700;color:#818cf8')
        with ui.row().classes('gap-4 items-center'):
            ui.label('Ecuaciones Diferenciales Difusas').style('font-size:.85rem;color:#6b7280')
            ui.link('Ver API Swagger', API_URL + '/docs', new_tab=True).style(
                'font-size:.8rem;color:#38bdf8;text-decoration:underline')
            ui.link('Ver ReDoc', API_URL + '/redoc', new_tab=True).style(
                'font-size:.8rem;color:#38bdf8;text-decoration:underline')

        # Controles
        with ui.card().style('background:#1f2937;border:1px solid #374151;border-radius:10px;padding:1rem'):
            ui.label('Parametros').style('color:#818cf8;font-weight:600;font-size:.8rem')
            with ui.row().classes('items-center gap-8 flex-wrap mt-2'):
                with ui.column().classes('gap-1'):
                    ui.label('Pasos N').style('color:#9ca3af;font-size:.85rem')
                    n_slider = ui.slider(min=4, max=100, step=1, value=20).style('width:220px')
                    n_lbl = ui.label('N = 20').style('color:#a78bfa;font-weight:600')
                with ui.column().classes('gap-1'):
                    ui.label('Alfa-corte r').style('color:#9ca3af;font-size:.85rem')
                    r_slider = ui.slider(min=0, max=1, step=0.05, value=0.5).style('width:220px')
                    r_lbl = ui.label('r = 0.50').style('color:#a78bfa;font-weight:600')
                btn = ui.button('Calcular').style(
                    'background:#6366f1;color:white;font-weight:600;border-radius:8px;padding:.5rem 1.5rem')

        # Stats
        with ui.row().classes('gap-4'):
            lbl_h    = ui.label('h = -').style('background:#1f2937;border:1px solid #374151;border-radius:8px;padding:.5rem 1rem;color:#a78bfa;font-weight:700')
            lbl_e    = ui.label('Error max = -').style('background:#1f2937;border:1px solid #374151;border-radius:8px;padding:.5rem 1rem;color:#f87171;font-weight:700')
            lbl_api  = ui.label('API: -').style('background:#1f2937;border:1px solid #374151;border-radius:8px;padding:.5rem 1rem;color:#4ade80;font-weight:700')

        # Grafica
        with ui.card().style('background:#1f2937;border:1px solid #374151;border-radius:10px;padding:1rem'):
            ui.label('Graficas').style('color:#818cf8;font-weight:600;font-size:.8rem')
            img = ui.html('<p style="color:#6b7280;text-align:center;padding:2rem">Presiona Calcular</p>')

        # Tabla
        with ui.card().style('background:#1f2937;border:1px solid #374151;border-radius:10px;padding:1rem'):
            ui.label('Tabla de errores').style('color:#818cf8;font-weight:600;font-size:.8rem')
            tabla = ui.html('')

    def update():
        n_lbl.set_text('N = ' + str(int(n_slider.value)))
        r_lbl.set_text('r = ' + str(round(r_slider.value, 2)))

    n_slider.on('update:model-value', lambda _: update())
    r_slider.on('update:model-value', lambda _: update())

    def calcular():
        N = int(n_slider.value)
        r = float(r_slider.value)

        try:
            resp = httpx.post(
                API_URL + '/calcular',
                json={'N': N, 'r': r},
                timeout=10
            )
            data = resp.json()
        except Exception as ex:
            lbl_api.set_text('API ERROR: ' + str(ex)[:40])
            lbl_api.style('background:#1f2937;border:1px solid #374151;border-radius:8px;padding:.5rem 1rem;color:#f87171;font-weight:700')
            return

        lbl_api.set_text('API: 200 OK')
        lbl_api.style('background:#1f2937;border:1px solid #374151;border-radius:8px;padding:.5rem 1rem;color:#4ade80;font-weight:700')
        lbl_h.set_text('h = ' + str(data['h']))
        lbl_e.set_text('Error max = ' + str(data['error_maximo']))

        puntos = data['puntos']
        b64 = graficar(puntos)
        img.set_content('<img src="data:image/png;base64,' + b64 + '" style="width:100%;border-radius:6px"/>')

        th = 'padding:.4rem .6rem;background:#111827;color:#818cf8;font-size:.75rem;text-align:right'
        td = 'padding:.3rem .6rem;border-bottom:1px solid #374151;font-size:.75rem;font-family:monospace'

        filas = ''
        for p in puntos:
            el = p['error_inf']
            eu = p['error_sup']
            cl = '#4ade80' if el < 1e-5 else '#f87171'
            cu = '#4ade80' if eu < 1e-5 else '#f87171'
            filas += '<tr>'
            filas += '<td style="' + td + ';color:#e5e7eb;text-align:center">' + str(round(p['t'], 3)) + '</td>'
            filas += '<td style="' + td + ';color:#9ca3af;text-align:right">' + str(p['y_low_exacta']) + '</td>'
            filas += '<td style="' + td + ';color:#9ca3af;text-align:right">' + str(p['y_low_milne']) + '</td>'
            filas += '<td style="' + td + ';color:' + cl + ';text-align:right">' + '{:.2e}'.format(el) + '</td>'
            filas += '<td style="' + td + ';color:#9ca3af;text-align:right">' + str(p['y_up_exacta']) + '</td>'
            filas += '<td style="' + td + ';color:#9ca3af;text-align:right">' + str(p['y_up_milne']) + '</td>'
            filas += '<td style="' + td + ';color:' + cu + ';text-align:right">' + '{:.2e}'.format(eu) + '</td>'
            filas += '</tr>'

        html = '<div style="overflow-x:auto">'
        html += '<table style="border-collapse:collapse;width:100%"><thead><tr>'
        html += '<th style="' + th + ';text-align:center">t</th>'
        html += '<th style="' + th + '">y_low Exacta</th>'
        html += '<th style="' + th + '">y_low Milne</th>'
        html += '<th style="' + th + '">Error inf</th>'
        html += '<th style="' + th + '">y_up Exacta</th>'
        html += '<th style="' + th + '">y_up Milne</th>'
        html += '<th style="' + th + '">Error sup</th>'
        html += '</tr></thead><tbody>' + filas + '</tbody></table></div>'
        tabla.set_content(html)

    btn.on('click', calcular)
    calcular()


ui.run(host='0.0.0.0', port=8003, title='Milne FDE Solver', dark=True)
