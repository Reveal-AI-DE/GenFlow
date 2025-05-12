// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import { styled } from '@mui/material/styles';
import CardContent from '@mui/material/CardContent';
import {
    PasswordInput, required,
    Validator, Form,
} from 'react-admin';

import { PasswordResetConfirmFormData } from '@/types';
import {
    PasswordInputWithStrengthBar,
    validatePassword, matchPassword,
} from '@/common';
import PasswordResetConfirmActions from '@/auth/form/PasswordResetConfirmActions';

const PREFIX = 'PasswordResetConfirmForm';

export const PasswordResetConfirmFormClasses = {
    content: `${PREFIX}-content`,
    button: `${PREFIX}-button`,
    icon: `${PREFIX}-icon`,
    passwordStrength: `${PREFIX}-password-strength`,
};

const StyledForm = styled(Form<FormData>, {
    name: PREFIX,
    slot: 'root',
})(({ theme }) => ({
    [`& .${PasswordResetConfirmFormClasses.content}`]: {
        width: 400,
        paddingBottom: `${theme.spacing(2)}!important`,
    },
    [`& .${PasswordResetConfirmFormClasses.button}`]: {
        marginTop: theme.spacing(2),
    },
    [`& .${PasswordResetConfirmFormClasses.icon}`]: {
        margin: theme.spacing(0.3),
    },
    [`& .${PasswordResetConfirmFormClasses.passwordStrength}`]: {
        marginTop: theme.spacing(0),
        height: 10,
        borderRadius: 5,
    },
}));

type PasswordResetConfirmFormProps = object;

const PasswordResetConfirmForm: FC<PasswordResetConfirmFormProps> = () => {
    const validatePassword1: Validator = (value: string) => (
        validatePassword(value, '', '')
    );

    const equalToPassword: Validator = (value: string, allValues: PasswordResetConfirmFormData) => (
        matchPassword(value, allValues.new_password1)
    );
    return (
        <StyledForm>
            <CardContent className={PasswordResetConfirmFormClasses.content}>
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
                <PasswordResetConfirmActions />
            </CardContent>
        </StyledForm>
    );
};

export default PasswordResetConfirmForm;
