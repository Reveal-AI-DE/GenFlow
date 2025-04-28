// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import {
    EntityGroup, CommonEntity, AIAssociatedEntity,
    CommonEntityData, AIAssociatedEntityData,
} from '@/types/common';
import { FileEntity } from '@/types/file';
import { CommonPrompt } from '@/types/prompt';

export type AssistantGroup = EntityGroup;

export enum ContextSource {
    FILES = 'files',
    COLLECTIONS = 'collections',
};

export enum AssistantStatus {
    DRAFTED = 'drafted',
    PUBLISHED = 'published',
};

export interface Assistant extends CommonEntity, AIAssociatedEntity, CommonPrompt {
    opening_statement: string;
    assistant_status: AssistantStatus;
    files: FileEntity[];
};

export interface AssistantData extends CommonEntityData, AIAssociatedEntityData, CommonPrompt {
    opening_statement: string;
    assistant_status: AssistantStatus;
}
