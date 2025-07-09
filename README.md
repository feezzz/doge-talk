```markdown
# n8n-qa 知识库问答服务

本项目基于 FastAPI + LangChain + FAISS 向量数据库，实现了一个本地知识库问答系统。  
知识库来源于本地或 Google Drive 中的多文本文件，通过文本向量化构建索引，并结合大模型回答用户问题。

---

## 项目结构

```

n8n-qa/
├── data/                      # 存放所有 txt 文本文件的目录
├── faiss_index/               # 向量索引文件夹（运行后生成）
├── build_vector_db.py         # 文本加载、向量构建和保存的脚本
├── qa_server.py               # FastAPI 服务器，提供问答接口
├── requirements.txt           # 依赖包清单
└── README.md                  # 项目说明文档

````

---

## 环境准备

1. 安装 Python 3.10+
2. 建议创建并激活虚拟环境：

```bash
python -m venv venv
source venv/bin/activate    # Linux/macOS
venv\Scripts\activate       # Windows
````

3. 安装依赖：

```bash
pip install -r requirements.txt
```

---

## 使用步骤

### 1. 准备文本数据

将你的 `.txt` 文件放到 `data/` 目录中，每个文件一份知识文本。

---

### 2. 构建向量数据库

运行脚本，将文本切分、向量化并构建 FAISS 索引：

```bash
python build_vector_db.py
```

成功后会在 `faiss_index/` 目录生成索引文件。

---

### 3. 启动问答服务

启动 FastAPI 服务器：

```bash
uvicorn qa_server:app --reload --port 8000
##n8n HTTP Request 里写的地址是 http://127.0.0.1:8000/ask，它会去访问容器自己内部的 8000 端口，而不是宿主机的。
uvicorn qa_server:app --host 0.0.0.0 --port 8000

#在 n8n HTTP Request 节点使用宿主机的局域网 IP
url:http://192.168.1.113:8000/ask
```

服务器启动后，访问接口文档：

```
http://127.0.0.1:8000/docs
```

使用 `/ask` 接口，发送带有 JSON 格式的提问：

```json
{
  "question": "你的问题内容"
}
```

接口会返回基于知识库和大模型的回答。

---

## 重要说明

* 项目使用了 `HuggingFaceEmbeddings`，推荐升级到 `langchain-huggingface` 包，避免未来版本弃用问题。
* 向量数据库使用 `faiss`，请根据你的环境安装 `faiss-cpu` 或 `faiss-gpu`。
* LLM 目前接入 DeepSeek API，需要配置 `OPENAI_API_KEY` 环境变量。
* `faiss_index` 是二进制索引文件，请勿随意修改。

---

## 依赖清单（requirements.txt 示例）

```
fastapi
uvicorn
langchain
langchain-community
langchain-huggingface
sentence-transformers
faiss-cpu
transformers
torch
pydantic
```

---

## 后续扩展

* 集成 n8n 触发器，实现自动调用问答接口
* 支持多语言知识库文本加载
* 前端网页聊天界面开发

---

## 联系

如有疑问，欢迎提 issue 或联系作者。

---

祝你项目顺利，玩转知识库问答！🚀

```
```
