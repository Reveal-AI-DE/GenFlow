// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import { styled } from '@mui/material/styles';
import CardContent from '@mui/material/CardContent';
import {
    required, email, useDataProvider,
    Validator, Form, TextInput,
} from 'react-admin';

import PasswordResetFormActions from '@/auth/form/PasswordResetFormActions';

const PREFIX = 'ResetPasswordForm';

export const ResetPasswordFormClasses = {
    content: `${PREFIX}-content`,
    button: `${PREFIX}-button`,
    icon: `${PREFIX}-icon`,
};

const StyledForm = styled(Form<FormData>, {
    name: PREFIX,
    slot: 'root',
})(({ theme }) => ({
    [`& .${ResetPasswordFormClasses.content}`]: {
        width: 400,
        paddingBottom: `${theme.spacing(2)}!important`,
    },
    [`& .${ResetPasswordFormClasses.button}`]: {
        marginTop: theme.spacing(2),
    },
    [`& .${ResetPasswordFormClasses.icon}`]: {
        margin: theme.spacing(0.3),
    },
}));

type PasswordResetFormProps = object;

const PasswordResetForm: FC<PasswordResetFormProps> = () => {
    const dataProvider = useDataProvider();
    const checkEmail: Validator = async (value: string) => {
        if (!value) {
            return 'ra.validation.required';
        }
        return dataProvider.check('users', { email: value })
            .then((result: boolean) => (result ? undefined : 'validation.not_available'))
    };
    return (
        <StyledForm>
            <CardContent className={ResetPasswordFormClasses.content}>
                <TextInput
                    source='email'
                    label='resources.users.fields.email'
                    variant='filled'
                    validate={[required(), email(), checkEmail]}
                />
                <PasswordResetFormActions />
            </CardContent>
        </StyledForm>
    );
};

export default PasswordResetForm;
