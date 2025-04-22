// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, {
    FC, useContext, useEffect,
} from 'react';
import Box from '@mui/material/Box';
import Divider from '@mui/material/Divider';
import { styled } from '@mui/material/styles';
import { useRecordContext } from 'react-admin';

import { SessionType, Session } from '@/types';
import { SessionContext, SessionContextInterface } from '@/context';
import { useScroll } from '@/hook';
import { ChatLayout } from '@/layout';
import { MessageSkeleton } from '@/message';
import { ChatScrollButtons, ChatActions} from '@/chat/bot/button';
import SessionMessages from '@/chat/bot/SessionMessages';
import ChatBotPlaceholder from '@/chat/bot/ChatBotPlaceholder';
import { PromptStartingMessage } from '@/prompt';

const Root = styled(Box, {
    name: 'GFChatBot',
    slot: 'root',
})(() => ({
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    height: '100%',
    width: '100%',
    overflow: 'auto',
    marginTop: '10px',
}));

type ChatBotProps = object;

const ChatBot: FC<ChatBotProps> = () => {
    const session = useRecordContext<Session>();

    if (!session) return null;

    const renderPlaceholder = (): JSX.Element | null => {
        switch(session.session_type) {
            case SessionType.LLM:
                return (
                    <ChatBotPlaceholder />
                )
            case SessionType.PROMPT:
                return (
                    <PromptStartingMessage />
                )
            default:
                return null;
        }
    };

    const {
        isLoadingInitialData,
        sessionMessages,
        isResponsiveLayout,
    } = useContext<SessionContextInterface>(SessionContext);
    const {
        messagesStartRef,
        messagesEndRef,
        handleScroll,
        isAtTop,
        isAtBottom,
        isOverflowing,
        scrollToTop,
        scrollToBottom,
        setIsAtBottom,
    } = useScroll();

    useEffect(() => {
        scrollToBottom()
        setIsAtBottom(true)
    }, [sessionMessages]);

    return (
        <ChatLayout responsive={isResponsiveLayout}>
            <Root onScroll={handleScroll}>
                <Box ref={messagesStartRef} />
                {
                    isLoadingInitialData && (
                        <>
                            <MessageSkeleton isAssistant={false} isLast={false} />
                            <MessageSkeleton isAssistant isLast={false} />
                            <MessageSkeleton isAssistant={false} isLast={false} />
                            <MessageSkeleton isAssistant isLast />
                        </>
                    )
                }
                {
                    !isLoadingInitialData && (sessionMessages.length === 0 ? (
                        renderPlaceholder()
                    ) : (
                        <>
                            {renderPlaceholder()}
                            <Divider
                                style={{
                                    width: '100%',
                                    marginBottom: '10px',
                                }}
                            />
                            <SessionMessages />
                        </>
                    ))
                }
                <Box ref={messagesEndRef} />
            </Root>
            {
                isLoadingInitialData ? (
                    null
                ) : (
                    <>
                        <ChatScrollButtons
                            isAtTop={isAtTop}
                            isAtBottom={isAtBottom}
                            isOverflowing={isOverflowing}
                            scrollToTop={scrollToTop}
                            scrollToBottom={scrollToBottom}
                        />
                        <ChatActions />
                    </>
                )
            }
        </ChatLayout>
    );
};

export default ChatBot;
