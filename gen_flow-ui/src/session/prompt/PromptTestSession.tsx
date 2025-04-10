// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import {
    RecordContextProvider, ShowBase,
    useGetOne, useRecordContext
} from 'react-admin';
import { matchPath, useLocation } from 'react-router';

import { Session, Prompt, SessionFloatActionKey } from '@/types';
import { SessionState} from '@/state';
import { ChatLayout } from '@/layout';
import { ChatBot } from '@/chat';

import TestSessionPlaceholder from '@/session/prompt/TestSessionPlaceholder';

type TestSessionProps = object;

const TestSession: FC<TestSessionProps> = () => {
    const prompt = useRecordContext<Prompt>();

    if (!prompt) {
        return (
            <ChatLayout responsive={false}>
                <TestSessionPlaceholder />
            </ChatLayout>
        );
    }

    const { data: testSession, isLoading, error } = useGetOne('sessions', { id: prompt.related_test_session });

    if (isLoading || error) {
        return (
            <ChatLayout responsive={false}>
                <TestSessionPlaceholder />
            </ChatLayout>
        );
    }

    return (
        <RecordContextProvider value={testSession as Session}>
            <SessionState
                useResponsiveLayout={false}
                actions={[
                    SessionFloatActionKey.INFO,
                    SessionFloatActionKey.USAGE,
                ]}
            >
                <ChatBot />
            </SessionState>
        </RecordContextProvider>
    )
};

interface PromptTestSessionProps {
    opened?: boolean;
};

const PromptTestSession: FC<PromptTestSessionProps> = ({
    opened,
}) => {
    const location = useLocation();
    const match = matchPath('/prompts/:id', location.pathname);

    if (!opened || !match || match.params.id === 'create') {
        return (
            <ChatLayout responsive={false}>
                <TestSessionPlaceholder />
            </ChatLayout>
        )
    }

    return (
        <ShowBase
            resource='prompts'
            id={match.params.id}
        >
            <TestSession />
        </ShowBase>
    );
}

export default PromptTestSession;
