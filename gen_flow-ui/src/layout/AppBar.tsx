// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React from 'react';
import { AppBar as RAAppBar, AppBarProps } from 'react-admin';

import { AppBarToolbar } from './AppBarToolbar';
import UserMenu from './UserMenu';

const AppBar = (props: AppBarProps): JSX.Element => (
    <RAAppBar {...props} toolbar={<AppBarToolbar />} userMenu={<UserMenu />} />
);

export default AppBar;
