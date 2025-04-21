// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import { Login as RaLogin, LoginProps} from 'react-admin';

import { RegistrationForm as DefaultRegistrationForm } from '@/auth/form';
import { LoginButton } from '@/auth/button';
import { LoginBackground } from '@/assets';
import { Footer } from '@/auth/Login';

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
