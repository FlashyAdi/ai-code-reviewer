# AI Code Reviewer

AI-powered tool to automatically generate Python docstrings in multiple styles.

---

## Features

- AI-powered docstring generation (Google, NumPy, reST styles)
- PEP-257 validation
- Coverage tracking
- Interactive web interface
- Export reports (JSON/CSV/HTML)

---

## Installation

```bash
git clone https://github.com/FlashyAdi/ai-code-reviewer.git
cd ai-code-reviewer
pip install -r requirements.txt
```

**Setup API Key:**
1. Rename `env-example.txt` to `.env`
2. Add your GROQ API key
3. Run: `streamlit run streamlit_app.py`

---

## Usage

1. **Scan** - Enter project path and scan
2. **Generate** - Select function and generate docstring
3. **Apply** - Click "Accept & Apply" to update file

---

## Example

**Before:**
```python
def multiply(x, y):
    return x * y
```

**After:**
```python
def multiply(x, y):
    """
    Multiply two numbers.
    
    Args:
        x: First number
        y: Second number
    
    Returns:
        Product of x and y
    """
    return x * y
```

---

## Tech Stack

Python • Streamlit • GROQ API • AST Parser

---

## Testing

```bash
pytest tests/
```

28+ tests with 96% pass rate

---

## Author

**Aditya Sharma**

GitHub: [@FlashyAdi](https://github.com/FlashyAdi)

---

**Star this repo if you find it helpful!**
