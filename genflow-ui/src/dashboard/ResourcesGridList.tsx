// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import Skeleton from '@mui/material/Skeleton';
import Grid from '@mui/material/Grid2';
import Box from '@mui/material/Box';
import {
    RecordContextProvider, ResourceContextProvider,
} from 'react-admin';

import { useColsForWidth, times } from '@/utils';
import { Prompt, Assistant } from '@/types';
import { PromptCard } from '@/prompt';
import { AssistantCard } from '@/assistant';

type ResourcesLoadingGridListProps = object;

const ResourcesLoadingGridList: FC<ResourcesLoadingGridListProps> = () => {
    const cols = useColsForWidth();

    return (
        <Grid container columns={cols*8} spacing={2}>
            {times(cols*2, (key) => (
                <Grid key={key} size={8}>
                    <Skeleton
                        height='180px'
                        variant='rectangular'
                        animation='wave'
                    />
                </Grid>
            ))}
        </Grid>
    );
};

export interface ResourcesGridListProps {
    isPending: boolean;
    prompts: Prompt[];
    assistants: Assistant[];
};

const ResourcesLoadedGridList: FC<Omit<ResourcesGridListProps, 'isPending'>> = ({
    assistants,
    prompts,
}) => {
    const cols = useColsForWidth();

    if (!assistants && !prompts) return null;

    if (prompts.length === 0 && assistants.length === 0) return null;

    const renderItem = (): JSX.Element[] => {
        const maxLength = Math.max(prompts.length, assistants.length);
        const mergedArray = [];
        for (let i = 0; i < maxLength; i++) {
            if (i < assistants.length && assistants[i].is_pinned) {
                mergedArray.push(
                    <Grid
                        key={assistants[i].id}
                        size={8}
                    >
                        <ResourceContextProvider value='assistants'>
                            <RecordContextProvider value={assistants[i]}>
                                <AssistantCard />
                            </RecordContextProvider>
                        </ResourceContextProvider>
                    </Grid>
                );
            }
            if (i < prompts.length && prompts[i].is_pinned) {
                mergedArray.push(
                    <Grid
                        key={prompts[i].id}
                        size={8}
                    >
                        <ResourceContextProvider value='prompts'>
                            <RecordContextProvider value={prompts[i]}>
                                <PromptCard />
                            </RecordContextProvider>
                        </ResourceContextProvider>
                    </Grid>
                );
            }
        }

        return mergedArray.slice(0, cols*2);
    };

    return (
        <Box sx={{ flexGrow: 1 }}>
            <Grid
                container
                columns={cols*8}
                spacing={2}
            >
                {renderItem()}
            </Grid>
        </Box>
    );
};

const ResourcesGridList: FC<ResourcesGridListProps> = ({
    isPending,
    prompts,
    assistants,
}) => (isPending ? (
    <ResourcesLoadingGridList />
) : (
    <ResourcesLoadedGridList
        prompts={prompts}
        assistants={assistants}
    />
));

export default ResourcesGridList;
