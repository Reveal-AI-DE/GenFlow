// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC, ReactNode } from 'react';
import Stack from '@mui/material/Stack';
import Tooltip from '@mui/material/Tooltip';
import TextSnippetIcon from '@mui/icons-material/TextSnippet';
import SettingsInputSvideoIcon from '@mui/icons-material/SettingsInputSvideo';
import { useRecordContext } from 'react-admin';
import get from 'lodash/get';

import {
    CommonPrompt, PromptType,
} from '@/types';

export interface EntityCardSubHeaderProps {
    statusSource?: string;
    renderStatus?: (status: string) => JSX.Element;
    children?: ReactNode;
};

const EntityCardSubHeader: FC<EntityCardSubHeaderProps> = ({
    statusSource = 'prompt_status',
    renderStatus,
    children,
}) => {
    const entity = useRecordContext<CommonPrompt>();
    if (!entity) {
        return null;
    }

    const entityStatus = statusSource ? get(entity, statusSource) : undefined;

    const renderType = (prompt_type: PromptType): JSX.Element => (
        <Tooltip
            title={prompt_type.toUpperCase()}
        >
            { prompt_type === PromptType.SIMPLE ? (
                <TextSnippetIcon color='success' />
            ) : (
                <SettingsInputSvideoIcon color='success' />
            )}
        </Tooltip>
    );

    return (
        <Stack
            direction='row'
            spacing={1}
            mt={1}
        >
            {children}
            {
                renderType(entity.prompt_type)
            }
            {
                renderStatus && entityStatus && renderStatus(entityStatus)
            }
        </Stack>
    );
};

export default EntityCardSubHeader;
