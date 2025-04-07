// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React from 'react';
import { LoadingIndicator, LocalesMenuButton } from 'react-admin';

import { ThemeSwapper } from '@/themes';

export const AppBarToolbar = (): JSX.Element => (
    <>
        <LocalesMenuButton />
        <ThemeSwapper />
        <LoadingIndicator />
    </>
);
