// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import Box from '@mui/material/Box';
import { styled } from '@mui/material/styles';
import { Title, useTranslate } from 'react-admin';

import { SessionCreate } from '@/session';
import { ChatLayout } from '@/layout';
import NewChatPlaceholder from '@/chat/form/new/NewChatPlaceholder';

const Content = styled(Box, {
    name: 'GFNewChat',
    slot: 'content',
})(() => ({
    height: '100%',
}));

type NewChatProps = object;

const NewChat: FC<NewChatProps> = () => {
    const translate = useTranslate();

    return (
        <ChatLayout>
            <Title title={translate('label.new')} />
            <Content>
                <SessionCreate />
                <NewChatPlaceholder />
            </Content>
        </ChatLayout>
    );
};

export default NewChat;
