// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import DashboardIcon from '@mui/icons-material/Dashboard';
import { useBasename, MenuItemLink, MenuItemLinkProps } from 'react-admin';

interface DashboardMenuItemProps extends Omit<MenuItemLinkProps, 'to'> {
    to?: string;
}

const DashboardMenuItem: FC<DashboardMenuItemProps> = (props) => {
    const basename = useBasename();
    const {
        leftIcon = <DashboardIcon />,
        to = `${basename}/`,
        primaryText = 'ra.page.dashboard',
        ...rest
    } = props;

    return (
        <MenuItemLink
            leftIcon={leftIcon}
            to={to}
            primaryText={primaryText}
            {...rest}
        />
    );
};

export default DashboardMenuItem;
