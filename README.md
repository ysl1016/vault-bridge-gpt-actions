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

## External Access Setup with ngrok

To make your local API accessible from the internet (required for GPT Actions), you can use ngrok. Here's how to set it up:

1. **Install ngrok**
   - Download from [ngrok website](https://ngrok.com/download)
   - Sign up for a free account to get your authtoken

2. **Configure ngrok**
   ```bash
   ngrok config add-authtoken your_authtoken_here
   ```

3. **Create ngrok configuration file** (ngrok.yml)
   ```yaml
   version: "2"
   authtoken: your_authtoken_here
   tunnels:
     obsidian-bridge:
       proto: http
       addr: 8000
       basic_auth:
         - "username:password"
   ```

4. **Start ngrok tunnel**
   ```bash
   ngrok start obsidian-bridge
   ```

5. **Update OpenAPI configuration**
   - When ngrok starts, it will display a forwarding URL (e.g., `https://xxxx-xx-xx-xx-xx.ngrok.io`)
   - Update the `servers` section in `openapi.yaml`:
   ```yaml
   servers:
     - url: your_ngrok_url_here
   ```

6. **Security Considerations**
   - Always use basic authentication with ngrok
   - Keep your ngrok authtoken private
   - Don't commit ngrok.yml to version control
   - Regularly rotate your basic auth credentials
   - Monitor your ngrok dashboard for unusual activity

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
- Basic authentication through ngrok

## Error Handling

- Detailed logging
- Graceful fallbacks
- HTTP error responses

## Development

### Environment Variables

Copy `.env.example` to `.env` and update the values:

```bash
cp .env.example .env
```

### Local Testing

1. Start the Obsidian Local REST API plugin
2. Configure your `.env` file
3. Start the server
4. Test endpoints using the Swagger UI at `/docs`

### Production Deployment

For production deployment, consider:

1. Using a proper reverse proxy (nginx/Apache)
2. Implementing rate limiting
3. Setting up SSL/TLS
4. Implementing proper authentication
5. Using a process manager (PM2/Supervisor)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License