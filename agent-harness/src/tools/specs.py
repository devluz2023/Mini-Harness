TOOL_SPECS = [
    {
        "name": "list_files",
        "description": "List the project files.",
        "input_schema": {"type": "object", "properties": {}}
    },
    {
        "name": "read_file",
        "description": "Read one project file.",
        "input_schema": {
            "type": "object",
            "properties": {"path": {"type": "string"}},
            "required": ["path"]
        }
    },
    {
        "name": "write_file",
        "description": "Replace a project file with new full content.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "content": {"type": "string"}
            },
            "required": ["path", "content"]
        }
    },
    {
        "name": "run_tests",
        "description": "Run the project's tests.",
        "input_schema": {"type": "object", "properties": {}}
    },
    {
        "name": "finish",
        "description": "Say the task is done. The harness checks it first.",
        "input_schema": {
            "type": "object",
            "properties": {"summary": {"type": "string"}},
            "required": ["summary"]
        }
    },
]
