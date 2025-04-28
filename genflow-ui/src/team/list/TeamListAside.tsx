// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Box from '@mui/material/Box';
import Divider from '@mui/material/Divider';
import Typography from '@mui/material/Typography';
import { styled } from '@mui/material/styles';
import { useGetResourceLabel, useRecordContext } from 'react-admin';

import { Team } from '@/types';
import { MembershipList } from '@/team/membership';
import { TeamShow } from '@/team/show';

const Root = styled(Box, {
    name: 'GFTeamListAside',
    slot: 'root',
})(({ theme }) => ({
    margin: theme.spacing(2),
    maxWidth: '700px',
}));

const StyledDivider = styled(Divider, {
    name: 'GFTeamListAside',
    slot: 'divider',
})(({ theme }) => ({
    marginTop: theme.spacing(2),
    marginBottom: theme.spacing(2),
}));

type TeamListAsideProps = object;

const TeamListAside: FC<TeamListAsideProps> = () => {
    const getResourceLabel = useGetResourceLabel();
    const team = useRecordContext<Team>();

    if (!team) {
        return null;
    }

    return (
        <Root>
            <TeamShow />
            <StyledDivider />
            <Card>
                <CardContent>
                    <Typography
                        variant='subtitle1'
                        color='textSecondary'
                    >
                        {getResourceLabel('memberships')}
                    </Typography>
                    <MembershipList />
                </CardContent>
            </Card>
        </Root>
    );
};

export default TeamListAside;
