# Chatbot Setup Guide

This guide explains how to set up the AI chatbot feature for your website.

## Overview

The chatbot is a floating button that appears on all pages. When clicked, it opens a chat panel where users can ask questions about your professional background, experience, skills, projects, and blog posts.

## Features

- ✅ Floating button that persists on all pages
- ✅ Beautiful slide-in panel from the right
- ✅ Dark mode support
- ✅ Responsive design (mobile-friendly)
- ✅ Context-aware: Only answers questions about you
- ✅ Supports OpenAI, Gemini, or Claude APIs

## Setup Instructions

### Option 1: Development with Next.js API Route (Recommended for Local Development)

1. **Temporarily disable static export** in `next.config.ts`:
   ```typescript
   const nextConfig: NextConfig = {
     // output: "export",  // Comment this out for development
     trailingSlash: true,
     images: {
       unoptimized: true,
     },
   };
   ```

2. **Create a `.env.local` file** in the root directory:
   ```env
   # Choose one of the following API keys:
   OPENAI_API_KEY=your_openai_api_key_here
   # OR
   GEMINI_API_KEY=your_gemini_api_key_here
   # OR
   CLAUDE_API_KEY=your_claude_api_key_here
   ```

3. **Run the development server**:
   ```bash
   npm run dev
   ```

4. **The chatbot will be available at** `/api/chat`

### Option 2: Production with Serverless Function

Since your app uses static export (`output: "export"`), API routes won't work in production. You'll need to deploy the serverless function separately.

#### For AWS Lambda:

1. Deploy the function in `/api/chat.ts` as an AWS Lambda function
2. Set up API Gateway to expose it as an HTTP endpoint
3. Set environment variables in Lambda:
   - `OPENAI_API_KEY` or `GEMINI_API_KEY` or `CLAUDE_API_KEY`
4. Update `NEXT_PUBLIC_CHAT_API_URL` in your build environment to point to your Lambda endpoint

#### For Vercel:

1. Create a `vercel.json` or use Vercel's serverless functions
2. Deploy the API route as a serverless function
3. Set environment variables in Vercel dashboard

#### For Other Platforms:

Deploy `/api/chat.ts` as a serverless function and configure the endpoint URL.

### Option 3: External API Endpoint

If you have an existing API endpoint, you can configure it:

1. Set the environment variable:
   ```env
   NEXT_PUBLIC_CHAT_API_URL=https://your-api-endpoint.com/chat
   ```

2. Ensure your API endpoint accepts POST requests with this format:
   ```json
   {
     "messages": [
       { "role": "user", "content": "What is your experience?" }
     ]
   }
   ```

3. And returns responses in this format:
   ```json
   {
     "message": "Response text here"
   }
   ```

## API Key Setup

### OpenAI
1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Add to `.env.local`: `OPENAI_API_KEY=sk-...`

### Google Gemini
1. Go to https://aistudio.google.com/app/apikey
2. Create a new API key
3. Add to `.env.local`: `GEMINI_API_KEY=...`

### Anthropic Claude
1. Go to https://console.anthropic.com/
2. Create a new API key
3. Add to `.env.local`: `CLAUDE_API_KEY=sk-ant-...`

## Customization

### Updating User Context

Edit `/src/lib/userContext.ts` to update:
- About information
- Work experience
- Education
- Skills
- Projects
- Blog posts

The chatbot automatically uses this information to answer questions.

### Styling

The chatbot component is in `/src/components/Chatbot.tsx`. It uses Tailwind CSS and matches your website's theme (dark mode support included).

### System Prompt

The system prompt that restricts the chatbot to only answer questions about you is in `/src/lib/userContext.ts` in the `formatUserContextForPrompt()` function. You can customize it there.

## Troubleshooting

### Chatbot not appearing
- Make sure the Chatbot component is imported in `src/app/layout.tsx`
- Check browser console for errors

### API errors
- Verify your API key is set correctly in environment variables
- Check that the API endpoint is accessible
- For static export builds, make sure you've configured `NEXT_PUBLIC_CHAT_API_URL`

### CORS errors
- If using an external API, ensure CORS is properly configured
- The serverless function includes CORS headers

## Notes

- The chatbot is designed to ONLY answer questions about your professional background
- It will politely decline to answer general-purpose questions
- All context is stored in `userContext.ts` for easy updates
- The component is fully responsive and works on mobile devices

