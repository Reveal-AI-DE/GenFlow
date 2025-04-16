// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC, useState, useContext } from 'react';
import Paper from '@mui/material/Paper';
import Box from '@mui/material/Box';
import Skeleton from '@mui/material/Skeleton';
import Avatar from '@mui/material/Avatar';
import PersonIcon from '@mui/icons-material/Person';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import Tooltip from '@mui/material/Tooltip';
import { styled } from '@mui/material/styles';

import { ChatBotMessage } from '@/types';
import { SessionContext } from '@/context';
import MessageMarkdown from '@/message/MessageMarkdown';
import MessageActions from '@/message/MessageActions';

interface OwnerStateProps {
    isAssistant: boolean;
    isLast: boolean;
    isResponsiveLayout?: boolean;
};

const MessageContainer = styled(Box, {
    name: 'GFMessage',
    slot: 'MessageContainer',
})<{ ownerState: OwnerStateProps }>(({ theme, ownerState }) => ({
    display: 'flex',
    flexDirection: ownerState.isAssistant ? 'row':'row-reverse',
    alignItems: 'flex-start',
    width: '70%',
    [theme.breakpoints.up('md')]: {
        width: ownerState.isResponsiveLayout ? '700px' : '70%',
    },
    [theme.breakpoints.up('lg')]: {
        width: ownerState.isResponsiveLayout ? '900px' : '70%',
    },
    [theme.breakpoints.up('xl')]: {
        width: ownerState.isResponsiveLayout ? '1100px' : '70%',
    }
}));

const MessageContent = styled(Box, {
    name: 'GFMessage',
    slot: 'MessageContent',
})<{ ownerState: OwnerStateProps }>(({ ownerState }) => ({
    margin: '0 10px',
    display: 'flex',
    flexDirection: 'column',
    alignItems: ownerState.isAssistant ? 'flex-start':'flex-end',
    width: '100%'
}));

const ContentContainer = styled(Paper, {
    name: 'GFMessage',
    slot: 'ContentContainer',
})<{ ownerState: OwnerStateProps }>(({ theme, ownerState }) => ({
    padding: `${theme.spacing(1)} ${theme.spacing(3)}`,
    backgroundColor: ownerState.isAssistant ? 'transparent':theme.palette.background.default,
    maxWidth: ownerState.isAssistant ? '100%':'70%',
}));

interface MessageProps {
    message: ChatBotMessage,
    isLast: boolean,
};

const Message: FC<MessageProps> = ({
    message,
    isLast,
}) => {
    const [isHovering, setIsHovering] = useState<boolean>(false);

    const {
        isResponsiveLayout,
    } = useContext(SessionContext);

    const isAssistant = message.role === 'assistant';

    return (
        <MessageContainer
            ownerState={{ isAssistant, isLast, isResponsiveLayout }}
            onMouseEnter={() => setIsHovering(true)}
            onMouseLeave={() => setIsHovering(false)}
        >
            <Avatar
                alt={message.role === 'user' ? message.owner : 'Assistant'}
            >
                {
                    message.role === 'user' ? (
                        <Tooltip title={message.owner}>
                            <PersonIcon />
                        </Tooltip>
                    ) : (
                        <Tooltip title='Assistant'>
                            <SmartToyIcon />
                        </Tooltip>
                    )
                }
            </Avatar>
            <MessageContent ownerState={{ isAssistant, isLast }}>
                <ContentContainer
                    elevation={0}
                    ownerState={{ isAssistant, isLast }}
                >
                    <MessageMarkdown content={message.content} />
                </ContentContainer>
                <MessageActions
                    message={message}
                    isLast={isLast}
                    isHovering={isHovering}
                    isAssistant={isAssistant}
                />
            </MessageContent>
        </MessageContainer>
    )
};

export const MessageSkeleton: FC<OwnerStateProps> = ({ isAssistant, isLast }) => (
    <MessageContainer ownerState={{ isAssistant, isLast }}>
        <Skeleton variant='circular' width={40} height={40} />
        <MessageContent ownerState={{ isAssistant, isLast }}>
            <ContentContainer
                elevation={0}
                ownerState={{ isAssistant, isLast }}
                sx={{ backgroundColor: 'transparent' }}
            >
                <Skeleton variant='rectangular' width='400px' height='50px' animation='wave' />
            </ContentContainer>
        </MessageContent>
    </MessageContainer>
);

export default Message;
