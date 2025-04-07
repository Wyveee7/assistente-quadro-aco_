
import streamlit as st
import ezdxf
import tempfile
from dwg_reader import extrair_quadro_aco

st.set_page_config(page_title="Assistente de Aço", layout="centered")

st.title("🧱 Assistente de Leitura de Quadro de Aço")
st.markdown("Envie um arquivo `.dxf` (ou `.dwg` caso suporte no futuro) contendo o quadro de aço.")

arquivo = st.file_uploader("📤 Envie um arquivo .dwg ou .dxf", type=["dwg", "dxf"])

if arquivo is not None:
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".dxf") as tmp:
            tmp.write(arquivo.read())
            tmp_path = tmp.name

        tabela = extrair_quadro_aco(tmp_path)
        st.success("✅ Quadro de aço extraído com sucesso!")
        st.dataframe(tabela)
    except Exception as e:
        st.error(f"❌ Erro ao processar o arquivo: {e}")
