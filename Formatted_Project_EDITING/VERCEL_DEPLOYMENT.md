# Vercel Deployment Guide - Luni Web

## 🚀 Quick Deployment to Vercel

### Prerequisites
- GitHub repository with your code
- Vercel account (free tier available)
- OpenAI API key

### Step 1: Connect to Vercel

1. **Go to [Vercel Dashboard](https://vercel.com/dashboard)**
2. **Click "New Project"**
3. **Import your GitHub repository**
4. **Select the `Formatted_Project_EDITING` folder as the root directory**

### Step 2: Configure Environment Variables

In the Vercel dashboard, go to **Settings > Environment Variables** and add:

```
OPENAI_API_KEY=your_openai_api_key_here
SECRET_KEY=your_secret_key_here
FLASK_ENV=production
PLAID_CLIENT_ID=your_plaid_client_id (optional)
PLAID_SECRET=your_plaid_secret (optional)
PLAID_ENVIRONMENT=sandbox (optional)
```

### Step 3: Configure Build Settings

**Framework Preset**: Other
**Root Directory**: `Formatted_Project_EDITING`
**Build Command**: `pip install -r api/requirements.txt`
**Output Directory**: Leave empty
**Install Command**: `pip install -r api/requirements.txt`

### Step 4: Deploy

1. **Click "Deploy"**
2. **Wait for deployment to complete**
3. **Your app will be available at**: `https://your-project-name.vercel.app`

## 🔧 Configuration Files

### vercel.json
- **Purpose**: Vercel deployment configuration
- **Routes**: All requests routed to Flask app
- **Environment**: Production settings
- **Functions**: Serverless function configuration

### requirements-vercel.txt
- **Purpose**: Python dependencies for Vercel
- **Includes**: All Flask dependencies + Gunicorn
- **Optimized**: For serverless deployment

### vercel_app.py
- **Purpose**: Vercel-optimized Flask app
- **Features**: Simplified for serverless deployment
- **Storage**: Uses /tmp for file uploads
- **Routes**: Core application routes

## 📁 File Structure for Vercel

```
Formatted_Project_EDITING/
├── vercel.json              # Vercel configuration
├── vercel_app.py           # Vercel-optimized app
├── requirements-vercel.txt # Vercel dependencies
├── build.sh               # Build script
├── .vercelignore          # Files to ignore
├── src/                   # Source code
├── templates/             # HTML templates
├── config/               # Configuration
└── docs/                 # Documentation
```

## 🔄 Automatic Deployment

### GitHub Integration
- **Automatic Deployments**: Every push to main branch triggers deployment
- **Preview Deployments**: Pull requests get preview URLs
- **Branch Deployments**: Each branch gets its own URL

### Deployment Process
1. **Push to GitHub** → Triggers Vercel build
2. **Vercel builds** → Installs dependencies and builds app
3. **Deploy** → App goes live at your domain
4. **Update** → Changes are automatically deployed

## 🛠️ Custom Domain (Optional)

### Adding Custom Domain
1. **Go to Vercel Dashboard** → Your Project → Settings
2. **Click "Domains"**
3. **Add your domain** (e.g., luniapp.com)
4. **Configure DNS** as instructed by Vercel
5. **SSL Certificate** is automatically provided

## 🔐 Environment Variables

### Required Variables
- `OPENAI_API_KEY`: Your OpenAI API key for AI parsing
- `SECRET_KEY`: Flask secret key for sessions

### Optional Variables
- `PLAID_CLIENT_ID`: For bank integration
- `PLAID_SECRET`: For bank integration
- `PLAID_ENVIRONMENT`: sandbox or production

### Setting Variables
1. **Vercel Dashboard** → Project → Settings → Environment Variables
2. **Add each variable** with its value
3. **Redeploy** for changes to take effect

## 📊 Monitoring and Analytics

### Vercel Analytics
- **Performance Metrics**: Page load times and performance
- **Usage Statistics**: User visits and page views
- **Error Tracking**: Application errors and issues
- **Real-time Monitoring**: Live application status

### Logs and Debugging
- **Function Logs**: Serverless function execution logs
- **Error Logs**: Application error tracking
- **Performance Logs**: Response times and metrics

## 🚨 Troubleshooting

### Common Issues

#### 404 NOT_FOUND Error
- **Check vercel.json** points to correct entry point (`api/index.py`)
- **Verify api/index.py** exists and imports correctly
- **Check routes configuration** in vercel.json
- **Ensure Flask app** is properly initialized in api/index.py

#### Build Failures
- **Check api/requirements.txt** for correct dependencies
- **Verify Python version** (Vercel uses Python 3.9+)
- **Check build logs** in Vercel dashboard

#### Runtime Errors
- **Check environment variables** are set correctly
- **Verify file paths** work in serverless environment
- **Check function logs** for specific errors

#### File Upload Issues
- **Use /tmp directory** for temporary files
- **Check file size limits** (Vercel has limits)
- **Implement proper cleanup** of temporary files

### Debugging Steps
1. **Check Vercel logs** in dashboard
2. **Test locally** with `vercel dev`
3. **Verify environment variables**
4. **Check file permissions** and paths

## 🔄 Updates and Maintenance

### Automatic Updates
- **GitHub Integration**: Push to main = automatic deployment
- **Preview Deployments**: Test changes before going live
- **Rollback**: Easy rollback to previous versions

### Manual Updates
1. **Make changes** to your code
2. **Push to GitHub**
3. **Vercel automatically deploys** the changes
4. **Monitor deployment** in Vercel dashboard

## 💡 Best Practices

### Performance
- **Optimize images** and static files
- **Use CDN** for static assets
- **Implement caching** where appropriate
- **Monitor performance** metrics

### Security
- **Never commit** API keys to repository
- **Use environment variables** for sensitive data
- **Implement proper** input validation
- **Regular security** updates

### Development
- **Test locally** before deploying
- **Use preview deployments** for testing
- **Monitor logs** for issues
- **Keep dependencies** updated

## 📞 Support

### Vercel Support
- **Documentation**: [Vercel Docs](https://vercel.com/docs)
- **Community**: [Vercel Community](https://github.com/vercel/vercel/discussions)
- **Support**: Available through Vercel dashboard

### Project Support
- **Issues**: Create GitHub issues for bugs
- **Features**: Submit feature requests
- **Documentation**: Check project README and docs

Your Luni Web application is now ready for Vercel deployment! 🎉
