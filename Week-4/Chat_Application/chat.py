def format_message(name, message):
    return f"{name}: {message}"

def parse_message(message):
    """Separating Name and Message"""
    if ':' in message:
        name, msg = message.split(':', 1)
        return name.strip(), msg.strip()
    return "", message

def is_valid_name(name, existing_names):
    """Check if a name is not empty or already taken by someone."""
    return name and name not in existing_names
