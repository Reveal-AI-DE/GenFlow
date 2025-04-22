// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC, useState } from 'react';
import { styled } from '@mui/material/styles';
import CircularProgress from '@mui/material/CircularProgress';
import { useFormContext } from 'react-hook-form';
import { useNavigate } from 'react-router';
import {
    Button, useTranslate, useNotify,
} from 'react-admin';

import { authProvider } from '@/auth';

type RegistrationFormActionsProps = object;

const StyledButton = styled(Button, {
    name: 'GFRegistrationForm',
    slot: 'button',
})(({ theme }) => ({
    marginTop: theme.spacing(2),
}));

const StyledCircularProgress = styled(CircularProgress, {
    name: 'GFRegistrationForm',
    slot: 'loading',
})(({ theme }) => ({
    margin: theme.spacing(0.3),
}));

const RegistrationFormActions: FC<RegistrationFormActionsProps> = () => {
    const [loading, setLoading] = useState(false);
    const translate = useTranslate();
    const { handleSubmit, reset } = useFormContext();
    const notify = useNotify();
    const navigate = useNavigate();

    const onSubmit = async (data: any): Promise<void> => {
        setLoading(true);
        try {
            const resp = await authProvider.register(data);
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
        <StyledButton
            variant='contained'
            type='button'
            onClick={handleClick}
            disabled={loading}
            fullWidth
        >
            {
                loading ? (
                    <StyledCircularProgress
                        size={19}
                        thickness={3}
                    />
                ) : (
                    translate('action.sign_up')
                )
            }
        </StyledButton>
    );
};

export default RegistrationFormActions;
