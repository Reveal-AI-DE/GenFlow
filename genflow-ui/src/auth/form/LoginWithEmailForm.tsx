// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import {
    PasswordInput, TextInput, required,
    useTranslate, LoginForm, email,
} from 'react-admin';

type LoginWithEmailFormProps = object;

const LoginWithEmailForm: FC<LoginWithEmailFormProps> = () => {
    const translate = useTranslate();
    return (
        <LoginForm>
            <TextInput
                autoFocus
                source='email'
                label={translate('ra.auth.email', { _: 'Email' })}
                autoComplete='email'
                type='email'
                validate={[required(), email()]}
            />
            <PasswordInput
                source='password'
                label={translate('ra.auth.password', { _: 'Password' })}
                autoComplete='current-password'
                validate={required()}
            />
        </LoginForm>
    );
};

export default LoginWithEmailForm;
