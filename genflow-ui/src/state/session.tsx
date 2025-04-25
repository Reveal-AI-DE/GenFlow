// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, {
    useState, FC, ReactNode, useEffect,
} from 'react';
import { BatchItem } from '@rpldy/uploady';
import { useRecordContext, useDataProvider } from 'react-admin';

import {
    Session, SessionMessage, FileEntity,SessionFloatActionKey,
    SessionType, ChatSetting, Parameters, ConfigurationEntity,
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

    const dataProvider = useDataProvider();

    const [generateURL, setGenerateURL] = useState<string | undefined>(undefined);

    const [userInput, setUserInput] = useState<string>('');
    const [attachedFile, setAttachedFile] = useState<BatchItem | undefined>(undefined);
    const [userFiles, setUserFiles] = useState<FileEntity[]>([]);
    const [chatSetting, setChatSetting] = useState<ChatSetting>({});
    const [sessionMessages, setSessionMessages] = useState<SessionMessage[] | []>([]);

    const [isLoadingInitialData, setIsLoadingInitialData] = useState<boolean>(true);
    const [isGenerating, setIsGenerating] = useState<boolean>(false);

    const [isResponsiveLayout, setIsResponsiveLayout] = useState<boolean>(true);
    const [floatActions, setFloatActions] = useState<SessionFloatActionKey[]>(actions || []);
    const [promptSelection, setPromptSelection] = useState<boolean>(false);

    useEffect(() => {
        if (session) {
            setGenerateURL(createGenerateURL(session));
        }
    }, [session]);

    if (!session) return null;

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
    };

    const initializeChatSetting = async (): Promise<void> => {
        if (!session.related_model || !session.related_model.entity.parameter_configs) return;
        // initialize chat setting
        setChatSetting({
            ...chatSetting,
            parameters: session.related_model.entity.parameter_configs.reduce(
                (parameters: Parameters, config: ConfigurationEntity) => {
                    if (!Object.keys(parameters).includes(config.name)) {
                        parameters[config.name] = config.default;
                    }
                    return parameters;
                }, {})
        });
    };

    const fetchInitialData = async (): Promise<void> => {
        switch(session.session_type) {
            case SessionType.LLM:
                setFloatActions([
                    SessionFloatActionKey.SETTINGS,
                    SessionFloatActionKey.INFO,
                    SessionFloatActionKey.USAGE,
                    SessionFloatActionKey.NEW,
                ]);
                break;
            case SessionType.PROMPT:
                setFloatActions([
                    SessionFloatActionKey.INFO,
                    SessionFloatActionKey.USAGE,
                    SessionFloatActionKey.NEW,
                ]);
                break;
            case SessionType.ASSISTANT:
                setFloatActions([
                    SessionFloatActionKey.INFO,
                    SessionFloatActionKey.USAGE,
                    SessionFloatActionKey.NEW,
                ]);
                break;
            default:
                break;
        }
        // initialize chat setting
        await initializeChatSetting();
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
        chatSetting,
        setChatSetting,
        sessionMessages,
        setSessionMessages,

        isLoadingInitialData,
        isGenerating,
        setIsGenerating,

        isResponsiveLayout,
        floatActions,
        promptSelection,
        setPromptSelection,
    }), [
        isLoadingInitialData,
        userInput,
        chatSetting,
        sessionMessages,
        isGenerating,
        attachedFile,
        promptSelection,
    ]);

    return (
        <SessionContext.Provider value={contextValue}>
            {children}
        </SessionContext.Provider>
    );
};
