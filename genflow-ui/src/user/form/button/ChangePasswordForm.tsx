// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import {
    PasswordInput, required,
    Validator, useGetIdentity,
} from 'react-admin';

import { ChangePasswordFormData } from '@/types';
import {
    PasswordInputWithStrengthBar,
    validatePassword, matchPassword,
} from '@/common';

type ChangePasswordFormProps = object;

const ChangePasswordForm: FC<ChangePasswordFormProps> = () => {
    const { data: currentUser } = useGetIdentity();
    if (!currentUser) {
        return null;
    }

    const validatePassword1: Validator = (value: string) => (
        validatePassword(value, currentUser.username, currentUser.email)
    );

    const equalToPassword: Validator = (value: string, allValues: ChangePasswordFormData) => (
        matchPassword(value, allValues.new_password1)
    );

    return (
        <>
            <PasswordInput
                source='old_password'
                label='resources.users.fields.old_password'
                variant='outlined'
                validate={[required()]}
            />
            <PasswordInputWithStrengthBar
                source='new_password1'
                label='resources.users.fields.new_password1'
                variant='outlined'
                validate={[required(), validatePassword1]}
            />
            <PasswordInput
                source='new_password2'
                label='resources.users.fields.new_password2'
                variant='outlined'
                validate={[required(), equalToPassword]}
            />
        </>
    );
};

export default ChangePasswordForm;
