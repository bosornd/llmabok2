# llmabok2

* google adk
```sh
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

.env 파일 필요.

* mcp
```sh
node.js
npx -y @modelcontextprotocol/inspector
npx -y @modelcontextprotocol/server-everything
@modelcontextprotocol/server-filesystem
```

* qdrant
```sh
docker pull qdrant/qdrant
qdrant
```