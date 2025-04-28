// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import { Login, useTranslate } from 'react-admin';

import { LoginBackground } from '@/assets';
import { LoginButton } from '@/auth/button';
import { Footer } from '@/auth/Login';

export const Content = styled(Box, {
    name: 'GFLogin',
    slot: 'content',
})(({ theme }) => ({
    margin: theme.spacing(2),
    maxWidth: 400,
}));

export const Text = styled(Typography, {
    name: 'GFLogin',
    slot: 'text',
})(({ theme }) => ({
    marginBottom: theme.spacing(2),
}));

type ConfirmedProps = object;

const Confirmed: FC<ConfirmedProps> = (props) => {
    const translate = useTranslate();

    return (
        <Login
            {...props}
            backgroundImage={LoginBackground}
        >
            <Content>
                <Text
                    variant='h5'
                >
                    {translate('message.confirmed')}
                </Text>
                <Text
                    variant='body1'
                >
                    {translate('message.email_confirmed')}
                </Text>
            </Content>
            <Footer>
                <LoginButton />
            </Footer>
        </Login>
    );
};

export default Confirmed;
