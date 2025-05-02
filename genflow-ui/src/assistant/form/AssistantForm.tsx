// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC, useContext } from 'react';

import { AssistantContext, AssistantContextInterface } from '@/context';
import { StepperForm } from '@/common';

import AssistantPromptForm from '@/assistant/form/AssistantPromptForm';
import AssistantIntroForm from '@/assistant/form/AssistantIntroForm';
import AssistantContextForm from '@/assistant/form/AssistantContextForm';
import AssistantFormActions from '@/assistant/form/AssistantFormActions';

const steps = ['label.assistant.step1', 'label.assistant.step2', 'label.assistant.step3'];

type AssistantFormProps = object;

const AssistantForm: FC<AssistantFormProps> = () => {
    const {
        activeStep,
    } = useContext<AssistantContextInterface>(AssistantContext);

    const renderStep = (step: number): JSX.Element | null => {
        switch (step) {
            case 0:
                return (
                    <AssistantPromptForm />
                );
            case 1:
                return (
                    <AssistantIntroForm />
                );
            case 2:
                return (
                    <AssistantContextForm />
                );
            default:
                return null;
        }
    };

    return (
        <StepperForm
            activeStep={activeStep}
            steps={steps}
            renderStepForm={renderStep}
            renderStepActions={() => (
                <AssistantFormActions />
            )}
        />
    );
};

export default AssistantForm;
