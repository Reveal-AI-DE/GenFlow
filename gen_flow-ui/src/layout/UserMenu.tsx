// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import {
    UserMenu as RAUserMenu,
    Logout,
    UserMenuProps,
} from 'react-admin';

import { AboutMenuItem, SettingsMenuItem } from '@/system';
import { TeamMenuItem } from '@/team';

const UserMenu: FC<UserMenuProps> = (props) => (
    <RAUserMenu
        {...props}
    >
        <TeamMenuItem />
        <SettingsMenuItem />
        <AboutMenuItem />
        <Logout />
    </RAUserMenu>
);

export default UserMenu;
