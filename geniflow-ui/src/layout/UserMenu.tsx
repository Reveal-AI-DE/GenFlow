// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

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
