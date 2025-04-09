// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import MenuList from '@mui/material/MenuList';
import { styled } from '@mui/material/styles';
import lodashGet from 'lodash/get';
import clsx from 'clsx';
import {
    MenuProps, useSidebarState, MenuClasses, ResourceMenuItems,
    DRAWER_WIDTH, CLOSED_DRAWER_WIDTH,
} from 'react-admin';

import { ChatMenuItem } from '@/chat';

const PREFIX = 'RaMenu';

const Root = styled(MenuList, {
    name: PREFIX,
    overridesResolver: (props, styles) => styles.root,
})(({ theme }) => ({
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'flex-start',
    [theme.breakpoints.only('xs')]: {
        marginTop: 0,
    },
    transition: theme.transitions.create('width', {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.leavingScreen,
    }),

    [`&.${MenuClasses.open}`]: {
        width: lodashGet(theme, 'sidebar.width', DRAWER_WIDTH),
    },

    [`&.${MenuClasses.closed}`]: {
        width: lodashGet(theme, 'sidebar.closedWidth', CLOSED_DRAWER_WIDTH),
    },
}));

const Menu: FC<MenuProps> = (props: MenuProps) => {
    const { children, className, ...rest } = props;
    const [open] = useSidebarState();

    return (
        <Root
            className={clsx(
                {
                    [MenuClasses.open]: open,
                    [MenuClasses.closed]: !open,
                }
            )}
            {...rest}
        >
            <ChatMenuItem />
            <ResourceMenuItems />
        </Root>
    );
};

export default Menu;
