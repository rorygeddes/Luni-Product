# Luni Web - Personal Finance Management

A beautiful, responsive web application for managing personal finances with AI-powered transaction analysis.

## Features

- 📊 **Dashboard**: Clean, modern interface with animated statistics
- 📤 **File Upload**: Upload transaction files in various formats
- 🏦 **Bank Integration**: Connect bank accounts securely
- 🤖 **AI Analysis**: Intelligent transaction categorization
- 📱 **Responsive**: Works perfectly on all devices

## Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript
- **Backend**: Python Flask (API endpoints)
- **Deployment**: Vercel
- **Styling**: Modern CSS with gradients and animations

## Local Development

```bash
# Serve the static files
python -m http.server 8000
# or
npx serve public
```

## Deployment

This project is automatically deployed to Vercel when changes are pushed to the main branch.

## Live Demo

Visit: https://luni-product.vercel.app

## Project Structure

```
├── public/
│   └── index.html          # Main application
├── api/
│   └── transactions.py     # Backend API
├── vercel.json             # Vercel configuration
└── package.json           # Project metadata
```
