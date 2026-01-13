def format_docstring(data: dict, style: str) -> str:
    lines = []
    lines.append(data["summary"])
    lines.append("")

    if data["args"]:
        if style == "google":
            lines.append("Args:")
            for k, v in data["args"].items():
                lines.append(f"    {k}: {v}")
        elif style == "numpy":
            lines.append("Parameters")
            lines.append("----------")
            for k, v in data["args"].items():
                lines.append(f"{k}")
                lines.append(f"    {v}")
        else:  # rest
            for k, v in data["args"].items():
                lines.append(f":param {k}: {v}")

    if data["returns"]:
        lines.append("")
        if style == "google":
            lines.append("Returns:")
            lines.append(f"    {data['returns']}")
        elif style == "numpy":
            lines.append("Returns")
            lines.append("-------")
            lines.append(data["returns"])
        else:
            lines.append(f":return: {data['returns']}")

    if data["raises"]:
        lines.append("")
        lines.append("Raises:")
        for k, v in data["raises"].items():
            lines.append(f"    {k}: {v}")

    return "\n".join(lines)
