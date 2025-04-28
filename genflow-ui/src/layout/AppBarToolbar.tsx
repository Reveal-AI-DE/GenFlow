// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

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
