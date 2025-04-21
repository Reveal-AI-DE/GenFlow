// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import { Login, useTranslate } from 'react-admin';

import { LoginBackground } from '@/assets';
import { LoginButton } from '@/auth/button';
import { Footer } from '@/auth/Login';
import { Content, Text } from '@/auth/email/Confirmed';

type VerificationSentProps = object;

const VerificationSent: FC<VerificationSentProps> = (props) => {
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
                    {translate('message.verification_sent')}
                </Text>
                <Text
                    variant='body1'
                >
                    {translate('message.verification_email_sent')}
                </Text>
            </Content>
            <Footer>
                <LoginButton />
            </Footer>
        </Login>
    );
};

export default VerificationSent;
