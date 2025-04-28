// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import { RaRecord } from 'react-admin'

import { FileEntity } from '@/types/file';
import { ModelConfigWithEntity, Parameters, ChatModelSetting } from '@/types/model';
import { Prompt, ChatPromptSetting } from '@/types/prompt';

export enum SessionType {
    LLM = 'llm',
    PROMPT = 'prompt',
    ASSISTANT = 'assistant',
};

export enum SessionMode {
    CHAT = 'chat',
    COMPLETION = 'completion',
}

export interface SessionDailyUsage {
    day: string;
    total_messages: number;
    total_price: number;
}

export interface SessionUsage {
    total_messages: number;
    total_input_tokens: number;
    total_output_tokens: number;
    total_price: number;
    total_input_price: number;
    total_output_price: number;
    currency: string;
    per_day: SessionDailyUsage[];
}

export interface Session extends RaRecord {
    name: string;
    session_type: SessionType;
    session_mode: SessionMode;
    related_model?: ModelConfigWithEntity;
    related_prompt?: Prompt | undefined;
    created_at?: string;
    updated_at?: string;
    usage?: SessionUsage;
};

export interface GenerateRequest {
    query: string;
    files?: FileEntity[];
    parameters?: Parameters;
    stream?: boolean;
};

export enum SessionFloatActionKey {
    SETTINGS = 'settings',
    INFO = 'info',
    USAGE = 'usage',
    NEW = 'new',
};

export type ChatSetting = ChatModelSetting | ChatPromptSetting;
