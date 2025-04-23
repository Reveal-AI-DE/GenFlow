// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import BiotechIcon from '@mui/icons-material/Biotech';
import PublishIcon from '@mui/icons-material/Publish';
import UnpublishedIcon from '@mui/icons-material/Unpublished';
import SaveAsIcon from '@mui/icons-material/SaveAs';
import {
    TopToolbar, SaveButton, Button,
    useRedirect, useRecordContext,
} from 'react-admin';

import {
    PromptStatus, Prompt, PromptData,
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
    const prompt = useRecordContext<Prompt>();

    const transform = (values: Prompt): PromptData => {
        const { group, related_model: relatedModel, ...rest } = values;
        const { provider_name: providerName, model_name: modelName, config } = relatedModel;
        return ({
            group_id: group.id,
            related_model: {
                provider_name: providerName,
                model_name: modelName,
                config,
            },
            ...rest,
        })
    };

    const transformToPublish = (data: Prompt): PromptData => ({
        ...transform(data),
        prompt_status: data.prompt_status === PromptStatus.PUBLISHED ? PromptStatus.DRAFTED : PromptStatus.PUBLISHED,
    });

    const renderPublishButton = (currentPrompt: Prompt | undefined): JSX.Element | null => (currentPrompt ? (
        <SaveButton
            type='button'
            label={currentPrompt.prompt_status === PromptStatus.PUBLISHED ? 'action.unpublish' : 'action.publish'}
            variant='outlined'
            icon={currentPrompt.prompt_status === PromptStatus.PUBLISHED ? (
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
                    redirect('edit', 'prompts', data.id, data);
                }
            }}
            icon={<BiotechIcon />}
            variant='outlined'
            alwaysEnable={!createMode}
            transform={transform}
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
                        transform={transform}
                    />
                ) : (
                    renderPublishButton(prompt)
                )
            }
        </TopToolbar>
    );
};

export default PromptFormActions;
