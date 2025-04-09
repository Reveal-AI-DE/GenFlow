// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import { RaRecord } from 'react-admin'

import { ModelConfigWithEntity } from '@/types/model';

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
