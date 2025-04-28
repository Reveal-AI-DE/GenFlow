// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import { Login, useTranslate } from 'react-admin';

import { LoginBackground } from '@/assets';
import { LoginButton } from '@/auth/button';
import { Footer } from '@/auth/Login';
import { Content, Text } from '@/auth/email/Confirmed';

type ConfirmedProps = object;

const IncorrectConfirmation: FC<ConfirmedProps> = (props) => {
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
                    {translate('message.not_confirmed')}
                </Text>
                <Text
                    variant='body1'
                >
                    {translate('message.email_not_confirmed')}
                </Text>
            </Content>
            <Footer>
                <LoginButton />
            </Footer>
        </Login>
    );
}

export default IncorrectConfirmation;
