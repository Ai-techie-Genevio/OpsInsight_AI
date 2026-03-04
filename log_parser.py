# log_parser.py

def read_log_file(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.readlines()
    except Exception as e:
        raise Exception(f"Error reading log file: {e}")


def extract_relevant_sections(log_lines, context_before=10, context_after=5):
    """
    Extracts ERROR and WARN lines with surrounding context.
    """

    relevant_indices = []

    for i, line in enumerate(log_lines):
        if "ERROR" in line or "WARN" in line:
            start = max(0, i - context_before)
            end = min(len(log_lines), i + context_after)
            relevant_indices.extend(range(start, end))

    # Remove duplicates & sort
    relevant_indices = sorted(set(relevant_indices))

    # Build filtered log
    filtered_log = [log_lines[i] for i in relevant_indices]

    return "".join(filtered_log);