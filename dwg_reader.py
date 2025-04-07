
import ezdxf
import pandas as pd

def extrair_quadro_aco(caminho_arquivo):
    doc = ezdxf.readfile(caminho_arquivo)
    msp = doc.modelspace()
    dados = []

    for tabela in msp.query('TEXT MTEXT'):
        texto = tabela.plain_text() if tabela.dxftype() == 'MTEXT' else tabela.dxf.text
        pos = tabela.dxf.insert
        dados.append({'texto': texto.strip(), 'x': pos.x, 'y': pos.y})

    df = pd.DataFrame(dados)
    df = df.sort_values(by=['y', 'x'], ascending=[False, True]).reset_index(drop=True)
    return df
