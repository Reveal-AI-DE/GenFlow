// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, {
    useState, FC, ReactNode, useEffect,
} from 'react';
import { BatchItem } from '@rpldy/uploady';
import { useRecordContext, useDataProvider } from 'react-admin';

import {
    Session, SessionMessage, FileEntity, SessionFloatActionKey,
    SessionType,
} from '@/types';
import { SessionContext } from '@/context';
import { createGenerateURL } from '@/utils';

interface SessionStateProps {
    children: ReactNode,
    useResponsiveLayout?: boolean,
    actions?: SessionFloatActionKey[],
};

export const SessionState: FC<SessionStateProps> = ({
    children,
    useResponsiveLayout,
    actions,
}) => {
    const session = useRecordContext<Session>();
    if (!session) return null;

    const dataProvider = useDataProvider();

    const [generateURL] = useState<string>(createGenerateURL(session));

    const [userInput, setUserInput] = useState<string>('');
    const [attachedFile, setAttachedFile] = useState<BatchItem | undefined>(undefined);
    const [userFiles, setUserFiles] = useState<FileEntity[]>([]);
    const [sessionMessages, setSessionMessages] = useState<SessionMessage[] | []>([]);

    const [isLoadingInitialData, setIsLoadingInitialData] = useState<boolean>(true);
    const [isGenerating, setIsGenerating] = useState<boolean>(false);

    const [isResponsiveLayout, setIsResponsiveLayout] = useState<boolean>(true);
    const [floatActions, setFloatActions] = useState<SessionFloatActionKey[]>(actions || []);

    const fetchSessionMessages = async (): Promise<void> => {
        // get stored messages
        dataProvider.getList('messages', {
            filter: {session: session.id},
            pagination: { page: 1, perPage: -1 }
        }).then((messageData: any) => {
            const { data: messages } = messageData;
            setSessionMessages(messages);
            if (useResponsiveLayout !== undefined) setIsResponsiveLayout(useResponsiveLayout);
        });
    }

    const fetchInitialData = async (): Promise<void> => {
        switch(session.type) {
            case SessionType.LLM:
                setFloatActions([
                    SessionFloatActionKey.SETTINGS,
                    SessionFloatActionKey.INFO,
                    SessionFloatActionKey.USAGE,
                    SessionFloatActionKey.NEW,
                ]);
                break;
            default:
                break;
        }
        // get stored messages
        await fetchSessionMessages();
    };

    useEffect(() => {
        (async () => {
            await fetchInitialData().then(() => setIsLoadingInitialData(false));
        })();
    }, []);

    const contextValue = React.useMemo(() => ({
        generateURL,

        userInput,
        setUserInput,
        attachedFile,
        setAttachedFile,
        userFiles,
        setUserFiles,

        sessionMessages,
        setSessionMessages,

        isLoadingInitialData,
        isGenerating,
        setIsGenerating,

        isResponsiveLayout,
        floatActions,
    }), [
        isLoadingInitialData,
        userInput,
        sessionMessages,
        isGenerating,
        attachedFile,
    ]);

    return (
        <SessionContext.Provider value={contextValue}>
            {children}
        </SessionContext.Provider>
    );
};
