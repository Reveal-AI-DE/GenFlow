// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import {
    UIEventHandler, useRef, useState, useCallback,
    useContext, useEffect
} from 'react'

import { SessionContext } from '@/context';

interface ScrollHook {
    messagesStartRef: React.RefObject<HTMLDivElement>,
    messagesEndRef: React.RefObject<HTMLDivElement>,
    isAtTop: boolean,
    isAtBottom: boolean,
    userScrolled: boolean,
    isOverflowing: boolean,
    handleScroll: UIEventHandler<HTMLDivElement>,
    scrollToTop: () => void,
    scrollToBottom: () => void,
    setIsAtBottom: (isAtBottom: boolean) => void,
};

const useScroll = (): ScrollHook => {
    const { isGenerating, sessionMessages } = useContext(SessionContext)

    const messagesStartRef = useRef<HTMLDivElement>(null)
    const messagesEndRef = useRef<HTMLDivElement>(null)
    const isAutoScrolling = useRef(false)

    const [isAtTop, setIsAtTop] = useState(false)
    const [isAtBottom, setIsAtBottom] = useState(true)
    const [userScrolled, setUserScrolled] = useState(false)
    const [isOverflowing, setIsOverflowing] = useState(false)

    const handleScroll: UIEventHandler<HTMLDivElement> = useCallback((event) => {
        const target = event.target as HTMLDivElement
        const bottom =
            Math.round(target.scrollHeight) - Math.round(target.scrollTop) ===
            Math.round(target.clientHeight);
        setIsAtBottom(bottom);

        const top = target.scrollTop === 0;
        setIsAtTop(top);

        if(!bottom && !isAutoScrolling.current) {
            setUserScrolled(true)
        } else {
            setUserScrolled(false)
        }

        const isOverflow = target.scrollHeight > target.clientHeight;
        setIsOverflowing(isOverflow);
    }, [])

    const scrollToTop = useCallback(() => {
        if (messagesStartRef.current) {
            messagesStartRef.current.scrollIntoView({ behavior: 'instant' })
        }
    }, [])

    const scrollToBottom = useCallback(() => {
        isAutoScrolling.current = true

        setTimeout(() => {
            if (messagesEndRef.current) {
                messagesEndRef.current.scrollIntoView({ behavior: 'instant' })
            }

            isAutoScrolling.current = false
        }, 100)
    }, [])

    useEffect(() => {
        setUserScrolled(false);
        if (!isGenerating && userScrolled) {
            setUserScrolled(false);
        }
    }, [isGenerating])

    useEffect(() => {
        if (isGenerating && !userScrolled) {
            scrollToBottom()
        }
    }, [sessionMessages])

    return {
        messagesStartRef,
        messagesEndRef,
        isAtTop,
        isAtBottom,
        userScrolled,
        isOverflowing,
        handleScroll,
        scrollToTop,
        scrollToBottom,
        setIsAtBottom,
    };
};

export default useScroll;
