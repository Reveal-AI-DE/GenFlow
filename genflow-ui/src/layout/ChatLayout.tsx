// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, {
    FC, ReactNode,
} from 'react';
import Paper from '@mui/material/Paper';
import Box from '@mui/material/Box';
import { styled } from '@mui/material/styles';

import { ChatInput } from '@/chat';

const RootContainer = styled(Paper, {
    name: 'GFChat',
    slot: 'root',
})(({ theme }) => ({
    flexDirection: 'column',
    display: 'flex',
    flexGrow: 1,
    marginRight: '-8px',
    alignItems: 'center',
    justifyContent: 'center',
    overflow: 'hidden',
    [theme.breakpoints.down('sm')]: {
        marginLeft: '-8px',
    },
    height: 'calc(100vh - 48px)'
}));

const ContentContainer = styled(Box, {
    name: 'GFChat',
    slot: 'content',
})(() => ({
    flexGrow: 1,
    width: '100%',
    position: 'relative',
    overflow: 'hidden',
}));

interface InputContainerProps {
    responsive: boolean;
};

const InputContainer = styled(Box, {
    name: 'GFChat',
    slot: 'input',
})<{ ownerState: InputContainerProps }>(({ theme, ownerState }) => ({
    padding: '20px 8px',
    width: '70%',
    [theme.breakpoints.up('md')]: {
        width: ownerState.responsive ? '700px' : '70%',
    },
    [theme.breakpoints.up('lg')]: {
        width: ownerState.responsive ? '900px' : '70%',
    },
    [theme.breakpoints.up('xl')]: {
        width: ownerState.responsive ? '1100px' : '70%',
    }
}));

interface ChatLayoutProps {
    children: ReactNode;
    responsive?: boolean;
}

const ChatLayout: FC<ChatLayoutProps> = ({
    children,
    responsive = true,
}) => (
    <RootContainer>
        <ContentContainer>
            {children}
        </ContentContainer>
        <InputContainer ownerState={{ responsive }}>
            <ChatInput />
        </InputContainer>
    </RootContainer>
);

export default ChatLayout;
