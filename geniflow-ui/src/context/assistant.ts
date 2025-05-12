// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import { Dispatch, SetStateAction, createContext } from 'react';

import { FormMode } from '@/types';

export interface AssistantContextInterface {
    activeStep: number;
    setActiveStep: Dispatch<SetStateAction<number>>
    mode: FormMode;
    setMode: Dispatch<SetStateAction<FormMode>>;
    remainingFiles: number;
    setRemainingFiles: Dispatch<SetStateAction<number>>;
};

export const AssistantContext = createContext<AssistantContextInterface>({
    activeStep: 0,
    setActiveStep: () => {},
    mode: FormMode.CREATE,
    setMode: () => {},
    remainingFiles: 0,
    setRemainingFiles: () => {},
});
