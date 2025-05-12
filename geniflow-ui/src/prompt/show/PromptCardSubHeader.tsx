// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import Tooltip from '@mui/material/Tooltip';
import DraftsIcon from '@mui/icons-material/Drafts';
import PublishedWithChangesIcon from '@mui/icons-material/PublishedWithChanges';
import { useRecordContext, ReferenceField } from 'react-admin';

import {
    Prompt, PromptStatus,
} from '@/types';
import { GroupField, GroupFieldSlot } from '@/group';
import { EntityCardSubHeader } from '@/entity';

type PromptCardSubHeaderProps = object;

const PromptCardSubHeader: FC<PromptCardSubHeaderProps> = () => {
    const prompt = useRecordContext<Prompt>();
    if (!prompt) {
        return null;
    }

    const renderStatus = (prompt_status: string): JSX.Element => (
        <Tooltip title={prompt_status.toUpperCase()}>
            { prompt_status === PromptStatus.DRAFTED ? (
                <DraftsIcon color='warning' />
            ) : (
                <PublishedWithChangesIcon color='success' />
            )}
        </Tooltip>
    );

    return (
        <EntityCardSubHeader
            statusSource='prompt_status'
            renderStatus={renderStatus}
        >
            <ReferenceField
                source='group.id'
                reference='prompt-groups'
            >
                <GroupField
                    slots={[GroupFieldSlot.COLOR]}
                />
            </ReferenceField>
        </EntityCardSubHeader>
    );
};

export default PromptCardSubHeader;
