# Quick Start Guide - GPT-4o Bill Analysis (Secure)

## 🚀 Super Quick Setup (2 minutes)

### 1. Get your OpenAI API Key
- Go to https://platform.openai.com/api-keys
- Create a new API key
- Copy the key (starts with `sk-proj-...`)

### 2. Install and configure
```bash
npm install
cp .env.local.example .env.local
# Edit .env.local and add your API key:
# OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 3. Start the app
```bash
npm run dev
```

### 4. Use the app
- Go to http://localhost:3000
- Upload a bill image
- Click "Analyze with GPT-4o"
- View the extracted data!

## 🔒 **SECURITY FIXED!**

✅ **Your API key is now secure:**
- **Server-side only**: API key is never exposed to users
- **Next.js API Routes**: Secure backend handling
- **Production ready**: Safe to deploy publicly
- **No NEXT_PUBLIC_ prefix**: Keeps the key private

## 🎯 Architecture

- **Frontend**: React components for UI
- **API Route**: `/app/api/process-bill/route.ts` (secure server-side)
- **OpenAI Integration**: Server-side only, API key protected
- **No traditional backend**: Uses Next.js built-in API routes

## ✅ **Benefits of This Approach:**

1. **Secure**: API key never exposed to browsers
2. **Simple**: No separate backend server to manage
3. **Fast**: Next.js API routes are very performant
4. **Deployable**: Works on Vercel, Netlify, any Node.js host
5. **Scalable**: Automatic scaling with serverless functions

## 💰 Cost Information

- GPT-4o Vision costs about $0.01-0.03 per bill analysis
- Monitor usage at https://platform.openai.com/usage
- Set up billing alerts in your OpenAI account
- Server-side calls are more efficient (no browser overhead)

## 🚀 Deploy to Production

**Vercel (Recommended):**
```bash
npm install -g vercel
vercel --prod
# Add OPENAI_API_KEY in Vercel dashboard (Environment Variables)
```

**Netlify:**
```bash
npm run build
# Deploy to Netlify
# Add OPENAI_API_KEY in Netlify dashboard (Environment Variables)
```

## 🔧 Troubleshooting

**API key errors:**
- Make sure you used `OPENAI_API_KEY` (not `NEXT_PUBLIC_OPENAI_API_KEY`)
- Verify the key is in `.env.local`
- Restart the dev server after adding the key

**Image upload fails:**
- Ensure image is under 10MB
- Use supported formats: JPEG, PNG, BMP, TIFF
- Check browser console for detailed errors

**500 Internal Server Error:**
- Check if OpenAI API key is valid
- Verify you have OpenAI credits
- Check server logs in terminal

## � **What's New (Security Update):**

### ❌ **Removed (Insecure):**
- Direct OpenAI API calls from browser
- `NEXT_PUBLIC_OPENAI_API_KEY` exposure
- Client-side API key handling

### ✅ **Added (Secure):**
- Next.js API route `/api/process-bill`
- Server-side OpenAI integration
- Proper error handling and validation
- File type and size validation
- Secure environment variable handling

Now your bill analysis app is both simple AND secure! 🎉🔒
