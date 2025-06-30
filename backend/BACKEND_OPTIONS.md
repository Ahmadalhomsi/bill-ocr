# Backend Options for GPT-4o Bill Analysis

You now have three different ways to use the GPT-4o bill analysis:

## Option 1: Command Line Tool (Simplest)

Use `simple_analyzer.py` as a standalone command-line tool:

```bash
# Install minimal dependencies
pip install -r requirements-simple.txt

# Analyze a bill
python simple_analyzer.py path/to/bill.jpg

# Save results to file
python simple_analyzer.py path/to/bill.jpg --output results.json --pretty

# Verbose output
python simple_analyzer.py path/to/bill.jpg --verbose
```

**Pros:**
- ✅ No web server needed
- ✅ Minimal dependencies
- ✅ Easy to integrate into scripts
- ✅ Direct API usage

**Cons:**
- ❌ No web interface
- ❌ Manual file handling

## Option 2: Simple HTTP Server (Middle Ground)

Use `simple_server.py` for a basic web API without FastAPI:

```bash
# Install minimal dependencies
pip install -r requirements-simple.txt

# Start server
python simple_server.py
```

**Pros:**
- ✅ Web API available
- ✅ Works with existing frontend
- ✅ No FastAPI dependency
- ✅ Built-in Python HTTP server

**Cons:**
- ❌ Less robust than FastAPI
- ❌ Basic error handling
- ❌ No automatic documentation

## Option 3: FastAPI Server (Full Featured)

Use `main.py` for the full FastAPI experience:

```bash
# Install all dependencies
pip install -r requirements.txt

# Start server
python main.py
```

**Pros:**
- ✅ Full-featured web API
- ✅ Automatic documentation
- ✅ Better error handling
- ✅ CORS support
- ✅ Request validation

**Cons:**
- ❌ More dependencies
- ❌ Slightly more complex

## Recommendation

- **For scripts/automation**: Use Option 1 (Command Line)
- **For simple web app**: Use Option 2 (Simple HTTP Server)
- **For production app**: Use Option 3 (FastAPI)

## Configuration

All options use the same configuration:

1. Create `.env` file:
```
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

2. Update `config.py` if needed

## Frontend Compatibility

Options 2 and 3 work with the existing Next.js frontend. Option 1 is command-line only.

## Example Usage

### Command Line:
```bash
python simple_analyzer.py test-images/bill1.jpg --pretty
```

### Simple Server:
```bash
python simple_server.py
# Then use frontend at http://localhost:3000
```

### FastAPI Server:
```bash
python main.py
# Then use frontend at http://localhost:3000
# API docs at http://localhost:8001/docs
```
