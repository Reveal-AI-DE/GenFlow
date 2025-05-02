// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC, useState } from 'react';
import { useFormContext } from 'react-hook-form';
import { useNavigate } from 'react-router';
import {
    useTranslate, useNotify,
} from 'react-admin';

import { userRegister } from '@/user';
import { ButtonWithLoadingIndicator } from '@/common';

type RegistrationFormActionsProps = object;

const RegistrationFormActions: FC<RegistrationFormActionsProps> = () => {
    const [loading, setLoading] = useState(false);
    const translate = useTranslate();
    const { handleSubmit, reset } = useFormContext();
    const notify = useNotify();
    const navigate = useNavigate();

    const onSubmit = async (data: any): Promise<void> => {
        setLoading(true);
        try {
            const resp = await userRegister(data);
            reset();
            if (resp.email_verification_required) {
                navigate('/auth/verification-sent');
            } else {
                notify('message.register_success', { type: 'success' });
            }
        } catch (error) {
            console.error(error);
            notify('message.register_error', { type: 'warning' });
        } finally {
            setLoading(false);
        }
    }

    const handleClick = (event: React.MouseEvent<HTMLButtonElement>): void => {
        event.preventDefault();
        handleSubmit(onSubmit)();
    };

    return (
        <ButtonWithLoadingIndicator
            variant='contained'
            type='button'
            onClick={handleClick}
            loading={loading}
            fullWidth
        >
            {translate('action.sign_up')}
        </ButtonWithLoadingIndicator>
    );
};

export default RegistrationFormActions;
