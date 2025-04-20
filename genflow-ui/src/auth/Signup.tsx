// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
import { Login as RaLogin, LoginProps} from 'react-admin';

import { RegistrationForm as DefaultRegistrationForm } from '@/auth/form';
import { LoginButton } from '@/auth/button';
import { LoginBackground } from '@/assets';

const Footer = styled(Box,{
    name: 'GFSignup',
    slot: 'toolbar',
})(({ theme }) => ({
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    margin: theme.spacing(1, 2),
}));

type SignupProps = LoginProps;

const Signup: FC<SignupProps> = (props) => {
    const { children = <DefaultRegistrationForm /> } = props;
    return (
        <RaLogin
            {...props}
            backgroundImage={LoginBackground}
        >
            {children}
            <Footer>
                <LoginButton />
            </Footer>
        </RaLogin>
    );
};
export default Signup;
