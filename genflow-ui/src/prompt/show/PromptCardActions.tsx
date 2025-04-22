// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC, useContext } from 'react';
import CardActions from '@mui/material/CardActions';
import IconButton from '@mui/material/IconButton';
import EditIcon from '@mui/icons-material/Edit';
import TerminalIcon from '@mui/icons-material/Terminal';
import {
    useRecordContext, useCreatePath, Link,
    useDataProvider, useRedirect, useTranslate,
    DeleteWithConfirmButton,
} from 'react-admin';

import { Prompt, PromptStatus, TeamRole } from '@/types';
import { GlobalContext, GlobalContextInterface } from '@/context';
import { WithTooltip } from '@/common';

type PromptInfoCardActionsProps = object;

const PromptCardActions: FC<PromptInfoCardActionsProps> = () => {
    const prompt = useRecordContext<Prompt>();
    if (!prompt) {
        return null;
    }

    const dataProvider = useDataProvider();
    const redirect = useRedirect();
    const translate = useTranslate();
    const createPath = useCreatePath();

    const { currentMembership } = useContext<GlobalContextInterface>(GlobalContext);
    const isOwnerOrAdmin = currentMembership?.role === TeamRole.OWNER || currentMembership?.role === TeamRole.ADMIN;

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
        });
    };

    return (
        <CardActions disableSpacing>
            <Link
                to={
                    isOwnerOrAdmin ? (
                        createPath({
                            resource: 'prompts',
                            id: prompt.id,
                            type: 'edit'
                        })) : ''
                }
                title={translate('ra.action.edit')}
            >
                <EditIcon
                    color={isOwnerOrAdmin ? 'primary' : 'disabled'}
                />
            </Link>
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
            <DeleteWithConfirmButton
                label=''
                mutationMode='pessimistic'
                size='small'
                title={translate('ra.action.delete')}
                disabled={!isOwnerOrAdmin}
                sx={{
                    ml: 'auto',
                    minWidth: 'auto',
                }}
            />
        </CardActions>
    );
};

export default PromptCardActions;
