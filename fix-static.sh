#!/bin/bash

# Fix static files for Cafes Iran

echo "🔧 Fixing static files..."

# Restart containers to ensure they're running
echo "🔄 Restarting containers..."
docker compose -f docker-compose.yml -f docker-compose.prod.yml restart back

# Wait for container to be ready
sleep 10

# Collect static files
echo "📦 Collecting static files..."
docker compose -f docker-compose.yml -f docker-compose.prod.yml exec back python manage.py collectstatic --no-input --clear

# Fix permissions
echo "🔐 Fixing permissions..."
sudo chown -R www-data:www-data /home/cafesiran_back/static
sudo chmod -R 755 /home/cafesiran_back/static

# Check if files exist
echo "📂 Checking static files..."
ls -la /home/cafesiran_back/static/

echo ""
echo "✅ Static files fix complete!"
echo "🔍 Test admin: https://api.cafesiran.ir/admin/"