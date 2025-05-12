// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import { Title, useGetList, useTranslate } from 'react-admin';

import { Prompt, Assistant, Session } from '@/types';
import { ResourceTotalCard } from '@/common';
import { AssistantResourceProps } from '@/assistant';
import { PromptResourceProps } from '@/prompt';
import { SessionResourceProps } from '@/session';
import ResourcesGridList from './ResourcesGridList';

type DashboardProps = object;

const Dashboard: FC<DashboardProps> = () => {
    const translate = useTranslate();
    const {
        data: prompts,
        total: totalPrompts,
        isPending: IsLoadingPrompts
    } = useGetList<Prompt>('prompts', {});

    const {
        data: assistants,
        total: totalAssistants,
        isPending: IsLoadingAssistants
    } = useGetList<Assistant>('assistants', {});

    const { total: totalSessions, isLoading: IsLoadingSessions } = useGetList<Session>('sessions', {});

    return (
        <Box m={2}>
            <Title title='ra.page.dashboard' />
            <Grid container spacing={2}>
                <Grid
                    size={{ xs: 12 }}
                >
                    <Grid container spacing={2}>
                        <Grid
                            size={{ xs: 12, sm: 12, md: 4 }}
                        >
                            <ResourceTotalCard
                                resource='assistants'
                                total={totalAssistants}
                                isLoading={IsLoadingAssistants}
                                icon={AssistantResourceProps.icon}
                            />
                        </Grid>
                        <Grid
                            size={{ xs: 12, sm: 12, md: 4 }}
                        >
                            <ResourceTotalCard
                                resource='prompts'
                                total={totalPrompts}
                                isLoading={IsLoadingPrompts}
                                icon={PromptResourceProps.icon}
                            />
                        </Grid>
                        <Grid
                            size={{ xs: 12, sm: 12, md: 4 }}
                        >
                            <ResourceTotalCard
                                resource='sessions'
                                total={totalSessions}
                                isLoading={IsLoadingSessions}
                                icon={SessionResourceProps.icon}
                            />
                        </Grid>
                    </Grid>
                </Grid>
                <Grid
                    size={{ xs: 12 }}
                >
                    <Typography
                        variant='overline'
                        gutterBottom
                    >
                        {translate('label.favorite_resources')}
                    </Typography>
                    <Divider
                        sx={{ mb: 2 }}
                    />
                    <ResourcesGridList
                        prompts={prompts || []}
                        assistants={assistants || []}
                        isPending={IsLoadingPrompts || IsLoadingAssistants}
                    />
                </Grid>
            </Grid>
        </Box>
    );
};

export default Dashboard;
