// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC, useState, useEffect } from 'react';
import { useFormContext } from 'react-hook-form';
import { useNavigate, useLocation } from 'react-router';
import {
    useTranslate, useNotify,
} from 'react-admin';

import { passwordResetConfirm } from '@/user';
import { ButtonWithLoadingIndicator } from '@/common';

type PasswordResetConfirmActionsProps = object;

const PasswordResetConfirmActions: FC<PasswordResetConfirmActionsProps> = () => {
    const [loading, setLoading] = useState(false);
    const translate = useTranslate();
    const { handleSubmit, reset } = useFormContext();
    const notify = useNotify();
    const navigate = useNavigate();
    const location = useLocation();

    // Extract uid and token from the URL
    const searchParams = new URLSearchParams(location.search);
    const uid = searchParams.get('uid');
    const token = searchParams.get('token');

    // Check for uid and token on first render
    useEffect(() => {
        if (!uid || !token) {
            notify('message.incorrect_reset_link', { type: 'error' });
            navigate('/login');
        }
    }, [uid, token, notify, navigate]);

    const onSubmit = async (data: any): Promise<void> => {
        setLoading(true);
        try {
            const payload = { ...data, uid, token };
            await passwordResetConfirm(payload);
            reset();
            notify('message.password_reset_success', { type: 'success' });
            navigate('/login');
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
            {translate('action.password_reset')}
        </ButtonWithLoadingIndicator>
    );
};

export default PasswordResetConfirmActions;
