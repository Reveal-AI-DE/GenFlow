// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import { Identifier } from 'react-admin';

import {
    EntityGroup, CommonEntity, AIAssociatedEntity,
    CommonEntityData, AIAssociatedEntityData,
} from '@/types/common';

export type PromptGroup = EntityGroup;

export enum PromptType {
    SIMPLE = 'simple',
    ADVANCED = 'advanced',
};

export enum PromptStatus {
    DRAFTED = 'drafted',
    PUBLISHED = 'published',
};

export interface Question {
    question: string;
};

export interface CommonPrompt {
    pre_prompt: string;
    suggested_questions: Question[];
    prompt_type: PromptType;
};

export interface Prompt extends CommonEntity, AIAssociatedEntity, CommonPrompt {
    prompt_status: PromptStatus;
    related_test_session: Identifier | undefined;
};

export interface PromptData extends CommonEntityData, AIAssociatedEntityData, CommonPrompt {
    prompt_status: PromptStatus;
}

export type ChatPromptSetting = object;
