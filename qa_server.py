from fastapi import FastAPI
from pydantic import BaseModel  # ✅ 新增
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
import os

app = FastAPI()

# ✅ 定义输入数据模型
class Question(BaseModel):
    question: str

# 设置 DeepSeek API Key
os.environ["OPENAI_API_KEY"] = ""

# 加载向量数据库
embedding_model = HuggingFaceEmbeddings(model_name="GanymedeNil/text2vec-base-chinese")
db = FAISS.load_local("faiss_index", embedding_model, allow_dangerous_deserialization=True)

# 设置 LLM 模型
llm = ChatOpenAI(
    openai_api_base="https://api.deepseek.com/v1",
    openai_api_key=os.environ["OPENAI_API_KEY"],
    model_name="deepseek-chat",
    temperature=0.3
)

qa = RetrievalQA.from_chain_type(llm=llm, retriever=db.as_retriever())

# ✅ 使用 pydantic 接收 POST 请求
@app.post("/ask")
async def ask_question(data: Question):
    result = qa.run(data.question)
    return {"answer": result}
