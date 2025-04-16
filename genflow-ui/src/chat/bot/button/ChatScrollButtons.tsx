// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import Box from '@mui/material/Box';
import Fab from '@mui/material/Fab';
import ArrowUpwardIcon from '@mui/icons-material/ArrowUpward';
import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward';
import { styled } from '@mui/material/styles';
import { useTranslate } from 'react-admin';

import { WithTooltip } from '@/common';

const StyledBox = styled(Box, {
    name: 'GFChatBot',
    slot: 'ScrollRoot',
})(() => ({
    position: 'absolute',
    bottom: '10px',
    right: '10px',
    display: 'flex',
    flexDirection: 'column',
}));

const StyledFab = styled(Fab, {
    name: 'GFChatBot',
    slot: 'ScrollFab',
})(() => ({
    margin: '5px',
}));

interface ChatScrollButtonsProps {
    isAtTop: boolean
    isAtBottom: boolean
    isOverflowing: boolean
    scrollToTop: () => void
    scrollToBottom: () => void
};

const ChatScrollButtons: FC<ChatScrollButtonsProps> = ({
    isAtTop,
    isAtBottom,
    isOverflowing,
    scrollToTop,
    scrollToBottom,
}) => {
    const translate = useTranslate();

    return (
        <StyledBox>
            {
                !isAtTop && isOverflowing && (
                    <WithTooltip
                        title={translate('action.scroll_top')}
                        trigger={(
                            <StyledFab
                                onClick={scrollToTop}
                                size='small'
                                color='secondary'
                            >
                                <ArrowUpwardIcon />
                            </StyledFab>
                        )}
                        arrow
                    />
                )
            }
            {
                !isAtBottom && isOverflowing && (
                    <WithTooltip
                        title={translate('action.scroll_bottom')}
                        trigger={(
                            <StyledFab
                                onClick={scrollToBottom}
                                size='small'
                                color='secondary'
                            >
                                <ArrowDownwardIcon />
                            </StyledFab>
                        )}
                        arrow
                    />
                )
            }
        </StyledBox>
    );
};

export default ChatScrollButtons;
