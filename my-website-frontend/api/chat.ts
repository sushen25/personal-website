// Serverless function for handling chat requests
// This can be deployed as AWS Lambda, Vercel Serverless Function, or similar

import { formatUserContextForPrompt } from '../src/lib/userContext';

interface Message {
    role: 'user' | 'assistant';
    content: string;
}

export const handler = async (event: any) => {
    // Handle CORS
    const headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    };

    if (event.httpMethod === 'OPTIONS') {
        return {
            statusCode: 200,
            headers,
            body: '',
        };
    }

    try {
        const { messages } = JSON.parse(event.body || '{}');

        if (!messages || !Array.isArray(messages)) {
            return {
                statusCode: 400,
                headers,
                body: JSON.stringify({ error: 'Invalid request: messages array required' }),
            };
        }

        // Get API key from environment
        // const apiKey = process.env.OPENAI_API_KEY || process.env.GEMINI_API_KEY || process.env.CLAUDE_API_KEY;
        const apiKey = "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"
        if (!apiKey) {
            return {
                statusCode: 500,
                headers,
                body: JSON.stringify({ error: 'API key not configured' }),
            };
        }

        // Determine which API to use based on available keys
        const useOpenAI = !!process.env.OPENAI_API_KEY;
        const useGemini = !!process.env.GEMINI_API_KEY && !useOpenAI;
        const useClaude = !!process.env.CLAUDE_API_KEY && !useOpenAI && !useGemini;

        const systemPrompt = formatUserContextForPrompt();

        let response;

        if (useOpenAI) {
            response = await callOpenAI(messages, systemPrompt, apiKey);
        } else if (useGemini) {
            response = await callGemini(messages, systemPrompt, apiKey);
        } else if (useClaude) {
            response = await callClaude(messages, systemPrompt, apiKey);
        } else {
            return {
                statusCode: 500,
                headers,
                body: JSON.stringify({ error: 'No API key configured' }),
            };
        }

        return {
            statusCode: 200,
            headers,
            body: JSON.stringify({ message: response }),
        };
    } catch (error: any) {
        console.error('Error processing chat request:', error);
        return {
            statusCode: 500,
            headers,
            body: JSON.stringify({ error: error.message || 'Internal server error' }),
        };
    }
};

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

