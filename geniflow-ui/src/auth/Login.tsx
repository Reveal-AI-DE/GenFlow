// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC, useState, useCallback } from 'react';
import Box from '@mui/material/Box';
import { styled } from '@mui/material/styles';
import Divider from '@mui/material/Divider';
import {
    Login as RaLogin, LoginProps, LoginForm
} from 'react-admin';
import { GoogleOAuthProvider } from '@react-oauth/google';

import { LoginWithEmailForm } from '@/auth/form';
import {
    GoogleLoginButton, PasswordResetButton, SignupButton , LoginMethodSwitchButton,
} from '@/auth/button';
import { LoginBackground } from '@/assets';

const Toolbar = styled(Box,{
    name: 'GFLogin',
    slot: 'toolbar',
})(({ theme }) => ({
    display: 'flex',
    alignItems: 'center',
    margin: theme.spacing(1, 2),
}));

export const Footer = styled(Box,{
    name: 'GFLogin',
    slot: 'toolbar',
})(({ theme }) => ({
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    margin: theme.spacing(1, 2),
}));

const Login: FC<LoginProps> = (props) => {
    const [loginWithEmail, setLoginWithEmail] = useState<boolean>(false);

    const renderLoginMethodSwitchButton = (): JSX.Element => (loginWithEmail ? (
        <LoginMethodSwitchButton
            onClick={() => setLoginWithEmail(false)}
            loginMethod='username'
        />
    ) : (
        <LoginMethodSwitchButton
            onClick={() => setLoginWithEmail(true)}
            loginMethod='email'
        />
    ));

    const renderGoogleLoginButton = useCallback((): JSX.Element | null => (process.env.REACT_APP_GOOGLE_CLIENT_ID ? (
        <GoogleOAuthProvider
            clientId={process.env.REACT_APP_GOOGLE_CLIENT_ID}
        >
            <GoogleLoginButton />
        </GoogleOAuthProvider>
    ):null), []);

    const renderLoginForm = useCallback((): JSX.Element => (
        <>
            <Toolbar>
                {renderLoginMethodSwitchButton()}
                {renderGoogleLoginButton()}
            </Toolbar>
            {
                loginWithEmail ? (
                    <LoginWithEmailForm />
                ) : (
                    <LoginForm />
                )
            }
        </>
    ), [loginWithEmail]);

    return (
        <RaLogin
            {...props}
            backgroundImage={LoginBackground}
        >
            {renderLoginForm()}
            <Footer>
                <SignupButton />
                <Divider />
                <PasswordResetButton />
            </Footer>
        </RaLogin>
    );
};

export default Login;
