// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import { RaRecord } from 'react-admin'

import { FileEntity } from '@/types/common';
import { ModelConfigWithEntity, Parameters } from '@/types/model';

export enum SessionType {
    LLM = 'llm',
};

export interface Session extends RaRecord {
    name: string;
    session_type: string;
    session_mode: string;
    related_model?: ModelConfigWithEntity;
    created_at?: string;
    updated_at?: string;
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
