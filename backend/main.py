import os

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from collections import defaultdict, deque

from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Pipeline(BaseModel):
    nodes: list
    edges: list


@app.get("/")
def read_root():
    return {"Ping": "Pong"}


@app.post("/pipelines/parse")
def parse_pipeline(pipeline: Pipeline):
    nodes = pipeline.nodes
    edges = pipeline.edges

    num_nodes = len(nodes)
    num_edges = len(edges)

    graph = defaultdict(list)
    indegree = defaultdict(int)
    degree = defaultdict(int)

    node_ids = {node["id"] for node in nodes}

    for node_id in node_ids:
        indegree[node_id] = 0

    for edge in edges:
        source = edge["source"]
        target = edge["target"]

        graph[source].append(target)
        indegree[target] += 1

        degree[source] += 1
        degree[target] += 1

    queue = deque([n for n in node_ids if indegree[n] == 0])

    visited = 0

    while queue:
        node = queue.popleft()
        visited += 1

        for nxt in graph[node]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)

    is_dag = visited == num_nodes

    # A node with zero edges touching it isn't part of the pipeline.
    # A lone node with no others to connect to doesn't count as disconnected.
    is_connected = num_nodes <= 1 or all(degree[n] > 0 for n in node_ids)

    return {
        "num_nodes": num_nodes,
        "num_edges": num_edges,
        "is_dag": is_dag,
        "is_connected": is_connected,
    }