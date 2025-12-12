"use client";

import { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface Message {
    role: 'user' | 'assistant';
    content: string;
    timestamp?: number;
}

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
    const [useStreaming, setUseStreaming] = useState(true);
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const inputRef = useRef<HTMLTextAreaElement>(null);

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
            const apiEndpoint = 'http://localhost:3000/dev/api/chat/';

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
            const apiEndpoint = 'http://localhost:8001/api/chat/stream';
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
                className="fixed bottom-6 right-6 w-14 h-14 bg-blue-600 hover:bg-blue-700 text-white rounded-full shadow-lg flex items-center justify-center z-50 transition-all duration-300 hover:scale-110"
                aria-label="Open chat"
            >
                {isOpen ? (
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                ) : (
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
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
                                    <div className="text-sm prose prose-sm dark:prose-invert max-w-none prose-p:my-4 prose-ul:my-4 prose-ol:my-4 prose-li:my-2 prose-headings:my-4 prose-h1:mb-4 prose-h2:mb-3 prose-h2:mt-6 prose-h3:mb-2 prose-h3:mt-4 leading-relaxed">
                                        <ReactMarkdown
                                            remarkPlugins={[remarkGfm]}
                                            components={{
                                                p: ({ children }) => <p className="mb-4">{children}</p>,
                                                br: () => <br className="my-2" />,
                                            }}
                                        >
                                            {message.content}
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
                        Ask me anything about Sushen's professional background
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

