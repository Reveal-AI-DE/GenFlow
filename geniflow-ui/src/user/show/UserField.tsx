// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Avatar from '@mui/material/Avatar';
import { styled } from '@mui/material/styles';
import { useTranslate } from 'react-admin';

import { Identity } from '@/types';

const Root = styled(Box, {
    name: 'GFUserField',
    slot: 'root',
})(() => ({
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-start',
    flexGrow: 1,
}));

const StyledAvatar = styled(Avatar, {
    name: 'GFUserField',
    slot: 'avatar',
})(() => ({
    width: 24,
    height: 24,
    marginRight: '8px',
}));

const StyledContent = styled(Box, {
    name: 'GFUserField',
    slot: 'content',
})(() => ({
    display: 'flex',
    flexDirection: 'column',
}));

interface UserFieldProps {
    user: Identity;
}

const UserField: FC<UserFieldProps> = ({ user }) => {
    const translate = useTranslate()

    if (!user) {
        return null;
    }
    return (
        <Root>
            <StyledAvatar
                src={user.avatar ? user.avatar : undefined}
                alt={user.fullName || user.email}
            />
            <StyledContent>
                <Typography variant='subtitle2'>
                    {`${user.first_name} ${user.last_name} ${user?.id === user.id ? `(${translate('label.you')})`:''}`}
                </Typography>
                <Typography variant='body2'>
                    {user.email}
                </Typography>
            </StyledContent>
        </Root>
    );
};

export default UserField;
