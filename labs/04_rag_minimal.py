"""
Minimal RAG (Retrieval-Augmented Generation) Pipeline Example

Corresponds to: Chapter 12.5 - 上下文工程（Context Engineering）

This is a fully runnable, dependency-free mini RAG example. It intentionally
uses a tiny in-memory corpus and lexical retrieval so beginners can see the
complete loop before replacing each part with embeddings, a vector database,
and a real LLM API.

Pipeline:
1. Retrieve: rank local document chunks by TF-IDF cosine similarity, plus a small
   exact-keyword bonus (see `retrieve`) that keeps ranking deterministic on this
   tiny corpus. The bonus is a teaching crutch, not part of TF-IDF.
2. Augment: format the top chunks into a bounded context block.
3. Generate: produce an extractive answer from the retrieved context.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import asdict, dataclass
import json


TOKEN_RE = re.compile(r"[A-Za-z0-9_]+|[\u4e00-\u9fff]")

DOCUMENTS = [
    "Transformer 的注意力机制会为查询 token 计算它与其他 token 的相关性。",
    "RAG 会先检索外部知识，再把相关片段放进提示词上下文。",
    "上下文工程关注模型能看到什么信息，而不仅仅是提示词怎么写。",
    "向量数据库适合大规模语义检索；本示例用词频检索展示最小闭环。",
    "生成答案时应引用检索到的上下文，避免编造未提供的信息。",
]


@dataclass(frozen=True)
class SearchHit:
    """A retrieved document chunk and its score."""

    rank: int
    score: float
    text: str


def tokenize(text: str) -> list[str]:
    """Tokenize English words and Chinese characters for a tiny local demo."""
    return [token.lower() for token in TOKEN_RE.findall(text)]


def build_idf(documents: list[str]) -> dict[str, float]:
    """Build an IDF table for the current in-memory corpus."""
    doc_count = len(documents)
    document_frequency: Counter[str] = Counter()
    for doc in documents:
        document_frequency.update(set(tokenize(doc)))

    return {
        token: math.log((doc_count + 1) / (count + 1)) + 1
        for token, count in document_frequency.items()
    }


def vectorize(text: str, idf: dict[str, float]) -> dict[str, float]:
    """Convert text into a sparse TF-IDF vector."""
    counts = Counter(tokenize(text))
    total = sum(counts.values()) or 1
    return {
        token: (count / total) * idf.get(token, 1.0)
        for token, count in counts.items()
    }


def cosine_similarity(a: dict[str, float], b: dict[str, float]) -> float:
    """Compute cosine similarity between two sparse vectors."""
    if not a or not b:
        return 0.0
    shared = set(a) & set(b)
    dot = sum(a[token] * b[token] for token in shared)
    norm_a = math.sqrt(sum(value * value for value in a.values()))
    norm_b = math.sqrt(sum(value * value for value in b.values()))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def retrieve(query: str, k: int = 3, documents: list[str] | None = None) -> list[SearchHit]:
    """Retrieve top-k relevant document chunks for a query."""
    corpus = documents or DOCUMENTS
    idf = build_idf(corpus)
    query_vector = vectorize(query, idf)
    explicit_terms = {token for token in tokenize(query) if len(token) > 1}

    scored = []
    for doc in corpus:
        score = cosine_similarity(query_vector, vectorize(doc, idf))
        # Teaching crutch, not part of TF-IDF: on a 3-document corpus the cosine
        # scores are too close to rank stably, so an exact-keyword hit gets +0.25.
        score += 0.25 * len(explicit_terms & set(tokenize(doc)))
        scored.append((score, doc))

    top_hits = sorted(scored, key=lambda item: item[0], reverse=True)[:k]
    return [
        SearchHit(rank=index + 1, score=score, text=text)
        for index, (score, text) in enumerate(top_hits)
        if score > 0
    ]


def augment_context(query: str, retrieved_docs: list[SearchHit]) -> str:
    """Format retrieved chunks into a prompt-style context block."""
    if not retrieved_docs:
        return f"问题：{query}\n\n未检索到相关上下文。"

    context_lines = [
        f"[{hit.rank}] score={hit.score:.3f} {hit.text}"
        for hit in retrieved_docs
    ]
    return "检索上下文：\n" + "\n".join(context_lines) + f"\n\n问题：{query}"


def generate(context: str, query: str) -> str:
    """
    Generate a conservative extractive answer.

    A production RAG system would call an LLM here. This local demo instead
    returns the most relevant retrieved snippets so the file stays runnable
    without API keys.
    """
    if "未检索到相关上下文" in context:
        return "我没有在本地知识库中找到足够依据，不能可靠回答。"

    evidence = [
        line.split(" ", 2)[-1]
        for line in context.splitlines()
        if line.startswith("[")
    ]
    joined = "；".join(evidence)
    return f"基于检索结果，{query} 的答案是：{joined}"


def rag_pipeline(query: str) -> str:
    """Complete RAG pipeline: Retrieve -> Augment -> Generate."""
    hits = retrieve(query)
    context = augment_context(query, hits)
    return generate(context, query)


def run_experiment() -> dict[str, object]:
    """Run one fixed query and return the complete retrieval trace."""
    query = "RAG 和上下文工程有什么关系？"
    hits = retrieve(query)
    context = augment_context(query, hits)
    answer = generate(context, query)
    return {
        "query": query,
        "hits": [asdict(hit) for hit in hits],
        "context": context,
        "answer": answer,
    }


def evaluate(result: dict[str, object]) -> dict[str, object]:
    """Confirm retrieval, context assembly, and grounded generation."""
    hits = result.get("hits", [])
    answer = str(result.get("answer", ""))
    checks = {
        "retrieved_relevant_context": bool(hits) and "RAG" in hits[0]["text"],
        "context_is_explicit": "检索上下文" in str(result.get("context", "")),
        "answer_is_grounded": "基于检索结果" in answer and hits[0]["text"] in answer,
    }
    return {"passed": all(checks.values()), "checks": checks}


if __name__ == "__main__":
    experiment = run_experiment()
    print(json.dumps({"result": experiment, "evaluation": evaluate(experiment)}, ensure_ascii=False, indent=2))
