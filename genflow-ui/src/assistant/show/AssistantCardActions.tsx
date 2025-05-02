// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import IconButton from '@mui/material/IconButton';
import TerminalIcon from '@mui/icons-material/Terminal';
import {
    useRecordContext, useDataProvider,
    useRedirect, useTranslate, useNotify,
} from 'react-admin';

import {
    Assistant, AssistantStatus,
} from '@/types';
import { EntityCardActions } from '@/entity';
import { WithTooltip } from '@/common';

type AssistantCardActionsProps = object;

const AssistantCardActions: FC<AssistantCardActionsProps> = () => {
    const assistant = useRecordContext<Assistant>();

    const dataProvider = useDataProvider();
    const redirect = useRedirect();
    const translate = useTranslate();
    const notify = useNotify();

    if (!assistant) {
        return null;
    }

    const OnUseClick = (): void => {
        if (assistant.assistant_status !== AssistantStatus.PUBLISHED) {
            return;
        }
        const data = {
            name: 'New Chat',
            session_type: 'assistant',
            session_mode: 'chat',
            related_assistant: assistant.id,
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
                            disabled={assistant.assistant_status !== AssistantStatus.PUBLISHED}
                        >
                            <TerminalIcon />
                        </IconButton>
                    </span>
                )}
            />
        </EntityCardActions>
    );
};

export default AssistantCardActions;
