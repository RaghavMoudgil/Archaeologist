# api.py
import os
import anthropic
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Allow Next.js frontend to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = anthropic.Anthropic()

class ScanRequest(BaseModel):
    path: str

# Our actual local function
def get_local_structure(path: str):
    tree = []
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if not d.startswith(('.', 'venv', 'node_modules'))]
        level = root.replace(path, '').count(os.sep)
        indent = ' ' * 4 * level
        tree.append(f"{indent}{os.path.basename(root)}/")
        for f in files:
            if not f.startswith('.'):
                tree.append(f"{indent}    {f}")
    return "\n".join(tree)

@app.post("/api/analyze")
def analyze_project(req: ScanRequest):
    tools = [{
        "name": "list_structure",
        "description": "Lists the directory tree.",
        "input_schema": {
            "type": "object",
            "properties": {"path": {"type": "string"}}
        }
    }]

    # Step 1: Ask Claude
    response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=4096,
        thinking={"type": "adaptive"},
        output_config={"effort": "high"},
        tools=tools,
        messages=[{"role": "user", "content": f"Scan this folder: {req.path} and tell me what its purpose is."}]
    )

    # Step 2: Handle Tool Call & Return Final Result
    final_text = ""
    for content in response.content:
        if content.type == "text":
            final_text += content.text + "\n"
        elif content.type == "tool_use" and content.name == "list_structure":
            # Actually execute the tool!
            structure = get_local_structure(req.path)
            
            # Send the result back to Claude for the final summary
            follow_up = client.messages.create(
                model="claude-opus-4-7",
                max_tokens=4096,
                messages=[
                    {"role": "user", "content": f"Scan this folder: {req.path} and tell me what its purpose is."},
                    {"role": "assistant", "content": response.content},
                    {"role": "user", "content": [{"type": "tool_result", "tool_use_id": content.id, "content": structure}]}
                ]
            )
            final_text += follow_up.content[0].text

    return {"status": "success", "analysis": final_text}

if __name__ == "__main__":
    import uvicorn
    # Runs the API on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8080)