// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import { SelectInput, required } from 'react-admin';
import { useWatch } from 'react-hook-form';

import { ContextSource } from '@/types';
import { getChoicesFromEnum } from '@/utils';
import AssistantFilesUpload from '@/assistant/form/AssistantFileUpload';

type AssistantContextSourceSetupProps = object;

const AssistantContextSourceSetup : FC<AssistantContextSourceSetupProps> = () => {
    const { context_source: contextSource } = useWatch();

    const renderContextSourceForm = (): JSX.Element | null => {
        switch (contextSource) {
            case ContextSource.FILES:
                return <AssistantFilesUpload />;
            case ContextSource.COLLECTIONS:
                return null;
            default:
                return null;
        }
    };

    return (
        <>
            <SelectInput
                source='context_source'
                choices={getChoicesFromEnum(ContextSource)}
                defaultValue={ContextSource.FILES}
                validate={required()}
            />
            {renderContextSourceForm()}
        </>
    );
}

export default AssistantContextSourceSetup;
