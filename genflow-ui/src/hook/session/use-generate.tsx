// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import { Dispatch, SetStateAction } from 'react';
import { fetchUtils } from 'react-admin';

import {
    GenerateRequest,
    ChatResponse,
    ChatResponseType,
    SessionMessage,
} from '@/types';
import { createFetchOptions, fetchJsonWithAuthToken } from '@/utils';

const processMessage = (
    message: ChatResponse,
    fullText: string,
    lastSessionMessage: SessionMessage,
    setSessionMessages: Dispatch<SetStateAction<SessionMessage[] | []>>,
): string => {
    let text = '';
    if (message.type === ChatResponseType.ERROR) {
        throw new Error(message.data as string);
    }
    if (message.type === ChatResponseType.CHUNK) {
        text = message.data as string;
        setSessionMessages((prev: SessionMessage[]) => prev.map((sessionMessage) => {
            if (sessionMessage.id === lastSessionMessage.id) {
                const updatedChatMessage: SessionMessage = {
                    ...sessionMessage,
                    answer: fullText + text,
                }
                return updatedChatMessage
            }
            return sessionMessage
        }));
    }
    if (message.type === ChatResponseType.MESSAGE) {
        setSessionMessages((prev: SessionMessage[]) => prev.map((sessionMessage) => {
            if (sessionMessage.id === lastSessionMessage.id) {
                const updatedChatMessage: SessionMessage = message.data as SessionMessage;
                return updatedChatMessage
            }
            return sessionMessage
        }));
    }
    return text;
};

// TODO: fix this
// eslint-disable-next-line @typescript-eslint/no-unused-vars
const fallbackToHttpStream = async (
    fallbackURL: string,
    options: fetchUtils.Options,
    generateRequest: GenerateRequest,
    lastSessionMessage: SessionMessage,
    setSessionMessages: Dispatch<SetStateAction<SessionMessage[] | []>>
): Promise<void> => new Promise((resolve, reject) => {
    const { user, headers } = options;
    if (!user || !user.token || !headers) {
        reject(new Error('Not authenticated'));
        return;
    }
    const requestHeaders = options.headers as Headers;
    options.method = 'POST';
    options.body = JSON.stringify(generateRequest);
    requestHeaders.set('Authorization', user.token)
    requestHeaders.set('Content-Type', 'application/json');
    fetch(fallbackURL, { ...options, headers: requestHeaders }).then((response) => {
        let fullText = '';

        const reader = response.body?.getReader();
        const decoder = new TextDecoder('utf-8');
        if (!reader) {
            reject(new Error('HTTP response body is not readable'));
        }

        let buffer = '';
        let done = false;

        const processChunk = async (): Promise<void> => {
            if (!reader) {
                reject(new Error('HTTP response body is not readable'));
                return;
            }
            const { value, done: readerDone }: { value?: Uint8Array; done: boolean } = await reader.read();
            done = readerDone;
            if (readerDone) {
                return;
            }
            if (value) {
                // Decode the chunk and append it to the buffer
                const chunk = decoder.decode(value, { stream: true });
                buffer += chunk;
                // Process complete JSON objects in the buffer
                let boundary = buffer.indexOf('\n\n');
                while (boundary !== -1) {
                    const jsonString = buffer.slice(0, boundary).trim();
                    buffer = buffer.slice(boundary + 1);
                    try {
                        const message = JSON.parse(jsonString) as ChatResponse;
                        fullText += processMessage(message, fullText, lastSessionMessage, setSessionMessages);
                    }
                    catch {
                        reject(new Error('Failed to handle message'));
                        return;
                    }
                    // next chunk
                    boundary = buffer.indexOf('\n');
                }
            }
        };

        let iterationCount = 0;
        const maxIterations = 1000;
        while (!done && iterationCount < maxIterations) {
            processChunk().catch((err) => reject(err));
            iterationCount++;
        }
        resolve();
    }).catch((error) => {
        console.log(error);
        reject(new Error('HTTP fallback failed'));
    })
});

const fallbackToHttp = async (
    fallbackURL: string,
    generateRequest: GenerateRequest,
    lastSessionMessage: SessionMessage,
    setSessionMessages: Dispatch<SetStateAction<SessionMessage[] | []>>
): Promise<void> => fetchJsonWithAuthToken(fallbackURL, {
    method: 'POST',
    body: JSON.stringify({
        ...generateRequest,
        stream: false,
    }),
}).then(({ json }) => {
    setSessionMessages((prev: SessionMessage[]) => prev.map((sessionMessage) => {
        if (sessionMessage.id === lastSessionMessage.id) {
            const updatedChatMessage: SessionMessage = json.data as SessionMessage;
            return updatedChatMessage
        }
        return sessionMessage
    }));
}).catch((error) => {
    throw new Error('Error during HTTP fallback:', error);
}
);

type GenerateHook = (
    url: string,
    fallbackURL: string,
    generateRequest: GenerateRequest,
    lastSessionMessage: SessionMessage,
    setSessionMessages: Dispatch<SetStateAction<SessionMessage[] | []>>
) => Promise<void>;

const useGenerate = (): GenerateHook => {
    const generate: GenerateHook = (
        url,
        fallbackURL,
        generateRequest,
        lastSessionMessage,
        setSessionMessages
    ): Promise<void> => new Promise((resolve, reject) => {
        let fullText = '';

        const options = createFetchOptions(url);
        const { user, headers } = options;
        if (!user || !user.token || !headers) {
            reject(new Error('Not authenticated'));
            return;
        }
        const teamId = (headers as Headers).get('X-Team');
        if (!teamId) {
            reject(new Error('X-Team header is missing'));
            return;
        }

        const webSocket = new WebSocket(url, [
            'json',
            user.token.replace('Token ', ''),
            teamId,
        ]);

        webSocket.onerror = (error) => {
            // Check if WebSocket is forbidden (e.g., HTTP 403 or network restrictions)
            if (error instanceof Event) {
                console.warn('WebSocket connection failed. Falling back to HTTP.');
                fallbackToHttp(fallbackURL, generateRequest, lastSessionMessage, setSessionMessages)
                    .then(() => {
                        resolve();
                    })
                    .catch((err) => {
                        reject(err);
                    });
            } else {
                reject(error);
            }

            webSocket.close();
        };

        // Handle incoming chunks
        webSocket.onmessage = (event) => {
            const message = JSON.parse(event.data as string) as ChatResponse;
            try {
                fullText += processMessage(message, fullText, lastSessionMessage, setSessionMessages);
                if (message.type === ChatResponseType.MESSAGE) {
                    resolve();
                    webSocket.close();
                }
            }
            catch (error) {
                console.error('Error processing message:', error);
                reject(error);
            }
        };

        webSocket.onopen = () => {
            webSocket.send(JSON.stringify(generateRequest));
        };
    });

    return generate;
};

export default useGenerate;
