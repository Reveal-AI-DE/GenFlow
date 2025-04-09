// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import { useRef, useContext } from 'react'
import { useRefresh, useNotify } from 'react-admin'

import { FileEntity } from '@/types';
import { SessionContext, SessionContextInterface } from '@/context';
import { createTemporaryMessage, createGenerateRequest } from '@/utils';
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
        setSessionMessages,
        sessionMessages,
        generateURL,
    } = useContext<SessionContextInterface>(SessionContext);

    const handleFocusChatInput = (): void => {
        chatInputRef.current?.focus()
    }

    const handleSendMessage = (
        content: string,
        files: FileEntity[] = [],
    ): void => {
        try {
            setUserInput('');
            setIsGenerating(true);

            const tmpMessage = createTemporaryMessage(content, sessionMessages, setSessionMessages, false);
            const generateRequest = createGenerateRequest(
                content,
                files,
            );

            // streaming
            if (generateURL && generateRequest !== null) {
                generate(
                    generateURL,
                    generateRequest,
                    tmpMessage,
                    setSessionMessages
                ).then(() => {
                    setIsGenerating(false);
                    refresh();
                }).catch((error) => {
                    console.log(error);
                    notify(
                        error,
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
        } catch (error) {
            console.log(error);
            setUserInput(content);
            setIsGenerating(false);
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
