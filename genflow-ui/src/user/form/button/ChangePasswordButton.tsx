// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC, useState } from 'react';
import LockResetIcon from '@mui/icons-material/LockReset';
import { useFormContext, FieldValues } from 'react-hook-form';
import {
    useTranslate, useNotify,
    useLogout, HttpError,
} from 'react-admin';

import { ChangePasswordFormData } from '@/types';
import {
    ButtonWithDialog, CancelButton,
    ButtonWithLoadingIndicator,
} from '@/common';
import { changePassword } from '@/user/userDataProvider';
import ChangePasswordForm from '@/user/form/button/ChangePasswordForm';

interface ChangePasswordDialogActionsProps {
    onClose: () => void;
};

const ChangePasswordDialogActions: FC<ChangePasswordDialogActionsProps> = ({
    onClose,
}) => {
    const [loading, setLoading] = useState(false);
    const { handleSubmit, reset, setError } = useFormContext();
    const translate = useTranslate();
    const notify = useNotify();
    const logout = useLogout();

    const onSubmit = async (data: FieldValues): Promise<void> => {
        setLoading(true);
        try {
            await changePassword(data as ChangePasswordFormData);
            reset();
            onClose();
            notify('message.change_password_success', { type: 'success' });
            logout();
        } catch (error) {
            const { message, body } = error as HttpError;
            // Notify the general error message
            notify(message, { type: 'error' });
            // Set field-specific errors if they exist in the JSON response
            if (body) {
                Object.entries(body).forEach(([field, errors]) => {
                    if (Array.isArray(errors)) {
                        setError(field, {
                            type: 'manual',
                            message: errors.join(', '),
                        });
                    }
                });
            }
        } finally {
            setLoading(false);
        }
    };

    const handleClick = (event: React.MouseEvent<HTMLButtonElement>): void => {
        event.preventDefault();
        handleSubmit(onSubmit)();
    };

    return (
        <>
            <CancelButton
                onClick={() => {
                    reset();
                    onClose();
                }}
            />
            <ButtonWithLoadingIndicator
                type='button'
                onClick={handleClick}
                loading={loading}
                icon={<LockResetIcon />}
            >
                {translate('action.change_password')}
            </ButtonWithLoadingIndicator>
        </>
    )
};

type ChangePasswordButtonProps = object;

const ChangePasswordButton: FC<ChangePasswordButtonProps> = () => {
    const translate = useTranslate();

    return (
        <ButtonWithDialog
            label='action.change_password'
            startIcon={<LockResetIcon />}
            dialog={{
                title: translate('action.change_password'),
                maxWidth: 'sm',
                fullWidth: true,
                disableBackdropClick: true,
                dialogContent: (
                    <ChangePasswordForm />
                ),
                dialogAction: (onClose) => (
                    <ChangePasswordDialogActions
                        onClose={() => onClose && onClose({}, 'escapeKeyDown')}
                    />
                )
            }}
        />
    );
};
export default ChangePasswordButton;
