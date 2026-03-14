#!/usr/bin/env python3
"""Convert .github/agents/ VS Code Copilot agents to .claude/ Claude Code format."""

import os
import re
import shutil
import json
import yaml

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE, ".github", "agents")
DST_DIR = os.path.join(BASE, ".claude")

# VS Code tool name -> Claude Code tool name mapping
TOOL_MAP = {
    "vscode": None,       # No equivalent
    "execute": "Bash",
    "read": "Read",
    "agent": "Agent",
    "browser": "WebFetch",
    "edit": "Edit",
    "search": "Grep",
    "web": "WebSearch",
    "todo": None,          # No equivalent
}


def parse_frontmatter(content: str):
    """Parse YAML frontmatter from markdown content."""
    if not content.startswith("---"):
        return {}, content
    end = content.find("---", 3)
    if end == -1:
        return {}, content
    fm_text = content[3:end].strip()
    body = content[end + 3:].strip()
    try:
        fm = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError:
        fm = {}
    return fm, body


def map_tools(vscode_tools: list) -> list:
    """Map VS Code tool names to Claude Code tool names."""
    mapped = set()
    for t in vscode_tools:
        t = t.strip().lower()
        claude_tool = TOOL_MAP.get(t)
        if claude_tool:
            mapped.add(claude_tool)
    # Always add Read and Grep for agents that search
    mapped.add("Read")
    mapped.add("Grep")
    mapped.add("Glob")
    return sorted(mapped)


def build_claude_frontmatter(fm: dict, is_orchestrator: bool = False) -> str:
    """Build Claude Code agent YAML frontmatter."""
    name = fm.get("name", "unknown")
    desc = fm.get("description", "")
    tools = fm.get("tools", [])
    
    claude_tools = map_tools(tools if isinstance(tools, list) else [])
    
    lines = ["---"]
    lines.append(f"name: {name}")
    # Quote description if it has special chars
    if ":" in desc or "'" in desc or '"' in desc or "\n" in desc:
        lines.append(f"description: '{desc}'")
    else:
        lines.append(f"description: {desc}")
    lines.append(f"tools: [{', '.join(claude_tools)}]")
    
    if is_orchestrator or "orchestrator" in name:
        lines.append("maxTurns: 200")
    elif "writer" in name or "verification" in name or "fuzzing" in name:
        lines.append("maxTurns: 100")
    else:
        lines.append("maxTurns: 50")
    
    lines.append("---")
    return "\n".join(lines)


def fix_resource_refs(body: str, agent_name: str) -> str:
    """Fix resource references to point to .claude/skills/<name>/resources/."""
    # Replace relative resource references
    body = body.replace(
        "resources/",
        f"../skills/{agent_name}/resources/"
    )
    # Fix double replacements 
    body = body.replace(
        f"../skills/{agent_name}/../skills/{agent_name}/resources/",
        f"../skills/{agent_name}/resources/"
    )
    return body


def convert_agent(src_path: str, agent_name: str):
    """Convert a single VS Code agent file to Claude Code format."""
    with open(src_path, "r") as f:
        content = f.read()
    
    fm, body = parse_frontmatter(content)
    is_orch = agent_name == "audit-orchestrator"
    
    # Build Claude Code agent file
    new_fm = build_claude_frontmatter(fm, is_orchestrator=is_orch)
    
    # Write agent file
    agent_dir = os.path.join(DST_DIR, "agents")
    os.makedirs(agent_dir, exist_ok=True)
    agent_path = os.path.join(agent_dir, f"{agent_name}.md")
    with open(agent_path, "w") as f:
        f.write(new_fm + "\n\n" + body)
    
    print(f"  Agent: {agent_path}")


def create_skill(agent_name: str, fm: dict, body: str):
    """Create a SKILL.md for an agent."""
    skill_dir = os.path.join(DST_DIR, "skills", agent_name)
    os.makedirs(skill_dir, exist_ok=True)
    
    name = fm.get("name", agent_name)
    desc = fm.get("description", "")
    tools = fm.get("tools", [])
    claude_tools = map_tools(tools if isinstance(tools, list) else [])
    
    lines = ["---"]
    lines.append(f"name: {name}")
    if ":" in desc or "'" in desc or '"' in desc:
        lines.append(f'description: "{desc}"')
    else:
        lines.append(f"description: {desc}")
    lines.append(f"allowed-tools: [{', '.join(claude_tools)}]")
    lines.append("---")
    lines.append("")
    lines.append(body)
    
    skill_path = os.path.join(skill_dir, "SKILL.md")
    with open(skill_path, "w") as f:
        f.write("\n".join(lines))
    
    print(f"  Skill: {skill_path}")


def copy_resources():
    """Copy resource files to a shared resources directory under .claude/."""
    src_res = os.path.join(SRC_DIR, "resources")
    dst_res = os.path.join(DST_DIR, "resources")
    
    if os.path.exists(src_res):
        if os.path.exists(dst_res):
            shutil.rmtree(dst_res)
        shutil.copytree(src_res, dst_res)
        print(f"  Resources copied to: {dst_res}")


def create_settings():
    """Create .claude/settings.json with permissions."""
    settings = {
        "permissions": {
            "allow": [
                "Read",
                "Grep",
                "Glob",
                "Agent",
                "WebFetch",
                "WebSearch",
                "Bash(find *)",
                "Bash(grep *)",
                "Bash(rg *)",
                "Bash(wc *)",
                "Bash(cat *)",
                "Bash(head *)",
                "Bash(tail *)",
                "Bash(ls *)",
                "Bash(tree *)",
                "Bash(python3 *)",
                "Bash(forge *)",
                "Bash(anchor *)",
                "Bash(cargo *)",
                "Bash(sui *)",
                "Bash(go *)",
                "Bash(npx *)",
                "Bash(mkdir *)",
                "Bash(cp *)",
                "Bash(mv *)",
                "Bash(medusa *)",
                "Bash(halmos *)",
                "Bash(certoraRun *)",
                "Bash(cd *)",
                "Bash(pip *)",
                "Bash(pip3 *)",
                "Edit",
                "Write"
            ],
            "deny": [
                "Bash(rm -rf /)",
                "Bash(sudo *)",
                "Bash(chmod 777 *)"
            ]
        }
    }
    settings_path = os.path.join(DST_DIR, "settings.json")
    with open(settings_path, "w") as f:
        json.dump(settings, f, indent=2)
    print(f"  Settings: {settings_path}")


def main():
    os.makedirs(DST_DIR, exist_ok=True)
    
    # 1. Copy all resource files
    print("\n=== Copying Resources ===")
    copy_resources()
    
    # 2. Convert each agent
    print("\n=== Converting Agents ===")
    agent_files = sorted([
        f for f in os.listdir(SRC_DIR) 
        if f.endswith(".md") and os.path.isfile(os.path.join(SRC_DIR, f))
    ])
    
    for fname in agent_files:
        agent_name = fname.replace(".md", "")
        src_path = os.path.join(SRC_DIR, fname)
        print(f"\nProcessing: {agent_name}")
        
        with open(src_path, "r") as f:
            content = f.read()
        fm, body = parse_frontmatter(content)
        
        # Create agent file
        convert_agent(src_path, agent_name)
        
        # Create skill file
        create_skill(agent_name, fm, body)
    
    # 3. Create settings.json
    print("\n=== Creating Settings ===")
    create_settings()
    
    print(f"\n=== Done! Converted {len(agent_files)} agents ===")
    print(f"Output: {DST_DIR}")


if __name__ == "__main__":
    main()
