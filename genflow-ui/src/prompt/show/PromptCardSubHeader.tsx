// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT
import React, { FC } from 'react';
import Stack from '@mui/material/Stack';
import Tooltip from '@mui/material/Tooltip';
import DraftsIcon from '@mui/icons-material/Drafts';
import PublishedWithChangesIcon from '@mui/icons-material/PublishedWithChanges';
import TextSnippetIcon from '@mui/icons-material/TextSnippet';
import SettingsInputSvideoIcon from '@mui/icons-material/SettingsInputSvideo';
import { useRecordContext, ReferenceField } from 'react-admin';

import {
    Prompt, PromptStatus, PromptType,
} from '@/types';
import { GroupField, GroupFieldSlot } from '@/group';

type PromptCardSubHeaderProps = object;

const PromptCardSubHeader: FC<PromptCardSubHeaderProps> = () => {
    const prompt = useRecordContext<Prompt>();
    if (!prompt) {
        return null;
    }

    const renderType = (type: PromptType): JSX.Element => (
        <Tooltip
            title={type.toUpperCase()}
        >
            { type === PromptType.SIMPLE ? (
                <TextSnippetIcon color='success' />
            ) : (
                <SettingsInputSvideoIcon color='success' />
            )}
        </Tooltip>
    );

    const renderStatus = (status: PromptStatus): JSX.Element => (
        <Tooltip title={status.toUpperCase()}>
            { status === PromptStatus.DRAFTED ? (
                <DraftsIcon color='warning' />
            ) : (
                <PublishedWithChangesIcon color='success' />
            )}
        </Tooltip>
    );

    return (
        <Stack
            direction='row'
            spacing={1}
            mt={1}
        >
            <ReferenceField
                source='group.id'
                reference='prompt-groups'
            >
                <GroupField
                    slots={[GroupFieldSlot.COLOR]}
                />
            </ReferenceField>
            {
                renderType(prompt.type)
            }
            {
                renderStatus(prompt.status)
            }
        </Stack>
    );
};

export default PromptCardSubHeader;
