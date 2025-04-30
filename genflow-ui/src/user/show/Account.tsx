// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';

import { UserCard } from '@/user/show';
import AccountActions from '@/user/form/AccountActions';

const Root = styled(Box, {
    name: 'GFAccount',
    slot: 'root',
})(({ theme }) => ({
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'flex-start',
    margin: theme.spacing(1),
    gap: theme.spacing(1),
}));

type AccountProps = object;

const Account: FC<AccountProps> = () => (
    <Root>
        <UserCard
            actions={(
                <AccountActions />
            )}
        />
    </Root>
);

export default Account;
