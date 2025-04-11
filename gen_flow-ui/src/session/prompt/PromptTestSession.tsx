// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC, useEffect, useState } from 'react';
import {
    RecordContextProvider, ShowBase, CreateResult,
    useDataProvider, useRecordContext
} from 'react-admin';
import { matchPath, useLocation } from 'react-router';

import {
    Session, SessionType, SessionMode,
    Prompt, SessionFloatActionKey,
} from '@/types';
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

    const dataProvider = useDataProvider();
    const [testSession, setTestSession] = useState<Session | undefined>(undefined);

    const createTestSession = async (): Promise<CreateResult<Session>> => (
        dataProvider.create(
            'sessions',
            {
                data: {
                    name: `Testing - ${prompt.name}`,
                    session_type: SessionType.PROMPT,
                    session_mode: SessionMode.COMPLETION,
                    related_prompt: prompt.id,
                },
                meta: {
                    queryParams: {
                        testing: true,
                    },
                },
            })
    );

    useEffect(() => {
        if (!prompt.related_test_session) {
            createTestSession().then(({ data }) => {
                setTestSession(data);
            });
        } else {
            dataProvider.getOne('sessions', { id: prompt.related_test_session }).then((response) => {
                const { data: session } = response;
                if (session) {
                    setTestSession(session);
                }
            }).catch(() => {
                createTestSession().then(({ data }) => {
                    setTestSession(data);
                });
            });
        }
    }, []);

    if (!testSession) {
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
