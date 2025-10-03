#!/bin/bash
# Build script for Vercel deployment

echo "Building Luni Web application for Vercel..."

# Create necessary directories
mkdir -p /tmp/uploads
mkdir -p /tmp/static

# Install dependencies
pip install -r requirements-vercel.txt

# Copy static files if they exist
if [ -d "static" ]; then
    cp -r static/* /tmp/static/ 2>/dev/null || true
fi

# Copy templates
if [ -d "templates" ]; then
    cp -r templates /tmp/ 2>/dev/null || true
fi

echo "Build completed successfully!"
