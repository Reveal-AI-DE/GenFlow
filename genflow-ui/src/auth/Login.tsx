// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC, useState, useCallback } from 'react';
import IconButton from '@mui/material/IconButton';
import AlternateEmailIcon from '@mui/icons-material/AlternateEmail';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import Box from '@mui/material/Box';
import { styled } from '@mui/material/styles';
import {
    Login as RaLogin, LoginProps,
    LoginForm, useTranslate,
} from 'react-admin';
import { GoogleOAuthProvider } from '@react-oauth/google';

import { WithTooltip } from '@/common';
import { LoginWithEmailForm } from '@/auth/form';
import { GoogleLoginButton, SignupButton } from '@/auth/button';

const Toolbar = styled(Box,{
    name: 'GFLogin',
    slot: 'toolbar',
})(({ theme }) => ({
    display: 'flex',
    alignItems: 'center',
    margin: theme.spacing(1, 2),
}));

const Footer = styled(Box,{
    name: 'GFLogin',
    slot: 'toolbar',
})(({ theme }) => ({
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    margin: theme.spacing(1, 2),
}));

const Login: FC<LoginProps> = (props) => {
    const translate = useTranslate();
    const [withEmail, setWithEmail] = useState<boolean>(false);

    const renderLoginForm = useCallback((): JSX.Element => (withEmail ? (
        <LoginWithEmailForm />
    ) : (
        <LoginForm />
    )), [withEmail]);

    const renderSwitchButton = useCallback((): JSX.Element => (
        <WithTooltip
            title={withEmail ? translate('action.login_username'):translate('action.login_email')}
            trigger={(
                <span>
                    <IconButton
                        edge='start'
                        aria-label={withEmail ? translate('action.login_username'):translate('action.login_email')}
                        onClick={() => setWithEmail(!withEmail)}
                        size='small'
                        color='primary'
                    >
                        {
                            withEmail ? (
                                <AccountCircleIcon
                                    fontSize='medium'
                                />
                            ) : (
                                <AlternateEmailIcon
                                    fontSize='medium'
                                />
                            )
                        }
                    </IconButton>
                </span>
            )}
            arrow
        />
    ), [withEmail]);

    const renderGoogleLoginButton = useCallback((): JSX.Element | null => (process.env.REACT_APP_GOOGLE_CLIENT_ID ? (
        <GoogleOAuthProvider
            clientId={process.env.REACT_APP_GOOGLE_CLIENT_ID}
        >
            <GoogleLoginButton />
        </GoogleOAuthProvider>
    ):null), []);

    return (
        <RaLogin {...props}>
            <Toolbar>
                {renderSwitchButton()}
                {renderGoogleLoginButton()}
            </Toolbar>
            {renderLoginForm()}
            <Footer>
                <SignupButton />
            </Footer>
        </RaLogin>
    );
};

export default Login;
