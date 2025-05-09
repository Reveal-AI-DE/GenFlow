// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import { RaRecord } from 'react-admin';

export interface SessionMessage extends RaRecord {
    query: string;
    answer: string
    owner?: string;
    created_at?: number;
    updated_at?: number;
}

export interface ChatBotMessage extends RaRecord {
    content: string;
    role: string;
    owner?: string;
};

export enum ChatResponseType {
    CHUNK = 'chunk',
    MESSAGE = 'message',
    ERROR = 'error',
};

export interface ChatResponse {
    type: ChatResponseType;
    data: string | SessionMessage;
};
