// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import { Dispatch, SetStateAction } from 'react';
import {
    SessionMessage, Session, FileEntity, ChatSetting,
    GenerateRequest, ChatModelSetting,
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

    let newMessages: SessionMessage[] = [];

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
    chatSetting: ChatSetting,
    stream: boolean = true,
): GenerateRequest | null => ({
    query,
    files,
    parameters: (chatSetting as ChatModelSetting).parameters,
    stream,
});

export const createGenerateURL = (
    session: Session, base = process.env.REACT_APP_BACKEND_WS_URL
): string => (
    ResourceURL(`/sessions/${session.id}/generate`, base)
);
