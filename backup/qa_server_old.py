from fastapi import FastAPI, Request
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI  # ✅ 推荐新版导入方式
import os

app = FastAPI()

# ✅ 设置 DeepSeek API Key 和 base url
os.environ["OPENAI_API_KEY"] = "sk-ee50c75ee62449a7b68e20638e723284"
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
OPENAI_API_BASE = "https://api.deepseek.com/v1"

# ✅ 加载向量数据库
embedding_model = HuggingFaceEmbeddings(model_name="GanymedeNil/text2vec-base-chinese")
db = FAISS.load_local("../faiss_index", embedding_model, allow_dangerous_deserialization=True)

# ✅ 配置 LLM（DeepSeek 兼容 OpenAI 协议）
llm = ChatOpenAI(
    openai_api_base=OPENAI_API_BASE,
    openai_api_key=OPENAI_API_KEY,
    model_name="deepseek-chat",
    temperature=0.3
)

# ✅ 构建检索问答链
qa = RetrievalQA.from_chain_type(llm=llm, retriever=db.as_retriever())

@app.post("/ask")
async def ask_question(request: Request):
    try:
        data = await request.json()
        question = data.get("question", "").strip()

        if not question:
            return {"error": "question is required."}

        answer = qa.run(question)
        return {"answer": answer}

    except Exception as e:
        return {"error": str(e)}
