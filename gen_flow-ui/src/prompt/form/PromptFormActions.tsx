// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import BiotechIcon from '@mui/icons-material/Biotech';
import PublishIcon from '@mui/icons-material/Publish';
import SaveAsIcon from '@mui/icons-material/SaveAs';
import {
    TopToolbar, SaveButton, Button,
    useRedirect,
} from 'react-admin';

import { PromptStatus, Prompt } from '@/types';
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

    const transformToPublish = (data: any): Prompt => ({
        ...data,
        status: PromptStatus.PUBLISHED,
    });

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
                    <SaveButton
                        type='button'
                        label='action.test'
                        mutationOptions={{
                            meta: {
                                queryParams: {
                                    testing: true,
                                },
                            },
                            onSuccess: (data) => {
                                setTesting(true);
                                redirect('edit', 'prompts', data.id, data);
                            }
                        }}
                        icon={<BiotechIcon />}
                        variant='outlined'
                        alwaysEnable={!createMode}
                    />
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
                    <SaveButton
                        type='button'
                        label='action.publish'
                        variant='outlined'
                        icon={<PublishIcon />}
                        alwaysEnable
                        transform={transformToPublish}
                    />
                )
            }
        </TopToolbar>
    );
};

export default PromptFormActions;
