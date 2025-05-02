// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import { Login as RaLogin, LoginProps} from 'react-admin';

import { PasswordResetForm as DefaultPasswordResetForm } from '@/auth/form';
import { LoginButton } from '@/auth/button';
import { LoginBackground } from '@/assets';
import { Footer } from '@/auth/Login';

type PasswordResetProps = LoginProps;

const PasswordReset: FC<PasswordResetProps> = (props) => {
    const { children = <DefaultPasswordResetForm /> } = props;
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

export default PasswordReset;
