// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import { Login as RaLogin, LoginProps} from 'react-admin';

import { PasswordResetConfirmForm as DefaultPasswordResetConfirmForm } from '@/auth/form';
import { LoginButton } from '@/auth/button';
import { LoginBackground } from '@/assets';
import { Footer } from '@/auth/Login';

type PasswordResetConfirmProps = LoginProps;

const PasswordResetConfirm: FC<PasswordResetConfirmProps> = (props) => {
    const { children = <DefaultPasswordResetConfirmForm /> } = props;
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
export default PasswordResetConfirm;
