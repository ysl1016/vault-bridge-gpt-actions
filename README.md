# Vault Bridge for GPT Actions

Obsidian vault bridge API middleware - Connects Obsidian local REST API with external services

## Overview

This API middleware serves as a bridge between Obsidian's local REST API and external services (like GPT actions). It provides a robust interface for accessing and managing Obsidian vault contents through HTTP endpoints.

## Features

- Full Obsidian vault access
- Note search functionality
- File content reading and writing
- Fallback to file system when API fails
- CORS support
- Detailed error logging
- OpenAPI documentation

## Setup

1. Create a virtual environment:
```bash
python -m venv .venv
```

2. Activate the virtual environment:
- Windows:
```bash
.venv\Scripts\activate
```
- Unix/MacOS:
```bash
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your configuration:
```env
OBSIDIAN_API_URL=http://127.0.0.1:27123
OBSIDIAN_API_KEY=your_api_key_here
VAULT_PATH=/path/to/your/vault
```

## Running the Server

```bash
uvicorn main:app --reload
```

The server will start on `http://localhost:8000`

## API Endpoints

- `GET /search` - Search notes by keyword
- `GET /vault` - List all markdown files
- `GET /read-file` - Read specific note content
- `POST /save` - Save or update note

For full API documentation, visit `/docs` when the server is running.

## Security

- API key authentication
- CORS middleware
- Environment variable configuration

## Error Handling

- Detailed logging
- Graceful fallbacks
- HTTP error responses

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License