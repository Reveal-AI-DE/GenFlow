// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC, useContext } from 'react';
import Card from '@mui/material/Card';
import CardHeader from '@mui/material/CardHeader';
import CardContent from '@mui/material/CardContent';
import Avatar from '@mui/material/Avatar';
import Typography from '@mui/material/Typography';
import Tooltip from '@mui/material/Tooltip';
import { styled } from '@mui/material/styles';
import { useRecordContext } from 'react-admin';

import {
    Prompt, TeamRole
} from '@/types';
import { GlobalContext } from '@/context';
import { PinButton } from '@/common';
import { truncateText } from '@/utils';
import PromptCardActions from '@/prompt/show/PromptCardActions';
import PromptCardSubHeader from '@/prompt/show/PromptCardSubHeader';

const StyledCard = styled(Card, {
    name: 'GFPromptCard',
    slot: 'root',
})(() => ({
    display: 'flex',
    flexDirection: 'column',
    height: '100%',
}));

const StyledCardHeader = styled(CardHeader, {
    name: 'GFPromptCard',
    slot: 'header',
})(() => ({
    padding: '8px 16px',
}));

const StyledCardContent = styled(CardContent, {
    name: 'GFPromptCard',
    slot: 'content',
})(() => ({
    flexGrow: 1,
    padding: '8px 16px',
}));

const StyledAvatar = styled(Avatar, {
    name: 'GFPromptCard',
    slot: 'avatar',
})(() => ({
    width: 100,
    height: 100
}));

const StyledTitle = styled(Typography, {
    name: 'GFPromptCard',
    slot: 'title',
})(() => ({
    fontWeight: 'bold',
    lineHeight: 1.2,
}));

type PromptCardProps = object;

const PromptCard: FC<PromptCardProps> = () => {
    const prompt = useRecordContext<Prompt>();
    const { currentMembership } = useContext(GlobalContext);

    if (!prompt) {
        return null;
    }

    const isOwnerOrAdmin = currentMembership?.role === TeamRole.OWNER || currentMembership?.role === TeamRole.ADMIN;

    return (
        <StyledCard>
            <StyledCardHeader
                avatar={(
                    <StyledAvatar
                        src={prompt.avatar}
                        alt={prompt.name}
                    >
                        {!prompt.avatar && prompt.name[0]}
                    </StyledAvatar>
                )}
                title={(
                    <StyledTitle
                        variant='subtitle1'
                        gutterBottom
                    >
                        {prompt.name}
                    </StyledTitle>
                )}
                subheader={<PromptCardSubHeader />}
                action={(
                    <PinButton
                        disabled={!isOwnerOrAdmin}
                    />
                )}
                disableTypography
            />
            <StyledCardContent>
                <Tooltip title={prompt.description}>
                    <Typography
                        variant='subtitle2'
                        gutterBottom
                    >
                        {truncateText(prompt.description, 20)}
                    </Typography>
                </Tooltip>
            </StyledCardContent>
            <PromptCardActions />
        </StyledCard>
    );
};

export default PromptCard;
