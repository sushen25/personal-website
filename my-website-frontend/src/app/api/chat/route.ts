// Next.js API route for chat
// Note: This will only work when static export is disabled in next.config.ts
// For production with static export, use the serverless function in /api/chat.ts

import { formatUserContextForPrompt } from '@/lib/userContext';
import { NextRequest, NextResponse } from 'next/server';

interface Message {
    role: 'user' | 'assistant';
    content: string;
}

export async function POST(request: NextRequest) {
    try {
        const { messages } = await request.json();

        if (!messages || !Array.isArray(messages)) {
            return NextResponse.json(
                { error: 'Invalid request: messages array required' },
                { status: 400 }
            );
        }

        // Get API key from environment
        const apiKey = process.env.OPENAI_API_KEY || process.env.GEMINI_API_KEY || process.env.CLAUDE_API_KEY;
        if (!apiKey) {
            return NextResponse.json(
                { error: 'API key not configured. Please set OPENAI_API_KEY, GEMINI_API_KEY, or CLAUDE_API_KEY in your environment variables.' },
                { status: 500 }
            );
        }

        // Determine which API to use based on available keys
        const useOpenAI = !!process.env.OPENAI_API_KEY;
        const useGemini = !!process.env.GEMINI_API_KEY && !useOpenAI;
        const useClaude = !!process.env.CLAUDE_API_KEY && !useOpenAI && !useGemini;

        const systemPrompt = formatUserContextForPrompt();

        let response: string;

        if (useOpenAI) {
            response = await callOpenAI(messages, systemPrompt, process.env.OPENAI_API_KEY!);
        } else if (useGemini) {
            response = await callGemini(messages, systemPrompt, process.env.GEMINI_API_KEY!);
        } else if (useClaude) {
            response = await callClaude(messages, systemPrompt, process.env.CLAUDE_API_KEY!);
        } else {
            return NextResponse.json(
                { error: 'No API key configured' },
                { status: 500 }
            );
        }

        return NextResponse.json({ message: response });
    } catch (error) {
        console.error('Error processing chat request:', error);
        const errorMessage = error instanceof Error ? error.message : 'Internal server error';
        return NextResponse.json(
            { error: errorMessage },
            { status: 500 }
        );
    }
}

async function callOpenAI(messages: Message[], systemPrompt: string, apiKey: string): Promise<string> {
    const response = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${apiKey}`,
        },
        body: JSON.stringify({
            model: 'gpt-4o-mini',
            messages: [
                { role: 'system', content: systemPrompt },
                ...messages,
            ],
            temperature: 0.7,
            max_tokens: 500,
        }),
    });

    if (!response.ok) {
        const error = await response.text();
        throw new Error(`OpenAI API error: ${error}`);
    }

    const data = await response.json();
    return data.choices[0]?.message?.content || 'Sorry, I could not generate a response.';
}

async function callGemini(messages: Message[], systemPrompt: string, apiKey: string): Promise<string> {
    // Convert messages to Gemini format
    const contents = messages.map(msg => ({
        role: msg.role === 'user' ? 'user' : 'model',
        parts: [{ text: msg.content }],
    }));

    const response = await fetch(
        `https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=${apiKey}`,
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                contents: [
                    { role: 'user', parts: [{ text: systemPrompt }] },
                    ...contents,
                ],
            }),
        }
    );

    if (!response.ok) {
        const error = await response.text();
        throw new Error(`Gemini API error: ${error}`);
    }

    const data = await response.json();
    return data.candidates[0]?.content?.parts[0]?.text || 'Sorry, I could not generate a response.';
}

async function callClaude(messages: Message[], systemPrompt: string, apiKey: string): Promise<string> {
    const response = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'x-api-key': apiKey,
            'anthropic-version': '2023-06-01',
        },
        body: JSON.stringify({
            model: 'claude-3-haiku-20240307',
            max_tokens: 500,
            system: systemPrompt,
            messages: messages.map(msg => ({
                role: msg.role === 'user' ? 'user' : 'assistant',
                content: msg.content,
            })),
        }),
    });

    if (!response.ok) {
        const error = await response.text();
        throw new Error(`Claude API error: ${error}`);
    }

    const data = await response.json();
    return data.content[0]?.text || 'Sorry, I could not generate a response.';
}

