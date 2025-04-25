// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import IconButton from '@mui/material/IconButton';
import TerminalIcon from '@mui/icons-material/Terminal';
import {
    useRecordContext, useDataProvider,
    useRedirect, useTranslate, useNotify,
} from 'react-admin';

import { Prompt, PromptStatus } from '@/types';
import { WithTooltip } from '@/common';
import { EntityCardActions } from '@/entity';

type PromptCardActionsProps = object;

const PromptCardActions: FC<PromptCardActionsProps> = () => {
    const prompt = useRecordContext<Prompt>();
    const dataProvider = useDataProvider();
    const redirect = useRedirect();
    const translate = useTranslate();
    const notify = useNotify();

    if (!prompt) {
        return null;
    }

    const OnUseClick = (): void => {
        if (prompt.prompt_status !== PromptStatus.PUBLISHED) {
            return;
        }
        const data = {
            name: 'New Chat',
            session_type: 'prompt',
            session_mode: 'chat',
            related_prompt: prompt.id,
        };
        dataProvider.create('sessions', { data }).then((response) => {
            const { data: session } = response;
            redirect('show', 'sessions', session.id);
        }).catch(() => notify(
            'ra.notification.http_error',
            {
                type: 'error',
            }));
    };

    return (
        <EntityCardActions>
            <WithTooltip
                title={translate('action.use')}
                trigger={(
                    <span>
                        <IconButton
                            size='small'
                            onClick={OnUseClick}
                            color='primary'
                            disabled={prompt.prompt_status !== PromptStatus.PUBLISHED}
                        >
                            <TerminalIcon />
                        </IconButton>
                    </span>
                )}
            />
        </EntityCardActions>
    );
};

export default PromptCardActions;
