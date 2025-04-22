// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC, useContext } from 'react';
import Avatar from '@mui/material/Avatar';
import CheckIcon from '@mui/icons-material/Check';
import Typography from '@mui/material/Typography';
import { styled } from '@mui/material/styles';
import { useTranslate, useGetList, useGetIdentity } from 'react-admin';

import { Team } from '@/types';
import { GlobalContext } from '@/context';
import { NestedMenuItem, IconMenuItem } from '@/common';

export const StyledTypography = styled(Typography, {
    name: 'GFTeamMenuItem',
    slot: 'header',
})(({ theme }) => ({
    margin: theme.spacing(1, 2 , 1, 2),
}));

export const StyledAvatar = styled(Avatar, {
    name: 'GFTeamMenuItem',
    slot: 'avatar',
})(() => ({
    width: 24,
    height: 24
}));

const TeamMenuItem: FC = () => {
    const { data: currentUser } = useGetIdentity();

    const translate = useTranslate();
    const {
        currentTeam, switchTeam
    } = useContext(GlobalContext);

    const onClick = (team: Team): void => {
        if (currentUser) switchTeam(team, currentUser);
    };

    const { data: userTeams } = useGetList('teams', { pagination: { page: 1, perPage: -1 } });

    return userTeams && (
        <>
            <StyledTypography variant='subtitle2'>
                {translate('resources.teams.name', { smart_count: 1 })}
            </StyledTypography>
            <NestedMenuItem
                label={currentTeam?.name}
                leftIcon={(
                    <StyledAvatar>
                        {currentTeam?.name[0].toUpperCase()}
                    </StyledAvatar>
                )}
                divider
            >
                {
                    userTeams.map((team: Team) => (
                        <IconMenuItem
                            key={team.id}
                            label={team.name}
                            onClick={currentTeam?.id !== team.id ? () => onClick(team) : undefined}
                            leftIcon={(
                                <StyledAvatar>
                                    {team?.name[0].toUpperCase()}
                                </StyledAvatar>
                            )}
                            rightIcon={currentTeam?.id === team.id ? <CheckIcon color='primary' /> : undefined}
                        />
                    ))
                }
            </NestedMenuItem>
        </>
    );
};

export default TeamMenuItem;
