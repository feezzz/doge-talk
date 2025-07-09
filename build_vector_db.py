import os
import hashlib
import json
from tqdm import tqdm
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

CACHE_PATH = "vector_cache.json"
DB_PATH = "faiss_index"
DATA_DIR = "data"

# 加载本地缓存
if os.path.exists(CACHE_PATH):
    with open(CACHE_PATH, "r", encoding="utf-8") as f:
        file_hashes = json.load(f)
else:
    file_hashes = {}

# 初始化嵌入模型
embedding_model = HuggingFaceEmbeddings(
    model_name="GanymedeNil/text2vec-base-chinese"
)

# 文本切分器
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

all_splits = []
updated_hashes = {}

def md5(filepath):
    with open(filepath, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

# 遍历 data 文件夹
print(f"📂 正在扫描 data/ 文件夹...")
for filename in tqdm(os.listdir(DATA_DIR), desc="读取文本文件"):
    if not filename.endswith(".txt"):
        continue

    path = os.path.join(DATA_DIR, filename)
    file_md5 = md5(path)
    updated_hashes[filename] = file_md5

    # 如果 hash 一致，说明文件没变，跳过
    if filename in file_hashes and file_hashes[filename] == file_md5:
        continue

    loader = TextLoader(path, encoding="utf-8")
    docs = loader.load()
    split_docs = text_splitter.split_documents(docs)
    all_splits.extend(split_docs)

# 加载已有数据库
if os.path.exists(DB_PATH):
    print("📥 加载已有向量数据库...")
    db = FAISS.load_local(DB_PATH, embedding_model)
else:
    db = None

# 添加新数据
if all_splits:
    print(f"📌 新增 {len(all_splits)} 条文档片段，正在生成向量...")
    new_db = FAISS.from_documents(all_splits, embedding_model)
    if db:
        db.merge_from(new_db)
    else:
        db = new_db
    db.save_local(DB_PATH)
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(updated_hashes, f, ensure_ascii=False, indent=2)
    print("✅ 新向量数据已保存完成！")
else:
    print("✅ 没有发现新的 txt 文件或文件内容未变化，无需更新。")
