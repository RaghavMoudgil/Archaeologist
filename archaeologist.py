import os
import anthropic
from rich import print

client = anthropic.Anthropic()

def analyze_project():
    print("[bold blue]Archaeologist is waking up (Adaptive Mode)...[/bold blue]")

    tools = [
        {
            "name": "list_structure",
            "description": "Lists the directory tree to help Claude plan.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "default": "."}
                }
            }
        }
    ]

    try:
        response = client.messages.create(
            model="claude-opus-4-7", # The 2026 Flagship
            max_tokens=4096,
            # NEW 2026 STANDARDS:
            thinking={"type": "adaptive"}, 
            output_config={"effort": "high"}, # Options: 'low', 'medium', 'high', 'xhigh'
            tools=tools,
            messages=[{"role": "user", "content": "Scan this folder and tell me what its purpose is."}]
        )

        for content in response.content:
            # In 2026, 'thinking' blocks are separate content types
            if content.type == "thinking":
                print(f"\n[italic cyan]Claude is thinking...[/italic cyan]")
            
            if content.type == "text":
                print(f"\n[bold green]Claude:[/bold green] {content.text}")
            
            if content.type == "tool_use":
                print(f"\n[yellow]Action:[/yellow] Calling {content.name}...")

    except Exception as e:
        print(f"[bold red]System Error:[/bold red] {e}")

if __name__ == "__main__":
    analyze_project()