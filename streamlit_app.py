from __future__ import annotations

import json
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


APP_DIR = Path(__file__).resolve().parent


def read_secret(name: str) -> str:
    try:
        return str(st.secrets.get(name, "")).strip()
    except FileNotFoundError:
        return ""


def build_html() -> str:
    html = (APP_DIR / "translate_quity.html").read_text(encoding="utf-8")
    api_key = read_secret("DIRECT_TECH_API_KEY")
    if not api_key:
        raise RuntimeError("请在 Streamlit App settings -> Secrets 中配置 DIRECT_TECH_API_KEY")

    injected_key = json.dumps(api_key, ensure_ascii=False)
    return html.replace(
        "window.__STREAMLIT_DIRECT_TECH_API_KEY || ''",
        f"{injected_key}",
    )


st.set_page_config(page_title="LLM 翻译结果查看", layout="wide")

try:
    page_html = build_html()
except RuntimeError as error:
    st.error(str(error))
    st.stop()

components.html(page_html, height=1200, scrolling=True)
