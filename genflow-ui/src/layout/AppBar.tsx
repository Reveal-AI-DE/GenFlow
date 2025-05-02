// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React from 'react';
import { AppBar as RAAppBar, AppBarProps } from 'react-admin';

import { AppBarToolbar } from '@/layout/AppBarToolbar';
import UserMenu from '@/layout/UserMenu';

const AppBar = (props: AppBarProps): JSX.Element => (
    <RAAppBar
        {...props}
        toolbar={<AppBarToolbar />}
        userMenu={<UserMenu />}
    />
);

export default AppBar;
