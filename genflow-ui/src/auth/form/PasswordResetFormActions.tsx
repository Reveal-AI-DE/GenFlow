// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC, useState } from 'react';
import { useFormContext } from 'react-hook-form';
import {
    useTranslate, useNotify,
} from 'react-admin';

import { passwordReset } from '@/user';
import { ButtonWithLoadingIndicator } from '@/common';

type PasswordResetActionsProps = object;

const PasswordResetActions: FC<PasswordResetActionsProps> = () => {
    const [loading, setLoading] = useState(false);
    const translate = useTranslate();
    const { handleSubmit, reset } = useFormContext();
    const notify = useNotify();

    const onSubmit = async (data: any): Promise<void> => {
        setLoading(true);
        try {
            await passwordReset(data);
            reset();
            notify('message.check_email', { type: 'success' });
        } catch (error) {
            console.error(error);
            notify('ra.notification.http_error', { type: 'warning' });
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
            {translate('action.password_reset_request')}
        </ButtonWithLoadingIndicator>
    );
};

export default PasswordResetActions;
