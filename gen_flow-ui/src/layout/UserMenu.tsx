// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import {
    UserMenu as RAUserMenu,
    Logout,
    UserMenuProps,
} from 'react-admin';

const UserMenu: FC<UserMenuProps> = (props) => (
    <RAUserMenu {...props}>
        <Logout />
    </RAUserMenu>
);

export default UserMenu;
