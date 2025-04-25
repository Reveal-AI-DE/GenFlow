// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC, createElement } from 'react';
import Card from '@mui/material/Card';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Skeleton from '@mui/material/Skeleton';
import { styled } from '@mui/material/styles';
import { useTranslate } from 'react-admin';
import { Link } from 'react-router';

const StyledCard = styled(Card, {
    name: 'ResourceTotal',
    slot: 'root',
})(() => ({
    minHeight: 52,
    display: 'flex',
    flexDirection: 'column',
    flex: '1',
    height: '100%',
    '& a': {
        textDecoration: 'none',
        color: 'inherit',
    },
}));

const Content = styled(Box, {
    name: 'ResourceTotal',
    slot: 'content',
})(({ theme }) => ({
    position: 'relative',
    overflow: 'hidden',
    padding: '16px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    '&:before': {
        position: 'absolute',
        top: '50%',
        left: 0,
        display: 'block',
        content: '\'\'',
        height: '200%',
        aspectRatio: '1',
        transform: 'translate(-30%, -60%)',
        borderRadius: '50%',
        backgroundColor: theme.palette.secondary.main,
        opacity: 0.15,
    },
}));

const Icon = styled(Box, {
    name: 'ResourceTotal',
    slot: 'icon',
})(({ theme }) => ({
    color: theme.palette.secondary.main,
    width: '3em',
}));

const Text = styled(Box, {
    name: 'ResourceTotal',
    slot: 'text',
})(() => ({
    textAlign: 'right',
}));

const Title = styled(Typography, {
    name: 'ResourceTotal',
    slot: 'title',
})(({ theme }) => ({
    color: theme.palette.text.secondary,
}));

interface ResourceTotalCardProps {
    icon?: any;
    resource?: string;
    total?: number;
    isLoading?: boolean;
};

const ResourceTotalCard: FC<ResourceTotalCardProps> = ({
    icon,
    resource,
    total,
    isLoading,
}) => {
    const translate = useTranslate();
    const title = translate('label.total_resource', { resource: translate(`resources.${resource}.name`, { smart_count: 2 }) });

    return (
        <StyledCard>
            <Link
                to={`/${resource}`}
            >
                <Content>
                    <Icon>
                        { icon ? createElement(icon, { fontSize: 'large' }) : ''}
                    </Icon>
                    <Text>
                        <Title>{title}</Title>
                        {
                            isLoading ? (
                                <Skeleton
                                    variant='text'
                                    width={100}
                                    height={30}
                                />
                            ) : (
                                <Typography variant='h5' component='h2'>
                                    {total || ' '}
                                </Typography>
                            )
                        }
                    </Text>
                </Content>
            </Link>
        </StyledCard>
    );
};

export default ResourceTotalCard;
