
import streamlit as st
import pymupdf

from ollama import chat

from utils.chunker import create_chunks
from utils.rag import RAGSystem


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="LexiBot",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# LOCAL AI MODEL CONFIGURATION
# ============================================================

OLLAMA_MODEL = "qwen3:4b"


# ============================================================
# CREATE RAG SYSTEM
# ============================================================

@st.cache_resource
def load_rag_system():
    return RAGSystem()


rag_system = load_rag_system()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚖️ LexiBot")

    st.write(
        "AI-powered legal document analysis using "
        "Qwen 3 4B and Retrieval-Augmented Generation (RAG)."
    )

    st.divider()

    st.subheader("Features")

    st.write("📄 PDF Text Extraction")
    st.write("🔍 Semantic Search")
    st.write("🧠 Local AI Model")
    st.write("💬 Document Question Answering")

    st.divider()

    st.caption(
        "For informational purposes only. "
        "This application does not provide legal advice."
    )


# ============================================================
# MAIN UI
# ============================================================

st.title("⚖️ LexiBot")

st.markdown(
    """
    Upload a legal PDF document and ask questions
    about its contents using Retrieval-Augmented Generation (RAG).
    """
)

st.divider()


# ============================================================
# UPLOAD PDF
# ============================================================

uploaded_file = st.file_uploader(
    "Upload your PDF",
    type=["pdf"]
)


# ============================================================
# PROCESS UPLOADED PDF
# ============================================================

if uploaded_file is not None:

    st.success("PDF uploaded successfully!")

    # --------------------------------------------------------
    # OPEN PDF
    # --------------------------------------------------------

    document = pymupdf.open(
        stream=uploaded_file.getvalue(),
        filetype="pdf"
    )

    # --------------------------------------------------------
    # EXTRACT TEXT
    # --------------------------------------------------------

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    # --------------------------------------------------------
    # CHECK EXTRACTED TEXT
    # --------------------------------------------------------

    if not text.strip():

        st.warning(
            "No readable text was found in this PDF. "
            "The PDF may contain scanned images instead of text."
        )

        st.stop()

    # --------------------------------------------------------
    # CREATE DOCUMENT CHUNKS
    # --------------------------------------------------------

    chunks = create_chunks(
        text,
        chunk_size=1000,
        overlap=200
    )

    # --------------------------------------------------------
    # BUILD FAISS INDEX
    # --------------------------------------------------------

    with st.spinner("Building document search index..."):

        try:

            rag_system.build_index(chunks)

        except Exception as e:

            st.error(
                f"Error building the document index: {e}"
            )

            st.stop()

    # --------------------------------------------------------
    # CREATE TABS
    # --------------------------------------------------------

    tab1, tab2 = st.tabs(
        [
            "📄 Document Text",
            "💬 Ask Questions"
        ]
    )

    # ========================================================
    # TAB 1 - DOCUMENT TEXT
    # ========================================================

    with tab1:

        st.subheader("Extracted Document Text")

        st.text_area(
            "Document Content",
            text,
            height=500
        )

        st.caption(
            f"Document divided into {len(chunks)} chunks "
            "for AI processing."
        )

    # ========================================================
    # TAB 2 - ASK QUESTIONS
    # ========================================================

    with tab2:

        st.subheader(
            "Ask Questions About the Document"
        )

        question = st.text_input(
            "Enter your question:",
            placeholder=(
                "Example: What is the termination "
                "notice period?"
            )
        )

        if st.button(
            "Ask Question",
            type="primary"
        ):

            if not question.strip():

                st.warning(
                    "Please enter a question."
                )

            else:

                # ------------------------------------------------
                # FIND RELEVANT CHUNKS
                # ------------------------------------------------

                with st.spinner(
                    "Finding relevant information..."
                ):

                    try:

                        relevant_results = rag_system.search(
                            question,
                            k=3
                        )

                    except Exception as e:

                        st.error(
                            f"Error searching the document: {e}"
                        )

                        st.stop()

                    if not relevant_results:

                        st.warning(
                            "No relevant information was found "
                            "in the document."
                        )

                        st.stop()

                    relevant_chunks = [
                        result["text"]
                        for result in relevant_results
                    ]

                    context = "\n\n".join(
                        relevant_chunks
                    )

                # ------------------------------------------------
                # CREATE RAG PROMPT
                # ------------------------------------------------

                question_prompt = f"""
You are LexiBot, an AI assistant specialized in legal document analysis.

Your task is to answer the user's question using ONLY the information
contained in the provided document context.

IMPORTANT RULES:

1. Use only the provided document context.
2. Do not use outside knowledge.
3. Do not invent or assume facts.
4. If the answer cannot be found in the context, say:
   "The information is not available in the provided document."
5. Give a concise and accurate answer.
6. Preserve the original legal meaning.
7. When possible, mention the relevant clause, section, or provision.
8. Do not provide legal advice.
9. Do not tell the user what they should legally do.
10. Answer directly and clearly.

DOCUMENT CONTEXT:

{context}

USER QUESTION:

{question}

ANSWER:
"""

                # ------------------------------------------------
                # GENERATE ANSWER USING LOCAL QWEN MODEL
                # ------------------------------------------------

                with st.spinner(
                    "Generating answer using Qwen 3 4B..."
                ):

                    try:

                        response = chat(
                            model=OLLAMA_MODEL,
                            messages=[
                                {
                                    "role": "user",
                                    "content": question_prompt
                                }
                            ]
                        )

                        answer = response.message.content

                    except Exception as e:

                        st.error(
                            "Error generating answer with Ollama: "
                            f"{e}"
                        )

                        st.info(
                            "Make sure Ollama is installed and "
                            f"the model '{OLLAMA_MODEL}' is available."
                        )

                        st.stop()

                # ------------------------------------------------
                # DISPLAY ANSWER
                # ------------------------------------------------

                st.subheader("AI Answer")

                if answer:

                    st.markdown(answer)

                else:

                    st.warning(
                        "Qwen returned an empty response."
                    )

                st.caption(
                    "Answer generated locally using Qwen 3 4B, "
                    "FAISS retrieval, and RAG."
                )
