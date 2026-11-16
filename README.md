# ⚖️ LexiBot – AI-Powered Legal Document Assistant

### Ever opened a long legal document and wished you could just ask it a question?

That's the idea behind **LexiBot**!

Legal documents can be lengthy, complicated and time-consuming to read. Finding one specific piece of information can mean going through several pages.

LexiBot makes this easier by allowing users to upload a legal PDF and ask questions about its content. Instead of searching through the entire document manually, the application finds relevant information and uses AI to generate an answer.

## 💡 How Does It Work?

LexiBot uses **Retrieval-Augmented Generation (RAG)**, which basically means the AI looks for relevant information in the uploaded document before generating an answer.

Here's the process:

1. **Upload a PDF** – The user uploads a legal document.
2. **Extract the text** – PyMuPDF reads and extracts the text from the PDF.
3. **Split into chunks** – The text is divided into smaller sections to make processing easier.
4. **Generate embeddings** – Sentence Transformers converts the text into numerical representations.
5. **Find relevant information** – FAISS searches for the three most relevant chunks based on the user's question.
6. **Generate an answer** – A language model uses the retrieved information to answer the question.

The goal is to make searching through legal documents quicker and more convenient.

## 🛠️ Technologies Used

- **Python** – Main programming language
- **Streamlit** – Web application interface
- **PyMuPDF** – PDF text extraction
- **Sentence Transformers** – Text embeddings using `all-MiniLM-L6-v2`
- **FAISS** – Semantic similarity search
- **Large Language Model (LLM)** – Answer generation

## ✨ Features

- Upload legal documents in PDF format
- Ask questions in natural language
- Search document content using semantic similarity
- Retrieve relevant information from long documents
- Generate AI-powered answers based on the uploaded PDF
- Simple interface built with Streamlit

## 🚀 Running the Project

**1. Clone the repository**

```bash
git clone https://github.com/VON-Noor/LexiBot-Legal-RAG.git
cd LexiBot-Legal-RAG
```

**2. Create and activate a virtual environment**

```bash
python -m venv venv
```

On Windows:

```bash
venv\Scripts\activate
```

**3. Install the dependencies**

```bash
pip install -r requirements.txt
```

**4. Start the application**

```bash
streamlit run app.py
```

The application will open in your browser.

*Note: If your version uses an external LLM API, you will need to configure the required API credentials before running it.*

## 🧪 Testing

I tested LexiBot by uploading a legal PDF and asking questions such as:

- What is the purpose of this document?
- What are the responsibilities of the parties?
- What happens if an agreement is breached?
- What conditions are mentioned in the document?

The application retrieves relevant sections and generates answers based on the document's content.

## ⚠️ Limitations

LexiBot is still a student project, so there are areas that could be improved.

For example, scanned PDFs may not work properly without OCR, and the quality of the generated answers depends on the information retrieved from the document.

AI-generated answers can also be inaccurate, so important information should always be checked against the original document.

**LexiBot is designed to assist with finding legal information, not to replace professional legal advice.**

## 🔮 Future Improvements

Some features I'd like to explore in future versions include:

- Supporting scanned PDFs using OCR
- Showing page numbers and sources for generated answers
- Allowing users to upload multiple documents
- Improving the accuracy of document retrieval
- Testing the system with a wider variety of legal documents

## 🌱 What I Learned

Building LexiBot helped me understand how AI can be used to solve practical problems.

Through this project, I got hands-on experience with text processing, embeddings, vector databases and Retrieval-Augmented Generation.

It was also an opportunity to explore how different Python libraries can work together to build an AI application.

---

*Built as part of my learning journey in Artificial Intelligence and Python development.*
