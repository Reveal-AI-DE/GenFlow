// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, {
    FC, memo, Children, isValidElement, ReactElement
} from 'react';
import ReactMarkdown, { Options } from 'react-markdown';
import remarkGfm from 'remark-gfm'
import remarkMath from 'remark-math'
import remarkBreaks from 'remark-breaks'

import CodeSnippet from '@/message/CodeSnippet';

const MemoizedReactMarkdown: FC<Options> = memo(
    ReactMarkdown,
    (prevProps, nextProps) => (
        prevProps.children === nextProps.children
        // && prevProps.className === nextProps.className
    ),
);

interface MessageMarkdownProps {
    content: string;
};

const MessageMarkdown: FC<MessageMarkdownProps> = ({
    content,
}): JSX.Element => (
    <MemoizedReactMarkdown
        // className='prose dark:prose-invert prose-p:leading-relaxed prose-pre:p-0 min-w-full space-y-6 break-words'
        remarkPlugins={[remarkGfm, remarkMath, remarkBreaks]}
        components={{
            p({ children }) {
                return <p className='mb-2 last:mb-0'>{children}</p>
            },
            img({ node, ...props }) {
                return <img className='max-w-[67%]' alt='' {...props} />
            },
            code({
                node, className, children, ...props
            }) {
                const childArray = Children.toArray(children)
                const firstChild = childArray[0] as ReactElement
                const firstChildAsString = isValidElement(firstChild) ?
                    (firstChild as ReactElement).props.children : firstChild

                if (firstChildAsString === '▍') {
                    return <span className='mt-1 animate-pulse cursor-default'>▍</span>
                }

                if (typeof firstChildAsString === 'string') {
                    childArray[0] = firstChildAsString.replace('`▍`', '▍')
                }

                const match = /language-(\w+)/.exec(className || '')

                if (
                    typeof firstChildAsString === 'string' &&
                !firstChildAsString.includes('\n')
                ) {
                    return (
                        <code className={className} {...props}>
                            {childArray}
                        </code>
                    )
                }

                return (
                    <CodeSnippet
                        key={Math.random()}
                        language={(match && match[1]) || ''}
                        code={String(childArray).replace(/\n$/, '')}
                        {...props}
                    />
                )
            }
        }}
    >
        {content}
    </MemoizedReactMarkdown>
);

export default MessageMarkdown;
