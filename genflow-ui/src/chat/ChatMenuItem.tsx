// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import ChatIcon from '@mui/icons-material/Chat';
import { useBasename, MenuItemLink, MenuItemLinkProps } from 'react-admin';

interface ChatMenuItemProps extends Omit<MenuItemLinkProps, 'to'> {
    to?: string;
}

const ChatMenuItem: FC<ChatMenuItemProps> = (props) => {
    const basename = useBasename();
    const {
        leftIcon = <ChatIcon />,
        to = `${basename}/new`,
        primaryText = 'label.chat.title',
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

export default ChatMenuItem;
