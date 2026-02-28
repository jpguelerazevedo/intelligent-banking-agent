from langchain_core.messages import AIMessage, HumanMessage
from src.graph import build_graph, _get_initial_state

import streamlit as st

def main():
    st.set_page_config(page_title="Banco Ágil", page_icon="🏦")
    st.markdown("""
        <style>
        .sticky-header {
            position: sticky;
            top: 0;
            z-index: 999;
            background: transparent;
            padding-top: 20px;
        }
        </style>
        <h1 class='sticky-header' style='text-align: center; font-size: 2.5em; padding-bottom: 30px;'>🏦 Agente Banco Ágil 🏦</h1>
    """, unsafe_allow_html=True)
    if "state" not in st.session_state:
        graph = build_graph()
        state = _get_initial_state()
        state["messages"] = [HumanMessage(content="")]
        try:
            state = graph.invoke(state)
        except Exception as e:
            st.error(f"Erro ao inicializar: {e}")
            return
        st.session_state.graph = graph
        st.session_state.state = state
        st.session_state.chat_history = []
        # Exibe saudação inicial
        for msg in state["messages"]:
            if isinstance(msg, AIMessage) and msg.content:
                st.session_state.chat_history.append(("Atendente", msg.content))
                break
    else:
        graph = st.session_state.graph
        state = st.session_state.state

    for sender, message in st.session_state.chat_history:
        if sender == "Atendente":
            col1, col2 = st.columns([6, 1])
            with col1:
                st.markdown(f"<div style='float:left; clear:both; background: #708090; border-radius: 8px; padding: 8px; margin-bottom: 10px; display: inline-block; max-width:90%; word-break: break-word;'><b></b> {message}</div>", unsafe_allow_html=True)
            with col2:
                st.write("")
        elif sender == "Você":
            col1, col2 = st.columns([1, 6])
            with col1:
                st.write("")
            with col2:
                st.markdown(f"<div style='float:right; clear:both; background: #4682B4; border-radius: 8px; padding: 8px; margin-bottom: 10px; display: inline-block; max-width: 90%; word-break: break-word; color: #fff;'>{message}</div>", unsafe_allow_html=True)

    if not state.get("should_end", False):
        user_input = st.chat_input("Digite sua mensagem...")
        if user_input:
            st.session_state.chat_history.append(("Você", user_input))
            state["messages"].append(HumanMessage(content=user_input))
            try:
                state = graph.invoke(state)
            except Exception as e:
                st.error(f"Erro de sistema: {e}")
                return
            for msg in reversed(state["messages"]):
                if isinstance(msg, AIMessage) and msg.content:
                    st.session_state.chat_history.append(("Atendente", msg.content))
                    break
            st.session_state.state = state
            st.rerun()
    # else:
    #     st.info("Atendimento encerrado. Até logo!")

if __name__ == "__main__":
    main()
