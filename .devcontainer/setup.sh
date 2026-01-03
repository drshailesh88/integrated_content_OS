#!/bin/bash
# Codespace setup script - runs on first creation

echo "🚀 Setting up Dr. Shailesh Content OS in Codespace..."

# Install Python dependencies
if [ -f requirements.txt ]; then
    echo "📦 Installing Python packages..."
    pip install -r requirements.txt --quiet
fi

# Install PubMed MCP dependencies
if [ -d pubmed-mcp-server ]; then
    echo "📚 Setting up PubMed MCP..."
    cd pubmed-mcp-server
    npm install --silent
    cd ..
fi

# Check if .env exists, if not create from template
if [ ! -f .env ]; then
    echo "⚙️  Creating .env from template..."
    echo "⚠️  IMPORTANT: Add your API keys to .env or use Codespaces Secrets"
    cp .env.example .env
fi

# Make scripts executable
chmod +x publish.py quick-publish.sh 2>/dev/null

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "   1. If using Codespaces Secrets: They're already loaded as env vars"
echo "   2. If using .env file: Edit .env and add your API keys"
echo "   3. Test: python publish.py 'Test' 'Hello from Codespace!'"
echo ""
echo "💡 Your Claude Code subscription works here - no API costs!"
echo ""
