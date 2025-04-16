// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import { Title, ShowBase, WithRecord } from 'react-admin';

import { SessionState } from '@/state';
import { ChatBot } from '@/chat';
import { SessionName } from '@/session/form';

type SessionShowProps = object;

const SessionShow: FC<SessionShowProps> = () => (
    <ShowBase>
        <>
            <WithRecord
                render={() => (
                    <Title title={<SessionName />} />
                )}
            />
            <SessionState>
                <ChatBot />
            </SessionState>
        </>
    </ShowBase>
);

export default SessionShow;
