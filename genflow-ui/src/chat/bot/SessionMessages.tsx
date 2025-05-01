// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC, Fragment, useContext } from 'react';

import { SessionContext, SessionContextInterface } from '@/context';
import { Message, MessageSkeleton } from '@/message';

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
                {
                    sessionMessage.answer ? (
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
                    ) : (
                        <MessageSkeleton isAssistant isLast />
                    )
                }
            </Fragment>
        ));
};

export default SessionMessages;
