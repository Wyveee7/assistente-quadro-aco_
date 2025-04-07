
import streamlit as st
import ezdxf
import tempfile
import pandas as pd
from dwg_reader import extrair_quadro_aco_formatado

st.set_page_config(page_title="Assistente de Aço", layout="centered")
st.title("🧱 Assistente de Leitura de Quadro de Aço")
st.markdown("Envie um arquivo `.dxf` com a tabela de aço no formato padrão.")

arquivo = st.file_uploader("📤 Envie um arquivo .dxf", type=["dxf"])

if arquivo is not None:
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".dxf") as tmp:
            tmp.write(arquivo.read())
            tmp_path = tmp.name

        tabela = extrair_quadro_aco_formatado(tmp_path)
        st.success("✅ Quadro de aço extraído com sucesso!")
        st.dataframe(tabela)

        csv = tabela.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Baixar CSV", data=csv, file_name="quadro_aco.csv", mime="text/csv")

    except Exception as e:
        st.error(f"❌ Erro ao processar o arquivo: {e}")
