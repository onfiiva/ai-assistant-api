def execute_action(action: str, action_input: str) -> str:
    if action == "search":
        return f"Search result for: {action_input}"

    raise ValueError(f"Unknown action: {action}")
