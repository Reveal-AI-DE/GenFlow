// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Grid';
import Stepper from '@mui/material/Stepper';
import Step from '@mui/material/Step';
import StepLabel from '@mui/material/StepLabel';
import {
    Form, useTranslate,
} from 'react-admin';

const Root = styled(Box, {
    name: 'StepperForm',
    slot: 'root',
})(({ theme }) => ({
    width: '100%',
    padding: theme.spacing(2),
}));

const Content = styled(Paper, {
    name: 'StepperForm',
    slot: 'content',
})(({ theme }) => ({
    height: '65vh',
    overflow: 'auto',
    padding: theme.spacing(2),
    marginBottom: theme.spacing(2),
    marginTop: theme.spacing(2),
}));

const Actions = styled(Paper, {
    name: 'StepperForm',
    slot: 'actions',
})(({ theme }) => ({
    padding: theme.spacing(1),
}));

interface StepperFormProps {
    activeStep: number;
    steps: string[];
    renderStepForm: (step: number) => JSX.Element | null;
    renderStepActions: (step: number) => JSX.Element;
};

const StepperForm: FC<StepperFormProps> = ({
    activeStep,
    steps,
    renderStepForm,
    renderStepActions,
}) => {
    const translate = useTranslate();

    return (
        <Root>
            <Stepper activeStep={activeStep} alternativeLabel>
                {steps.map((label) => {
                    const stepProps: { completed?: boolean } = {};
                    return (
                        <Step key={translate(label)} {...stepProps}>
                            <StepLabel>{translate(label)}</StepLabel>
                        </Step>
                    );
                })}
            </Stepper>
            <Form>
                <Grid container spacing={2}>
                    <Grid
                        size={{
                            xs: 12, sm: 12, md: 8, lg: 8, xl: 6
                        }}
                        offset={{
                            xs: 0, sm: 0, md: 2, lg: 2, xl: 3
                        }}
                    >
                        <Content>
                            {renderStepForm(activeStep)}
                        </Content>
                    </Grid>
                    <Grid
                        size={{
                            xs: 12, sm: 12, md: 10, lg: 10, xl: 8
                        }}
                        offset={{
                            xs: 0, sm: 0, md: 1, lg: 1, xl: 2
                        }}
                    >
                        <Actions>
                            {renderStepActions(activeStep)}
                        </Actions>
                    </Grid>
                </Grid>
            </Form>
        </Root>
    );
};

export default StepperForm;
