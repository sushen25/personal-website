'use client';

import { useState, useRef } from 'react';
import * as Dialog from '@radix-ui/react-dialog';
import { Bot, Send } from 'lucide-react';

type Message = {
    content: string;
    isUser: boolean;
};

export default function ChatBox() {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState<Message[]>([
        { content: "Hi! I'm an AI assistant. Ask me anything about Sushen!", isUser: false }
    ]);
    const [inputMessage, setInputMessage] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const typingTimeout = useRef<NodeJS.Timeout | null>(null);

    const handleSendMessage = () => {
        if (!inputMessage.trim()) return;

        setMessages(prev => [...prev, { content: inputMessage, isUser: true }]);
        setInputMessage('');
        setIsTyping(true);

        if (typingTimeout.current) clearTimeout(typingTimeout.current);
        typingTimeout.current = setTimeout(() => {
            setMessages(prev => [...prev, {
                content: "I'm still learning about Sushen. Please check back later!",
                isUser: false
            }]);
            setIsTyping(false);
        }, 1000);
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    };

    return (
        <Dialog.Root open={isOpen} onOpenChange={setIsOpen}>
            <Dialog.Trigger asChild>
                <button
                    className="fixed bottom-4 right-4 sm:bottom-6 sm:right-6 p-3 sm:p-4 bg-blue-600 hover:bg-blue-700 text-white rounded-full shadow-lg transition-all duration-200 hover:scale-105 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                    aria-label="Open AI Chat"
                >
                    <Bot className="w-5 h-5 sm:w-6 sm:h-6" />
                </button>
            </Dialog.Trigger>
            <Dialog.Portal>
                <Dialog.Overlay className="fixed inset-0 bg-black/50 backdrop-blur-sm" />
                <Dialog.Content className="fixed bottom-0 right-0 sm:bottom-24 sm:right-6 w-full sm:w-96 h-[80vh] sm:h-[500px] bg-white dark:bg-gray-800 rounded-t-lg sm:rounded-lg shadow-xl p-4 flex flex-col">
                    <div className="flex justify-between items-center mb-4">
                        <Dialog.Title className="text-base font-semibold text-gray-900 dark:text-white">
                            Chat with AI
                        </Dialog.Title>
                        <Dialog.Close className="text-gray-900 dark:text-white text-2xl font-bold ml-2 hover:text-red-500 focus:outline-none focus:ring-2 focus:ring-red-400 rounded-full px-2 py-0.5 transition-colors" aria-label="Close chat">
                            ✕
                        </Dialog.Close>
                    </div>
                    <div className="flex-1 overflow-y-auto mb-4 p-4 bg-gray-50 dark:bg-gray-900 rounded-lg">
                        <div className="space-y-3">
                            {messages.map((message, index) => (
                                <div
                                    key={index}
                                    className={`flex ${message.isUser ? 'justify-end' : 'justify-start'}`}
                                >
                                    <div
                                        className={`max-w-[80%] rounded-lg px-3 py-1.5 text-xs sm:text-sm ${message.isUser
                                            ? 'bg-blue-600 text-white'
                                            : 'bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-white'
                                            }`}
                                    >
                                        {message.content}
                                    </div>
                                </div>
                            ))}
                            {isTyping && (
                                <div className="flex justify-start">
                                    <div className="max-w-[80%] rounded-lg px-3 py-1.5 text-sm sm:text-base bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-white flex items-center gap-2">
                                        <span>AI is typing</span>
                                        <span style={{ display: 'inline-block', width: 18, textAlign: 'left' }}>
                                            <span style={{
                                                display: 'inline-block',
                                                animation: 'blink 1.4s infinite both',
                                                fontWeight: 'bold',
                                                fontSize: '1.2em',
                                                color: '#2563eb',
                                                animationDelay: '0s',
                                            }}>.</span>
                                            <span style={{
                                                display: 'inline-block',
                                                animation: 'blink 1.4s infinite both',
                                                fontWeight: 'bold',
                                                fontSize: '1.2em',
                                                color: '#2563eb',
                                                animationDelay: '0.2s',
                                            }}>.</span>
                                            <span style={{
                                                display: 'inline-block',
                                                animation: 'blink 1.4s infinite both',
                                                fontWeight: 'bold',
                                                fontSize: '1.2em',
                                                color: '#2563eb',
                                                animationDelay: '0.4s',
                                            }}>.</span>
                                        </span>
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>
                    <div className="flex gap-2">
                        <input
                            type="text"
                            value={inputMessage}
                            onChange={(e) => setInputMessage(e.target.value)}
                            onKeyPress={handleKeyPress}
                            placeholder="Type your message..."
                            className="flex-1 px-3 sm:px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 text-xs"
                        />
                        <button
                            onClick={handleSendMessage}
                            className="px-3 sm:px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors text-xs whitespace-nowrap flex items-center gap-2"
                        >
                            <Send className="w-4 h-4" />
                            Send
                        </button>
                    </div>
                </Dialog.Content>
            </Dialog.Portal>
        </Dialog.Root>
    );
} 