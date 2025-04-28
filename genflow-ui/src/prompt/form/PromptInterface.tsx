// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC, useState } from 'react';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid2';
import { styled } from '@mui/material/styles';
import {
    Create, Edit, Form,
} from 'react-admin';
import { matchPath, useLocation } from 'react-router';

import { ModelParameterForm } from '@/provider/model';

import { PromptInfo } from '@/prompt/show';
import { PromptTestSession} from '@/session/prompt';
import PromptForm from '@/prompt/form/PromptForm';
import PromptFormActions from '@/prompt/form/PromptFormActions';

const StyledBox = styled(Box, {
    name: 'GFPromptInterface',
    slot: 'form',
})(({ theme }) => ({
    height: '80vh',
    overflow: 'auto',
    padding: theme.spacing(2),
    display: 'flex',
    flexDirection: 'column',
}));

type PromptInterfaceProps = object;

const PromptInterface: FC<PromptInterfaceProps> = () => {
    const location = useLocation();
    const match = matchPath('/prompts/create', location.pathname);

    const [testing, setTesting] = useState<boolean>(false);

    let PromptRoot: any = Edit;
    // create mode
    if (match) {
        PromptRoot = Create;
    }

    return (
        <Grid container spacing={2}>
            <Grid
                size={{
                    xs: 12,
                    sm: 12,
                    md: 6,
                    lg: 6,
                    xl: 6
                }}
            >
                <PromptRoot
                    mutationMode='pessimistic'
                >
                    <Form>
                        <StyledBox>
                            {
                                testing ? (
                                    <PromptInfo />
                                ) : (
                                    <>
                                        <PromptForm />
                                        <ModelParameterForm />
                                    </>
                                )
                            }
                        </StyledBox>
                        <PromptFormActions
                            testing={testing}
                            setTesting={setTesting}
                            createMode={!!match}
                        />
                    </Form>
                </PromptRoot>
            </Grid>
            <Grid
                size={{
                    xs: 12,
                    sm: 12,
                    md: 6,
                    lg: 6,
                    xl: 6
                }}
            >
                <PromptTestSession
                    opened={testing}
                />
            </Grid>
        </Grid>
    )
};

export default PromptInterface;
