#!/bin/bash

# Generate migrations using Docker container

echo "🔄 Generating Django migrations using Docker..."

# Build a temporary container to generate migrations
echo "🏗️ Building Docker image..."
docker build -t cafesiran-temp .

# Run makemigrations in a temporary container
echo "📝 Running makemigrations..."
docker run --rm \
  -v "$(pwd):/home/app/cafesiran" \
  --env-file .env \
  cafesiran-temp \
  python manage.py makemigrations --no-input

# Check if migrations were created
if [ $? -eq 0 ]; then
    echo "✅ Migrations generated successfully!"
    echo ""
    echo "📋 Next steps:"
    echo "1. Review the generated migration files"
    echo "2. Commit the migration files to git (if any new ones were created)"
    echo "3. Run ./deploy.sh to deploy with migrations"
else
    echo "❌ Error generating migrations!"
    exit 1
fi

# Clean up temporary image
echo "🧹 Cleaning up..."
docker rmi cafesiran-temp