// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC, useContext, ReactNode } from 'react';
import Card from '@mui/material/Card';
import CardHeader from '@mui/material/CardHeader';
import CardContent from '@mui/material/CardContent';
import Avatar from '@mui/material/Avatar';
import Typography from '@mui/material/Typography';
import Tooltip from '@mui/material/Tooltip';
import { styled } from '@mui/material/styles';
import { useRecordContext } from 'react-admin';

import {
    CommonEntity, TeamRole
} from '@/types';
import { GlobalContext } from '@/context';
import { PinButton } from '@/common';
import { truncateText } from '@/utils';

const StyledCard = styled(Card, {
    name: 'GFEntityCard',
    slot: 'root',
})(() => ({
    display: 'flex',
    flexDirection: 'column',
    height: '100%',
}));

const StyledCardHeader = styled(CardHeader, {
    name: 'GFEntityCard',
    slot: 'header',
})(() => ({
    padding: '8px 16px',
}));

const StyledCardContent = styled(CardContent, {
    name: 'GFEntityCard',
    slot: 'content',
})(() => ({
    flexGrow: 1,
    padding: '8px 16px',
}));

const StyledAvatar = styled(Avatar, {
    name: 'GFEntityCard',
    slot: 'avatar',
})(() => ({
    width: 100,
    height: 100
}));

const StyledTitle = styled(Typography, {
    name: 'GFEntityCard',
    slot: 'title',
})(() => ({
    fontWeight: 'bold',
    lineHeight: 1.2,
}));

interface EntityCardProps {
    subHeader: ReactNode;
    actions?: ReactNode;
};

const EntityCard: FC<EntityCardProps> = ({
    subHeader,
    actions,
}) => {
    const entity = useRecordContext<CommonEntity>();
    const { currentMembership } = useContext(GlobalContext);

    if (!entity) {
        return null;
    }

    const isOwnerOrAdmin = currentMembership?.role === TeamRole.OWNER || currentMembership?.role === TeamRole.ADMIN;

    return (
        <StyledCard>
            <StyledCardHeader
                avatar={(
                    <StyledAvatar
                        src={entity.avatar}
                        alt={entity.name}
                    >
                        {!entity.avatar && entity.name[0]}
                    </StyledAvatar>
                )}
                title={(
                    <StyledTitle
                        variant='subtitle1'
                        gutterBottom
                    >
                        {entity.name}
                    </StyledTitle>
                )}
                subheader={subHeader}
                action={(
                    <PinButton
                        disabled={!isOwnerOrAdmin}
                    />
                )}
                disableTypography
            />
            <StyledCardContent>
                <Tooltip title={entity.description}>
                    <Typography
                        variant='subtitle2'
                        gutterBottom
                    >
                        {truncateText(entity.description, 20)}
                    </Typography>
                </Tooltip>
            </StyledCardContent>
            {actions}
        </StyledCard>
    );
};

export default EntityCard;
