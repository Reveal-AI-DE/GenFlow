// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC, useContext } from 'react';
import Box from '@mui/material/Box';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import DoneAllIcon from '@mui/icons-material/DoneAll';
import {
    TopToolbar, SaveButton, Button, useRecordContext,
    useRedirect, ButtonProps, useStore,
} from 'react-admin';

import {
    FormMode, Assistant, AssistantData, AssistantStatus,
} from '@/types';
import { CancelButton } from '@/common';
import { AssistantContext, AssistantContextInterface } from '@/context';

type AssistantFormActionsProps = object;

const AssistantFormActions: FC<AssistantFormActionsProps> = () => {
    const assistant = useRecordContext<Assistant>();
    const [,setAssistantCreated] = useStore<boolean>('assistantCreated');
    const redirect = useRedirect();

    const defaultButtonProps: ButtonProps = {
        variant: 'outlined',
        size: 'medium',
    };

    const {
        remainingFiles,
        activeStep,
        setActiveStep,
        mode,
    } = useContext<AssistantContextInterface>(AssistantContext);

    const goNext = (): void => {
        setActiveStep((prevActiveStep) => prevActiveStep + 1);
    };

    const goBack = (): void => {
        setActiveStep((prevActiveStep) => prevActiveStep - 1);
    };

    const transform = (values: Assistant): AssistantData => {
        const {
            group,
            related_model: relatedModel,
            ...rest
        } = values;
        const { provider_name: providerName, model_name: modelName, config } = relatedModel;
        return ({
            group_id: group.id,
            related_model: {
                provider_name: providerName,
                model_name: modelName,
                config,
            },
            ...rest,
        })
    };

    const getLabel = (): string => {
        if (activeStep !== 2) return 'action.next';
        if (assistant && assistant.assistant_status === AssistantStatus.PUBLISHED) {
            return 'action.draft';
        }
        return 'action.publish';
    };

    const transformToPublish = (data: Assistant): AssistantData => ({
        ...transform(data),
        assistant_status: data.assistant_status === AssistantStatus.PUBLISHED ?
            AssistantStatus.DRAFTED :
            AssistantStatus.PUBLISHED,
    });

    return (
        <TopToolbar
            sx={{
                justifyContent: 'space-between',
            }}
        >
            <Box>
                <Button
                    label='action.back'
                    startIcon={<ArrowBackIcon />}
                    onClick={() => {
                        setAssistantCreated(false);
                        goBack();
                    }}
                    sx={{ mr: 2 }}
                    disabled={activeStep === 0}
                    {...defaultButtonProps}
                />
                <CancelButton
                    onClick={() => {
                        setAssistantCreated(false);
                        redirect('list', 'assistants');
                    }}
                    {...defaultButtonProps}
                />
            </Box>
            <SaveButton
                type='button'
                label={getLabel()}
                endIcon={activeStep !== 2 ? <ArrowForwardIcon />:undefined}
                icon={<DoneAllIcon />}
                mutationOptions={
                    mode === FormMode.CREATE ? ({
                        onSuccess: (data) => {
                            setAssistantCreated(true);
                            redirect('edit', 'assistants', data.id, data);
                            goNext();
                        }
                    }) : ({
                        onSuccess: () => {
                            setAssistantCreated(false);
                            if (activeStep < 2) {
                                goNext();
                            } else {
                                redirect('list', 'assistants');
                            }
                        }
                    })
                }
                transform={activeStep === 2 ? transformToPublish:transform}
                alwaysEnable={mode !== FormMode.CREATE && remainingFiles === 0}
                {...defaultButtonProps}
            />
        </TopToolbar>
    );
};

export default AssistantFormActions;
