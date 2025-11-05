#!/bin/bash

# Nginx + Certbot setup script for Cafes Iran

echo "🌐 Setting up Nginx and SSL for Cafes Iran..."

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo "❌ This script must be run as root (use sudo)"
   exit 1
fi

# Install nginx and certbot
echo "📦 Installing Nginx and Certbot..."
apt update
apt install -y nginx certbot python3-certbot-nginx

# Copy nginx configuration
echo "⚙️  Setting up Nginx configuration..."
cp nginx-cafesiran.conf /etc/nginx/sites-available/cafesiran
ln -sf /etc/nginx/sites-available/cafesiran /etc/nginx/sites-enabled/

# Remove default nginx site
rm -f /etc/nginx/sites-enabled/default

# Test nginx configuration
echo "🔍 Testing Nginx configuration..."
nginx -t
if [ $? -ne 0 ]; then
    echo "❌ Nginx configuration test failed!"
    exit 1
fi

# Start nginx
echo "🚀 Starting Nginx..."
systemctl enable nginx
systemctl start nginx

# Test that the site works without SSL first
echo "🔍 Testing HTTP site..."
curl -I http://api.cafesiran.ir 2>/dev/null | head -1 || echo "⚠️  Site not reachable via HTTP yet"

# Get SSL certificate
echo "🔒 Getting SSL certificate..."
echo "⚠️  IMPORTANT: Make sure your domain (api.cafesiran.ir) points to this server's IP!"
echo "⚠️  Test first: http://api.cafesiran.ir should work before adding SSL"
read -p "Continue with certificate generation? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Create webroot directory for certbot
    mkdir -p /var/www/html
    
    # Get certificate and automatically update nginx config
    certbot --nginx -d api.cafesiran.ir --redirect
    
    if [ $? -eq 0 ]; then
        # Set up auto-renewal
        echo "⚡ Setting up certificate auto-renewal..."
        (crontab -l 2>/dev/null; echo "0 12 * * * /usr/bin/certbot renew --quiet") | crontab -
        
        echo "✅ SSL certificate installed and auto-renewal configured!"
        echo "🔒 Your site is now available at: https://api.cafesiran.ir"
    else
        echo "❌ SSL certificate generation failed!"
        echo "💡 Your site is still available at: http://api.cafesiran.ir"
    fi
else
    echo "⚠️  SSL certificate generation skipped."
    echo "💡 Your site is available at: http://api.cafesiran.ir"
    echo "🔒 Run this when ready: certbot --nginx -d api.cafesiran.ir --redirect"
fi

echo ""
echo "🎉 Nginx setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Make sure Docker services are running"
echo "2. Test your API: https://api.cafesiran.ir"
echo "3. Test WebSockets: wss://api.cafesiran.ir/ws/..."
echo ""
echo "📊 Useful commands:"
echo "  - Check nginx status: systemctl status nginx"
echo "  - Reload nginx: systemctl reload nginx"
echo "  - Check SSL: certbot certificates"