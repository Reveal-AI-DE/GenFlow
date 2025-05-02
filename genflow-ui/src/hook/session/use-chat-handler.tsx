// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import { useRef, useContext } from 'react'
import { useRefresh, useNotify } from 'react-admin'

import { FileEntity } from '@/types';
import { SessionContext, SessionContextInterface } from '@/context';
import { createTemporaryMessage, createGenerateRequest, truncateText } from '@/utils';
import { useGenerate } from '@/hook';

interface ChatHandlerHook {
    chatInputRef: React.RefObject<HTMLTextAreaElement>,
    handleFocusChatInput: () => void,
    handleSendMessage: (content: string, files?: FileEntity[]) => void,
    handleStopMessage: () => void,
};

const useChatHandler = (): ChatHandlerHook => {
    const chatInputRef = useRef<HTMLTextAreaElement>(null)
    const generate = useGenerate();
    const refresh = useRefresh();
    const notify = useNotify();

    const {
        setUserInput,
        setIsGenerating,
        chatSetting,
        setSessionMessages,
        sessionMessages,
        generateURL,
        fallbackGenerateURL,
    } = useContext<SessionContextInterface>(SessionContext);

    const handleFocusChatInput = (): void => {
        chatInputRef.current?.focus()
    }

    const handleSendMessage = (
        content: string,
        files: FileEntity[] = [],
    ): void => {
        setUserInput('');
        setIsGenerating(true);

        const tmpMessage = createTemporaryMessage(content, sessionMessages, setSessionMessages, false);
        const generateRequest = createGenerateRequest(
            content,
            files,
            chatSetting,
        );

        // streaming
        if (generateURL && fallbackGenerateURL && generateRequest !== null) {
            generate(
                generateURL,
                fallbackGenerateURL,
                generateRequest,
                tmpMessage,
                setSessionMessages
            ).then(() => {
                setIsGenerating(false);
                refresh();
            }).catch((error) => {
                notify(
                    truncateText(error.message, 100, 'characters') || 'An error occurred while generating the response',
                    {
                        type: 'error',
                    }
                );
                setUserInput(content);
                setIsGenerating(false);
                // remove the temporary message
                setSessionMessages((prev) => {
                    const newMessages = [...prev];
                    newMessages.pop();
                    return newMessages;
                });
            });
        }
    };

    const handleStopMessage = (): void => {
        console.log('stop');
    };

    return {
        chatInputRef,
        handleFocusChatInput,
        handleSendMessage,
        handleStopMessage,
    };
};

export default useChatHandler;
