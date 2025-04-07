
import ezdxf
import pandas as pd

def extrair_quadro_aco_formatado(caminho_arquivo):
    doc = ezdxf.readfile(caminho_arquivo)
    msp = doc.modelspace()
    dados = []

    for entidade in msp.query('TEXT MTEXT'):
        texto = entidade.plain_text() if entidade.dxftype() == 'MTEXT' else entidade.dxf.text
        pos = entidade.dxf.insert
        dados.append({'texto': texto.strip(), 'x': pos.x, 'y': pos.y})

    df = pd.DataFrame(dados)
    df = df.sort_values(by=['y', 'x'], ascending=[False, True]).reset_index(drop=True)

    # Detectar colunas com base nas posições x
    colunas = sorted(df['x'].unique())
    tabela_linhas = []

    for y in sorted(df['y'].unique(), reverse=True):
        linha = df[df['y'] == y].sort_values(by='x')
        if len(linha) >= 4:
            valores = linha['texto'].tolist()
            tabela_linhas.append(valores)

    # Ajustar para o formato da tabela de aço
    tabela_final = []
    tipo_aco = ""
    for linha in tabela_linhas:
        if "CA" in linha[0]:
            tipo_aco = linha[0]
            continue
        if len(linha) >= 5:
            n, diam, quant, c_unit, c_total = linha[:5]
            tabela_final.append({
                "AÇO": tipo_aco,
                "N": n,
                "DIAM (mm)": diam,
                "QUANT": quant,
                "C. UNIT (cm)": c_unit,
                "C. TOTAL (cm)": c_total
            })

    return pd.DataFrame(tabela_final)
