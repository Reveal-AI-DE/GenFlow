// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import { RaRecord } from 'react-admin'

import { FileEntity } from '@/types/common';
import { ModelConfigWithEntity, Parameters } from '@/types/model';
import { Prompt } from '@/types/prompt';

export enum SessionType {
    LLM = 'llm',
};

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
    session_type: string;
    session_mode: string;
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
};

export enum SessionFloatActionKey {
    SETTINGS = 'settings',
    INFO = 'info',
    USAGE = 'usage',
    NEW = 'new',
};
