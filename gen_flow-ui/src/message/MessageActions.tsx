// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, {
    FC, useContext, useState, useEffect
} from 'react';
import Box from '@mui/material/Box';
import styled from '@mui/material/styles/styled';

import { SessionContext, SessionContextInterface } from '@/context';
import { ChatBotMessage } from '@/types';
import{ CopyButton } from '@/common';

interface OwnerStateProps {
    isAssistant: boolean;
    isLast: boolean;
};

const Root = styled(Box, {
    name: 'GFMessageActions',
    slot: 'Root',
})<{ ownerState: OwnerStateProps }>(({ theme, ownerState }) => ({
    display: 'flex',
    marginTop: theme.spacing(1),
    marginLeft: ownerState.isAssistant ? theme.spacing(2):0,
    marginBottom: ownerState.isLast ? theme.spacing(1):0,
    flexDirection: ownerState.isAssistant ? 'row':'row-reverse',
    '& > *:not(:first-child)': {
        marginLeft: ownerState.isAssistant ? theme.spacing(1):0,
        marginRight: ownerState.isAssistant ? 0:theme.spacing(1),
    },
    minHeight: 30,
}));

interface MessageActionsProps {
    message: ChatBotMessage,
    isLast: boolean;
    isHovering: boolean;
    isAssistant: boolean;
};

const MessageActions: FC<MessageActionsProps> = ({
    isLast,
    message,
    isHovering,
    isAssistant,
}) => {
    const { isGenerating } = useContext<SessionContextInterface>(SessionContext);
    const [showCheckmark, setShowCheckmark] = useState(false);

    useEffect(() => {
        if (showCheckmark) {
            const timer = setTimeout(() => {
                setShowCheckmark(false)
            }, 2000)

            return () => clearTimeout(timer)
        }
        return undefined;
    }, [showCheckmark]);

    return (isLast && isGenerating) ? null : (
        <Root ownerState={{ isAssistant, isLast }}>
            {
                (isHovering || isLast) && (
                    <CopyButton value={message.content} />
                )
            }
        </Root>
    )
};

export default MessageActions;
