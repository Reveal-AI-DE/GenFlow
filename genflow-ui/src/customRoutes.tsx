// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React from 'react';
import { Route } from 'react-router';
import { Authenticated } from 'react-admin';

import { PasswordReset, PasswordResetConfirm, Signup } from '@/auth';
import { Confirmed, IncorrectConfirmation, VerificationSent } from '@/auth/email';
import { NewChat } from '@/chat';

const layoutCustomRoutes = [
    <Route
        key='new-chat'
        path='/new'
        element={(
            <Authenticated>
                <NewChat />
            </Authenticated>
        )}
    />,
];

const noLayoutCustomRoutes = [
    <Route
        key='signup'
        path='/signup'
        element={(
            <Signup />
        )}
    />,
    <Route
        key='password-reset'
        path='/auth/password-reset'
        element={(
            <PasswordReset />
        )}
    />,
    <Route
        key='password-reset-confirm'
        path='/auth/password-reset-confirm'
        element={(
            <PasswordResetConfirm />
        )}
    />,
    <Route
        key='email-confirmed'
        path='/auth/email-confirmed'
        element={(
            <Confirmed />
        )}
    />,
    <Route
        key='email-not-confirmed'
        path='/auth/email-not-confirmed'
        element={(
            <IncorrectConfirmation />
        )}
    />,
    <Route
        key='verification-sent'
        path='/auth/verification-sent'
        element={(
            <VerificationSent />
        )}
    />,
];

export { layoutCustomRoutes, noLayoutCustomRoutes };
