// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import BiotechIcon from '@mui/icons-material/Biotech';
import PublishIcon from '@mui/icons-material/Publish';
import UnpublishedIcon from '@mui/icons-material/Unpublished';
import SaveAsIcon from '@mui/icons-material/SaveAs';
import {
    TopToolbar, SaveButton, Button, useRedirect,
    useDataProvider, CreateResult, useRecordContext,
} from 'react-admin';

import {
    PromptStatus, Prompt, SessionType,
    SessionMode, Session,
} from '@/types';
import { CancelButton } from '@/common';

interface PromptFormActionsProps {
    testing: boolean;
    setTesting: (value: boolean) => void;
    createMode: boolean;
};

const PromptFormActions: FC<PromptFormActionsProps> = ({
    testing,
    setTesting,
    createMode,
}) => {
    const redirect = useRedirect();
    const dataProvider = useDataProvider();
    const prompt = useRecordContext<Prompt>();

    const transformToPublish = (data: any): Prompt => ({
        ...data,
        status: data.status === PromptStatus.PUBLISHED ? PromptStatus.DRAFTED : PromptStatus.PUBLISHED,
    });

    const createTestSession = async (data: Prompt): Promise<CreateResult<Session>> => (
        dataProvider.create(
            'sessions',
            {
                data: {
                    name: `Testing - ${data.name}`,
                    session_type: SessionType.PROMPT,
                    session_mode: SessionMode.COMPLETION,
                    related_prompt: data.id,
                },
                meta: {
                    queryParams: {
                        testing: true,
                    },
                },
            })
    );

    const renderPublishButton = (currentPrompt: Prompt | undefined): JSX.Element | null => (currentPrompt ? (
        <SaveButton
            type='button'
            label={currentPrompt.status === PromptStatus.PUBLISHED ? 'action.unpublish' : 'action.publish'}
            variant='outlined'
            icon={currentPrompt.status === PromptStatus.PUBLISHED ? (
                <UnpublishedIcon />
            ) : (
                <PublishIcon />
            )}
            alwaysEnable
            transform={transformToPublish}
        />
    ) : null)

    const renderTestButton = (): JSX.Element => (
        <SaveButton
            type='button'
            label='action.test'
            mutationOptions={{
                onSuccess: (data: Prompt) => {
                    setTesting(true);
                    if (!data.related_test_session) {
                        createTestSession(data).then(() => {
                            redirect('edit', 'prompts', data.id, data);
                        });
                    } else {
                        redirect('edit', 'prompts', data.id, data);
                    }
                }
            }}
            icon={<BiotechIcon />}
            variant='outlined'
            alwaysEnable={!createMode}
        />
    );

    return (
        <TopToolbar>
            <CancelButton
                onClick={() => redirect('list', 'prompts')}
                size='medium'
                variant='outlined'
                color='warning'
            />
            {
                testing ? (
                    <Button
                        label='ra.action.edit'
                        onClick={() => setTesting(false)}
                        size='medium'
                        variant='outlined'
                    />
                ) : (
                    renderTestButton()
                )
            }
            {
                createMode ? (
                    <SaveButton
                        type='button'
                        label='action.draft'
                        variant='outlined'
                        icon={<SaveAsIcon />}
                    />
                ) : (
                    renderPublishButton(prompt)
                )
            }
        </TopToolbar>
    );
};

export default PromptFormActions;
