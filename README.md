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

3. **Start ngrok tunnel**
   ```bash
   ngrok http 8000
   ```

   > **Important Note for Free Tier Users:**
   > - The free tier of ngrok generates a new random domain each time you start the tunnel
   > - The URL will look like `https://xxxx-xx-xx-xx-xx.ngrok.io`
   > - You'll need to update your OpenAPI configuration and GPT Actions configuration each time you restart ngrok
   > - For persistent domains, consider upgrading to a paid ngrok plan or wait for our upcoming Cloudflare Tunnel integration

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
   - Consider using ngrok's paid features or waiting for Cloudflare Tunnel integration for:
     - Custom/fixed domains
     - Additional security features
     - Persistent connections
     - Team collaboration

## Upcoming Features: Cloudflare Tunnel Integration 🚧

We are actively working on integrating Cloudflare Tunnels as an alternative to ngrok. This will provide several advantages:

### Planned Features
- **Persistent Custom Domains**: Set up a permanent domain for your API
- **Free Tier Benefits**:
  - Custom subdomain support
  - Unlimited tunnels
  - No random domain changes
  - Zero-trust security model
- **Enhanced Security**:
  - Built-in SSL/TLS encryption
  - Zero-trust network access
  - DDoS protection
  - WAF (Web Application Firewall)
- **Improved Performance**:
  - Global CDN network
  - Automatic optimization
  - Low-latency connections

### Implementation Timeline
- Initial Cloudflare integration: Q2 2024
- Beta testing phase: Q3 2024
- Stable release: Q4 2024

Stay tuned for updates! Star this repository to get notified when the Cloudflare integration is released.

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
6. Using a paid ngrok plan or waiting for our Cloudflare Tunnel integration

### Troubleshooting

1. **New ngrok URL not working:**
   - Verify the ngrok tunnel is running
   - Check if you've updated the OpenAPI configuration
   - Ensure your GPT Actions are using the new URL
   - Test the connection using the `/ping` endpoint

2. **Connection Issues:**
   - Confirm the local server is running on port 8000
   - Check ngrok status in the terminal
   - Verify your firewall settings
   - Ensure your ngrok authtoken is valid

## Roadmap

1. **Current Phase**
   - Basic API functionality ✅
   - ngrok integration ✅
   - Documentation ✅

2. **Next Phase (In Progress)**
   - Cloudflare Tunnel integration 🚧
   - Enhanced security features 🚧
   - Performance optimizations 🚧

3. **Future Plans**
   - Advanced search capabilities
   - Real-time updates
   - Multiple vault support
   - Collaborative features

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License