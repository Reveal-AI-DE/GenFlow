// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import { Dispatch, SetStateAction } from 'react';

import {
    GenerateRequest,
    ChatResponse,
    ChatResponseType,
    SessionMessage,
} from '@/types';
import { createOptions } from '@/auth/authProvider';

type GenerateHook = (
    url: string,
    generateRequest: GenerateRequest,
    lastSessionMessage: SessionMessage,
    setSessionMessages: Dispatch<SetStateAction<SessionMessage[] | []>>
) => Promise<void>;

const useGenerate = (): GenerateHook => {
    const generate: GenerateHook = (
        url,
        generateRequest,
        lastSessionMessage,
        setSessionMessages
    ): Promise<void> => new Promise((resolve, reject) => {
        let fullText = '';

        const options = createOptions(url);
        if (!options.user || !options.headers) {
            reject(new Error('Not authenticated'));
            return;
        }
        const teamHeader = options.headers.get('X-Team');
        if (!teamHeader) {
            reject(new Error('X-Team header is missing'));
            return;
        }

        const webSocket = new WebSocket(url, [
            'json',
            options.user.token.replace('Token ', ''),
            teamHeader,
        ]);

        webSocket.onerror = (error) => {
            reject(error);
            webSocket.close();
            // TODO: fallback to http
        };

        // Handle incoming chunks
        webSocket.onmessage = (event) => {
            const response = JSON.parse(event.data as string) as ChatResponse;
            if (response.type === ChatResponseType.ERROR) {
                reject(new Error(response.data as string));
                webSocket.close();
            }
            if (response.type === ChatResponseType.CHUNK) {
                fullText += response.data as string;
                setSessionMessages((prev: SessionMessage[]) => prev.map((sessionMessage) => {
                    if (sessionMessage.id === lastSessionMessage.id) {
                        const updatedChatMessage: SessionMessage = {
                            ...sessionMessage,
                            answer: fullText,
                        }
                        return updatedChatMessage
                    }
                    return sessionMessage
                }));
            }
            if (response.type === ChatResponseType.MESSAGE) {
                setSessionMessages((prev: SessionMessage[]) => prev.map((sessionMessage) => {
                    if (sessionMessage.id === lastSessionMessage.id) {
                        const updatedChatMessage: SessionMessage = response.data as SessionMessage;
                        return updatedChatMessage
                    }
                    return sessionMessage
                }));
                webSocket.close();
                resolve();
            }
        };

        webSocket.onopen = () => {
            webSocket.send(JSON.stringify(generateRequest));
        };
    });

    return generate;
};

export default useGenerate;
