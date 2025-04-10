// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import { RaRecord, Identifier } from 'react-admin';

import { Group } from '@/types/common';
import { ModelConfigWithEntity } from '@/types/model';

export type PromptGroup = Group;

export enum PromptType {
    SIMPLE = 'simple',
    ADVANCED = 'advanced',
};

export enum PromptStatus {
    DRAFTED = 'drafted',
    PUBLISHED = 'published',
};

export interface Prompt extends RaRecord {
    name: string;
    description: string;
    pre_prompt: string;
    suggested_questions: {
        question: string;
    }[];
    type: PromptType;
    status: PromptStatus;
    avatar: string;
    related_model: ModelConfigWithEntity;
    group_id: Identifier;
    related_test_session: Identifier | undefined;
    is_pinned: boolean;
};
