// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import { Dispatch, SetStateAction } from 'react';
import {
    SessionMessage, Session, FileEntity, GenerateRequest,
} from '@/types';

import { ResourceURL } from '@/utils/dataProvider';

export const createTemporaryMessage = (
    query: string,
    sessionMessages: SessionMessage[],
    setSessionMessages: Dispatch<SetStateAction<SessionMessage[] | []>>,
    isRegeneration: boolean
): SessionMessage => {
    const tempMessage: SessionMessage = {
        id: 'tmp',
        session_id: '',
        query,
        answer: '',
    };

    let newMessages = [];

    if (isRegeneration) {
        const lastMessageIndex = sessionMessages.length - 1
        sessionMessages[lastMessageIndex].answer = ''
        newMessages = [...sessionMessages]
    } else {
        newMessages = [
            ...sessionMessages,
            tempMessage,
        ]
    }

    setSessionMessages(newMessages)

    return tempMessage;
};

export const createGenerateRequest = (
    query: string,
    files: FileEntity[],
): GenerateRequest | null => ({
    query,
    files,
    // TODO: add parameters
});

export const createGenerateURL = (
    session: Session, base = process.env.REACT_APP_BACKEND_WS_URL
): string => (
    ResourceURL(`/sessions/${session.id}/generate`, base)
);
