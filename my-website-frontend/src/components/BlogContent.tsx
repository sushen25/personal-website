"use client";

import { useEffect, useRef } from "react";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneLight } from "react-syntax-highlighter/dist/esm/styles/prism";
import { createRoot } from "react-dom/client";

// Import language definitions
import 'react-syntax-highlighter/dist/esm/languages/prism/python';
import 'react-syntax-highlighter/dist/esm/languages/prism/typescript';
import 'react-syntax-highlighter/dist/esm/languages/prism/javascript';

interface BlogContentProps {
    html: string;
}

function CodeBlock({ code, language }: { code: string; language: string }) {
    // Map language names to Prism language codes
    const langMap: Record<string, string> = {
        'python': 'python',
        'typescript': 'typescript',
        'javascript': 'javascript',
        'js': 'javascript',
        'ts': 'typescript',
    };

    const prismLang = langMap[language.toLowerCase()] || language.toLowerCase() || 'text';

    return (
        <div className="code-block-wrapper my-6">
            <SyntaxHighlighter
                language={prismLang}
                style={oneLight}
                customStyle={{
                    fontSize: "1rem",
                    padding: "1.5rem",
                    borderRadius: "0.5rem",
                    margin: "0",
                    fontFamily: "'Courier New', Courier, monospace",
                    background: "#f8f9fa",
                }}
                showLineNumbers={false}
                PreTag="div"
            >
                {code}
            </SyntaxHighlighter>
        </div>
    );
}

export default function BlogContent({ html }: BlogContentProps) {
    const containerRef = useRef<HTMLDivElement>(null);
    const renderedRef = useRef(false);

    useEffect(() => {
        if (!containerRef.current || renderedRef.current) return;

        const container = containerRef.current;
        const tempDiv = document.createElement("div");
        tempDiv.innerHTML = html;

        // Find all pre elements with code blocks
        const preElements = Array.from(tempDiv.querySelectorAll('pre[data-code-block-lang]'));

        // Process each code block
        preElements.forEach((pre, index) => {
            const lang = pre.getAttribute('data-code-block-lang') || 'text';
            const contentSpan = pre.querySelector('.pre--content');

            if (contentSpan) {
                // Extract and clean code
                let code = contentSpan.innerHTML;

                // Replace <br> and <br/> with newlines
                code = code.replace(/<br\s*\/?>/gi, '\n');

                // Remove all HTML tags
                code = code.replace(/<[^>]+>/g, '');

                // Decode HTML entities
                const textarea = document.createElement('textarea');
                textarea.innerHTML = code;
                code = textarea.value;

                // Normalize and clean
                code = code.replace(/\r\n/g, '\n').replace(/\r/g, '\n').trim();

                // Replace the pre element with a div that we'll render into
                const codeWrapper = document.createElement('div');
                codeWrapper.className = 'code-block-placeholder';
                codeWrapper.setAttribute('data-code', code);
                codeWrapper.setAttribute('data-lang', lang);
                pre.parentNode?.replaceChild(codeWrapper, pre);
            }
        });

        // Set the processed HTML
        container.innerHTML = tempDiv.innerHTML;
        renderedRef.current = true;

        // Now render all code blocks
        const placeholders = container.querySelectorAll('.code-block-placeholder');
        placeholders.forEach((placeholder) => {
            const code = placeholder.getAttribute('data-code') || '';
            const lang = placeholder.getAttribute('data-lang') || 'text';

            if (code && placeholder.parentNode) {
                const wrapper = document.createElement('div');
                placeholder.parentNode.replaceChild(wrapper, placeholder);

                const root = createRoot(wrapper);
                root.render(<CodeBlock code={code} language={lang} />);
            }
        });
    }, [html]);

    return <div ref={containerRef} className="blog-article text-gray-700 dark:text-gray-300" />;
}
