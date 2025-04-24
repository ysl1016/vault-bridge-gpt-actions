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

1. Start the FastAPI server:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The server will start on `http://localhost:8000`

2. Start the Cloudflare tunnel (make sure you have cloudflared installed):
```bash
cloudflared tunnel --url http://localhost:8000
```

This will create a secure tunnel to your local FastAPI server, making it accessible from the internet with a stable URL.

## External Access Setup

### Option 1: Using Cloudflare Tunnel (Recommended)

1. **Install cloudflared**
   - Download from [Cloudflare website](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation)
   - Follow the installation instructions for your operating system

2. **Start the tunnel**
   ```bash
   cloudflared tunnel --url http://localhost:8000
   ```

   > **Benefits of Cloudflare Tunnel:**
   > - Free permanent URL
   > - Built-in SSL/TLS encryption
   > - DDoS protection
   > - No need to update URLs when restarting
   > - Better security and performance

### Option 2: Using ngrok

To make your local API accessible from the internet using ngrok, follow these steps:

1. **Install ngrok**
   - Download from [ngrok website](https://ngrok.com/download)
   - Sign up for a free account to get your authtoken

2. **Configure ngrok**
   ```bash
   ngrok config add-authtoken your_authtoken_here
   ```

3. **Start ngrok tunnel**
   ```bash
   ngrok http 8000
   ```

   > **Important Note for Free Tier Users:**
   > - The free tier of ngrok generates a new random domain each time you start the tunnel
   > - The URL will look like `https://xxxx-xx-xx-xx-xx.ngrok.io`
   > - You'll need to update your OpenAPI configuration and GPT Actions configuration each time you restart ngrok
   > - For persistent domains, consider upgrading to a paid ngrok plan or using Cloudflare Tunnel

4. **Update OpenAPI configuration**
   - When ngrok starts, it will display a forwarding URL
   - Update the `servers` section in `openapi.yaml` with the new URL:
   ```yaml
   servers:
     - url: your_new_ngrok_url_here  # Update this every time you restart ngrok
   ```

5. **Using with GPT Actions**
   - After starting ngrok, copy the new HTTPS URL
   - Update your GPT Actions configuration with the new URL
   - Remember to update this URL whenever you restart ngrok (free tier limitation)
   - Test the connection using the `/ping` endpoint before configuring GPT Actions

6. **Security Considerations**
   - The free tier doesn't support custom domains or persistent URLs
   - Each new ngrok session will generate a new URL
   - Monitor your ngrok dashboard for unusual activity
   - Consider using ngrok's paid features or Cloudflare Tunnel for:
     - Custom/fixed domains
     - Additional security features
     - Persistent connections
     - Team collaboration

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
- Basic authentication through ngrok (available in paid tiers)

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

### Troubleshooting

1. **Server Connection Issues:**
   - Verify the FastAPI server is running on port 8000
   - Check if the server is accessible at http://localhost:8000
   - Ensure your firewall allows the connection
   - Check the server logs for any errors

2. **Tunnel Connection Issues:**
   - For Cloudflare Tunnel:
     - Verify cloudflared is running
     - Check the tunnel logs for connection status
     - Ensure your Cloudflare account is properly configured
   - For ngrok:
     - Check ngrok status in the terminal
     - Verify your ngrok authtoken is valid
     - Ensure the tunnel is properly forwarding to port 8000

## Roadmap

1. **Current Phase**
   - Basic API functionality ✅
   - Cloudflare Tunnel integration ✅
   - Documentation ✅

2. **Next Phase (In Progress)**
   - Enhanced security features 🚧
   - Performance optimizations 🚧
   - Advanced authentication options 🚧

3. **Future Plans**
   - Advanced search capabilities
   - Real-time updates
   - Multiple vault support
   - Collaborative features

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License