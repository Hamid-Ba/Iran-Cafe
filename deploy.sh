#!/bin/bash

# Deployment script for Cafes Iran

echo "🚀 Starting Cafes Iran deployment..."

# Check if .env.prod exists
if [ ! -f ".env.prod" ]; then
    echo "❌ Error: .env.prod file not found!"
    echo "Please create .env.prod with production settings."
    exit 1
fi

# Check if production keys are set
grep -q "your-production-" .env.prod
if [ $? -eq 0 ]; then
    echo "⚠️  Warning: Found placeholder values in .env.prod"
    echo "Please update the following in .env.prod:"
    echo "  - MERCHANT_ID"
    echo "  - KAVENEGAR_API_KEY"
    echo ""
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Build and start services
echo "🏗️  Building Docker images..."
docker-compose -f docker-compose.yml -f docker-compose.prod.yml build

echo "📦 Starting services..."
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

echo "⏳ Waiting for services to be ready..."
sleep 30

# Check if services are healthy
echo "🏥 Checking service health..."
docker-compose -f docker-compose.yml -f docker-compose.prod.yml ps

echo "✅ Deployment complete!"
echo ""
echo "🌐 Your application should be available at:"
echo "   - API: http://localhost:8000 (local)"
echo "   - WebSockets: ws://localhost:8000/ws/... (local)"
echo "   - Flower (Celery monitoring): http://localhost:5555 (local)"
echo ""
echo "🔧 To set up Nginx and SSL:"
echo "   sudo ./setup-nginx.sh"
echo ""
echo "📊 To view logs:"
echo "   docker-compose -f docker-compose.yml -f docker-compose.prod.yml logs -f"
echo ""
echo "🛑 To stop services:"
echo "   docker-compose -f docker-compose.yml -f docker-compose.prod.yml down"