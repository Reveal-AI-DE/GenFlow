// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, {
    useState, FC, ReactNode,
    useMemo,
} from 'react';
import { useStore } from 'react-admin';

import { AssistantContext } from '@/context';
import { FormMode } from '@/types';

interface AssistantStateProps {
    children: ReactNode,
    formMode: FormMode,
};

export const AssistantState: FC<AssistantStateProps> = ({
    children,
    formMode,
}) => {
    const [assistantCreated,] = useStore<boolean>('assistantCreated');

    const [activeStep, setActiveStep] = useState<number>(assistantCreated ? 1 : 0);
    const [mode, setMode] = useState<FormMode>(formMode);
    const [remainingFiles, setRemainingFiles] = useState<number>(0);

    const contextValue = useMemo(() => ({
        activeStep,
        setActiveStep,
        mode,
        setMode,
        remainingFiles,
        setRemainingFiles,
    }), [activeStep, mode, remainingFiles]);

    return (
        <AssistantContext.Provider value={contextValue}>
            {children}
        </AssistantContext.Provider>
    );
};
