// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import { styled } from '@mui/material/styles';
import CardContent from '@mui/material/CardContent';
import Stack from '@mui/material/Stack';
import {
    TextInput, PasswordInput, required, email,
    useDataProvider, Form, Validator,
} from 'react-admin';

import { RegistrationFormData } from '@/types';
import { PasswordInputWithStrengthBar, validatePassword, matchPassword } from '@/common';
import RegistrationFormActions from '@/auth/form/RegistrationFormActions';

const PREFIX = 'GFRegistrationForm';

export const RegistrationFormClasses = {
    content: `${PREFIX}-content`,
    button: `${PREFIX}-button`,
    icon: `${PREFIX}-icon`,
    passwordStrength: `${PREFIX}-password-strength`,
};

const StyledForm = styled(Form<FormData>, {
    name: PREFIX,
    slot: 'root',
})(({ theme }) => ({
    [`& .${RegistrationFormClasses.content}`]: {
        width: 400,
        paddingBottom: `${theme.spacing(2)}!important`,
    },
    [`& .${RegistrationFormClasses.button}`]: {
        marginTop: theme.spacing(2),
    },
    [`& .${RegistrationFormClasses.icon}`]: {
        margin: theme.spacing(0.3),
    },
    [`& .${RegistrationFormClasses.passwordStrength}`]: {
        marginTop: theme.spacing(0),
        height: 10,
        borderRadius: 5,
    },
}));

type RegistrationFormProps = object;

const RegistrationForm: FC<RegistrationFormProps> = () => {
    const dataProvider = useDataProvider();
    const checkUsernameAvailability: Validator = async (value: string) => {
        if (!value) {
            return 'ra.validation.required';
        }
        return dataProvider.check('users', { username: value })
            .then((result: boolean) => (result ? 'validation.not_available' : undefined))
    };

    const checkEmail: Validator = async (value: string) => {
        if (!value) {
            return 'ra.validation.required';
        }
        return dataProvider.check('users', { email: value })
            .then((result: boolean) => (result ? 'validation.not_available' : undefined))
    };

    const validatePassword1: Validator = (value: string, allValues: RegistrationFormData) => (
        validatePassword(value, allValues.username, allValues.email)
    );

    const equalToPassword: Validator = (value: string, allValues: RegistrationFormData) => (
        matchPassword(value, allValues.password1)
    );

    return (
        <StyledForm>
            <CardContent className={RegistrationFormClasses.content}>
                <Stack
                    spacing={2}
                    direction='row'
                >
                    <TextInput
                        source='first_name'
                        label='resources.users.fields.first_name'
                        variant='filled'
                    />
                    <TextInput
                        source='last_name'
                        label='resources.users.fields.last_name'
                        variant='filled'
                    />
                </Stack>
                <TextInput
                    source='username'
                    label='resources.users.fields.username'
                    variant='filled'
                    validate={[required(), checkUsernameAvailability]}
                />
                <TextInput
                    source='email'
                    label='resources.users.fields.email'
                    variant='filled'
                    validate={[required(), email(), checkEmail]}
                />
                <PasswordInputWithStrengthBar
                    source='password1'
                    label='resources.users.fields.password1'
                    variant='filled'
                    validate={[required(), validatePassword1]}
                />
                <PasswordInput
                    source='password2'
                    label='resources.users.fields.password2'
                    variant='filled'
                    validate={[required(), equalToPassword]}
                />
                <RegistrationFormActions />
            </CardContent>
        </StyledForm>
    );
};

export default RegistrationForm;
