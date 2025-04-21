// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC, Fragment, useContext } from 'react';

import { SessionContext, SessionContextInterface } from '@/context';
import { Message } from '@/message';

type SessionMessagesProps = object;

const SessionMessages: FC<SessionMessagesProps> = () => {
    const { sessionMessages } = useContext<SessionContextInterface>(SessionContext);

    return sessionMessages
        .sort((a, b) => a.sequence - b.sequence)
        .map((sessionMessage, index, array) => (
            <Fragment key={index}>
                <Message
                    key={`${index}-user`}
                    isLast={false}
                    message={{
                        id: sessionMessage.id,
                        content: sessionMessage.query,
                        role: 'user',
                        owner: sessionMessage.owner,
                    }}
                />
                <Message
                    key={`${index}-bot`}
                    isLast={index === array.length - 1}
                    message={{
                        id: sessionMessage.id,
                        content: sessionMessage.answer,
                        role: 'assistant',
                        references: sessionMessage.references,
                    }}
                />
            </Fragment>
        ));
};

export default SessionMessages;
