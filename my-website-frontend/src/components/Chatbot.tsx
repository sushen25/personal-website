"use client";

import { useState, useRef, useEffect, useMemo } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import remarkBreaks from 'remark-breaks';

interface Message {
    role: 'user' | 'assistant';
    content: string;
    timestamp?: number;
}

const suggestedPrompts = [
    "What are Sushen's main skills?",
    "Tell me about his work experience",
    "What projects has he built?",
    "Show me recent blog posts",
    "What's his education background?",
    "How can I contact him?",
    "Tell me a fun fact about Sushen",
    "What technologies does he work with?"
]

const normalizeMarkdown = (text: string) =>
    text
        // normalise Windows line endings
        .replace(/\r\n/g, '\n')
        // ensure headings start on a new line
        .replace(/([^\n])(\s*##\s+)/g, '$1\n\n$2');

export default function Chatbot() {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState<Message[]>([
        {
            role: 'assistant',
            content: "Hi! I'm an AI assistant that can answer questions about Sushen Satturu - his experience, skills, projects, education, and blog posts. What would you like to know?"
        }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [sessionId, setSessionId] = useState<string>('');
    const [useStreaming] = useState(true);
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const inputRef = useRef<HTMLTextAreaElement>(null);

    // Select 3 random prompts when chatbot opens
    const displayedPrompts = useMemo(() => {
        const shuffled = [...suggestedPrompts].sort(() => Math.random() - 0.5);
        return shuffled.slice(0, 3);
    }, [isOpen]);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    useEffect(() => {
        if (isOpen && inputRef.current) {
            inputRef.current.focus();
        }
    }, [isOpen]);

    const handleSendNonStream = async () => {
        if (!input.trim() || isLoading) return;

        const userMessage = input.trim();
        setInput('');

        // Add user message to the chat
        const newUserMessage: Message = {
            role: 'user',
            content: userMessage,
            timestamp: Date.now() / 1000
        };
        setMessages(prev => [...prev, newUserMessage]);
        setIsLoading(true);

        try {
            // Get the API endpoint from environment variable or use a default
            const apiEndpoint = `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3000/dev'}/api/chat/`;

            const requestBody = {
                messages: [...messages, newUserMessage].map(msg => ({
                    role: msg.role,
                    content: msg.content,
                    ...(msg.timestamp && { timestamp: msg.timestamp })
                })),
                ...(sessionId && { session_id: sessionId })
            };

            const response = await fetch(apiEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestBody),
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.message || 'Failed to get response');
            }

            const data = await response.json();

            if (data.session_id && !sessionId) {
                setSessionId(data.session_id);
            }

            setMessages(prev => [...prev, {
                role: 'assistant',
                content: data.message.content,
                timestamp: data.message.timestamp
            }]);
        } catch (error) {
            console.error('Error sending message:', error);
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: "I'm sorry, I encountered an error. Please make sure the backend API is running and configured correctly."
            }]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleSendStream = async () => {
        if (!input.trim() || isLoading) return;

        const userMessage = input.trim();
        setInput('');

        const newUserMessage: Message = {
            role: 'user',
            content: userMessage,
            timestamp: Date.now() / 1000
        };
        setMessages(prev => [...prev, newUserMessage]);
        setIsLoading(true);

        const assistantMessageIndex = messages.length + 1;
        setMessages(prev => [...prev, {
            role: 'assistant',
            content: '',
            timestamp: Date.now() / 1000
        }]);

        try {
            const apiEndpoint = `${process.env.NEXT_PUBLIC_STREAM_API_URL || 'http://localhost:8001'}/api/chat/stream`;
            const requestBody = {
                messages: [...messages, newUserMessage].map(msg => ({
                    role: msg.role,
                    content: msg.content,
                    ...(msg.timestamp && { timestamp: msg.timestamp })
                })),
                ...(sessionId && { session_id: sessionId })
            };

            const response = await fetch(apiEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestBody),
            });

            if (!response.ok) {
                throw new Error('Failed to get streaming response');
            }

            // Read the stream
            const reader = response.body?.getReader();
            const decoder = new TextDecoder();
            let accumulatedContent = '';

            if (reader) {
                while (true) {
                    const { done, value } = await reader.read();

                    if (done) break;

                    const chunk = decoder.decode(value, { stream: true });
                    const lines = chunk.split('\n');

                    for (const line of lines) {
                        if (line.trim()) {
                            try {
                                const event = JSON.parse(line);

                                if (event.event?.contentBlockStop) {
                                    accumulatedContent += " \n"
                                }

                                if (event.data) {
                                    accumulatedContent += event.data.split("\n").join(" \n");

                                    setMessages(prev => {
                                        const updated = [...prev];
                                        updated[assistantMessageIndex] = {
                                            role: 'assistant',
                                            content: accumulatedContent,
                                            timestamp: Date.now() / 1000
                                        };
                                        return updated;
                                    });
                                } else if (event.error) {
                                    throw new Error(event.error);
                                } else if (event.session_id && !sessionId) {
                                    setSessionId(event.session_id);
                                }
                            } catch (e) {
                                console.error('Error parsing event:', e);
                            }
                        }
                    }
                }
            }
        } catch (error) {
            console.error('Error sending message:', error);
            setMessages(prev => [...prev.slice(0, -1), {
                role: 'assistant',
                content: "I'm sorry, I encountered an error. Please try again."
            }]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleSend = async () => {
        if (useStreaming) {
            return handleSendStream();
        } else {
            return handleSendNonStream();
        }
    };

    const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <>
            {/* Floating Button */}
            <button
                onClick={() => setIsOpen(!isOpen)}
                className={`fixed ${isOpen ? 'bottom-24 right-4' : 'bottom-6 right-6'} w-14 h-14 bg-blue-600 hover:bg-blue-700 text-white rounded-full shadow-lg flex items-center justify-center z-50 transition-all duration-300 hover:scale-110`}
                aria-label={isOpen ? "Close chat" : "Open chat"}
            >
                {isOpen ? (
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                ) : (
                    <svg
                        className="w-6 h-6"
                        viewBox="0 0 24 24"
                        fill="currentColor"
                        xmlns="http://www.w3.org/2000/svg"
                    >
                        <path d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09ZM18.259 8.715 18 9.75l-.259-1.035a3.375 3.375 0 0 0-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 0 0 2.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 0 0 2.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 0 0-2.456 2.456ZM16.894 20.567 16.5 21.75l-.394-1.183a2.25 2.25 0 0 0-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 0 0 1.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 0 0 1.423 1.423l1.183.394-1.183.394a2.25 2.25 0 0 0-1.423 1.423Z" />
                    </svg>
                )}
            </button>

            {/* Chat Panel */}
            <div
                className={`fixed right-0 top-0 h-full w-full md:w-[600px] lg:w-[700px] xl:w-[800px] bg-white dark:bg-gray-900 shadow-2xl z-40 transform transition-transform duration-300 ease-in-out ${isOpen ? 'translate-x-0' : 'translate-x-full'
                    } flex flex-col`}
            >
                {/* Header */}
                <div className="bg-blue-600 text-white p-4 flex items-center justify-between">
                    <div className="flex items-center gap-2">
                        <div className="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center">
                            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                            </svg>
                        </div>
                        <div>
                            <h3 className="font-semibold">Ask about Sushen</h3>
                            <p className="text-xs text-blue-100">AI Assistant</p>
                        </div>
                    </div>
                    <button
                        onClick={() => setIsOpen(false)}
                        className="text-white hover:text-gray-200 transition-colors"
                        aria-label="Close chat"
                    >
                        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>

                {/* Messages */}
                <div className="flex-1 overflow-y-auto p-4 space-y-4">
                    {/* Suggested Prompts - show only when no user messages yet */}
                    {messages.length === 1 && messages[0].role === 'assistant' && (
                        <div className="space-y-3 mt-2">
                            <p className="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide">
                                Suggested Questions
                            </p>
                            <div className="flex flex-wrap gap-2">
                                {displayedPrompts.map((prompt, index) => (
                                    <button
                                        key={index}
                                        onClick={() => {
                                            setInput(prompt);
                                            inputRef.current?.focus();
                                        }}
                                        className="px-3 py-1.5 text-sm bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 rounded-full border border-blue-200 dark:border-blue-700 hover:bg-blue-100 dark:hover:bg-blue-900/50 hover:border-blue-300 dark:hover:border-blue-600 transition-all duration-200 hover:scale-105 active:scale-95"
                                    >
                                        {prompt}
                                    </button>
                                ))}
                            </div>
                            <hr className="my-6 border-t border-gray-300 dark:border-gray-600" />
                        </div>
                    )}

                    {messages.map((message, index) => (
                        <div
                            key={index}
                            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                        >
                            <div
                                className={`max-w-[80%] rounded-lg px-4 py-2 ${message.role === 'user'
                                    ? 'bg-blue-600 text-white'
                                    : 'bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100'
                                    }`}
                            >
                                {message.role === 'user' ? (
                                    <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                                ) : (
                                    <div className="text-sm prose prose-sm dark:prose-invert max-w-none leading-relaxed">
                                        <ReactMarkdown
                                            remarkPlugins={[remarkGfm, remarkBreaks]}
                                            components={{
                                                p: ({ children }) => <p className="mb-4 last:mb-0">{children}</p>,
                                                ul: ({ children }) => <ul className="mb-4 last:mb-0 ml-4 list-disc">{children}</ul>,
                                                ol: ({ children }) => <ol className="mb-4 last:mb-0 ml-4 list-decimal">{children}</ol>,
                                                li: ({ children }) => <li className="mb-1">{children}</li>,
                                                h1: ({ children }) => <h1 className="text-xl font-bold mb-3 mt-4 first:mt-0">{children}</h1>,
                                                h2: ({ children }) => <h2 className="text-lg font-bold mb-2 mt-4 first:mt-0">{children}</h2>,
                                                h3: ({ children }) => <h3 className="text-base font-bold mb-2 mt-3 first:mt-0">{children}</h3>,
                                                strong: ({ children }) => <strong className="font-bold">{children}</strong>,
                                                em: ({ children }) => <em className="italic">{children}</em>,
                                                br: () => <br className="block my-2" />,
                                                hr: () => <hr className="my-6 border-t border-gray-300 dark:border-gray-600" />,
                                            }}
                                        >
                                            {normalizeMarkdown(message.content)}
                                        </ReactMarkdown>
                                    </div>
                                )}
                            </div>
                        </div>
                    ))}
                    {isLoading && (
                        <div className="flex justify-start">
                            <div className="bg-gray-100 dark:bg-gray-800 rounded-lg px-4 py-2">
                                <div className="flex space-x-1">
                                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                                </div>
                            </div>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>

                {/* Input */}
                <div className="border-t border-gray-200 dark:border-gray-700 p-4">
                    <div className="flex gap-2">
                        <textarea
                            ref={inputRef}
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyPress={handleKeyPress}
                            placeholder="Ask about Sushen's experience, skills, projects..."
                            className="flex-1 resize-none rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                            rows={1}
                            style={{ minHeight: '40px', maxHeight: '120px' }}
                            onInput={(e) => {
                                const target = e.target as HTMLTextAreaElement;
                                target.style.height = 'auto';
                                target.style.height = `${Math.min(target.scrollHeight, 120)}px`;
                            }}
                        />
                        <button
                            onClick={handleSend}
                            disabled={!input.trim() || isLoading}
                            className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed text-white rounded-lg px-4 py-2 transition-colors flex items-center justify-center"
                            aria-label="Send message"
                        >
                            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                            </svg>
                        </button>
                    </div>
                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-2 text-center">
                        Ask me anything about Sushen&apos;s professional background
                    </p>
                </div>
            </div>

            {/* Backdrop */}
            {isOpen && (
                <div
                    className="fixed inset-0 bg-black/20 dark:bg-black/40 z-30 md:hidden"
                    onClick={() => setIsOpen(false)}
                />
            )}
        </>
    );
}

