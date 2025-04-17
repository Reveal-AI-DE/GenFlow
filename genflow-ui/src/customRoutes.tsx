// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import React from 'react';
import { Route } from 'react-router';
import { Authenticated } from 'react-admin';

import { Signup } from '@/auth';
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
];

export { layoutCustomRoutes, noLayoutCustomRoutes };
