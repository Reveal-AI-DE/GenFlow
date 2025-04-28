// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import { Dispatch, SetStateAction, createContext } from 'react';
import { BatchItem } from '@rpldy/uploady';

import {
    SessionMessage, FileEntity, SessionFloatActionKey, ChatSetting,
} from '@/types';

export interface SessionContextInterface {
    generateURL: string | undefined,

    userInput: string,
    setUserInput: Dispatch<SetStateAction<string>>,
    attachedFile: BatchItem | undefined,
    setAttachedFile: Dispatch<SetStateAction<BatchItem | undefined>>,
    userFiles: FileEntity[],
    setUserFiles: Dispatch<SetStateAction<FileEntity[]>>,
    chatSetting: ChatSetting,
    setChatSetting: Dispatch<SetStateAction<ChatSetting>>,
    sessionMessages: SessionMessage[] | [],
    setSessionMessages: Dispatch<SetStateAction<SessionMessage[] | []>>

    isLoadingInitialData: boolean,
    isGenerating: boolean,
    setIsGenerating: Dispatch<SetStateAction<boolean>>,

    isResponsiveLayout: boolean,
    floatActions: SessionFloatActionKey[],
    promptSelection: boolean,
    setPromptSelection: Dispatch<SetStateAction<boolean>>,
};

export const SessionContext = createContext<SessionContextInterface>({
    generateURL: undefined,

    userInput: '',
    setUserInput: () => {},
    attachedFile: undefined,
    setAttachedFile: () => {},
    userFiles: [],
    setUserFiles: () => {},
    chatSetting: {},
    setChatSetting: () => {},
    sessionMessages: [],
    setSessionMessages: () => {},

    isLoadingInitialData: false,
    isGenerating: false,
    setIsGenerating: () => {},

    isResponsiveLayout: true,
    floatActions: [],
    promptSelection: false,
    setPromptSelection: () => {},
});
