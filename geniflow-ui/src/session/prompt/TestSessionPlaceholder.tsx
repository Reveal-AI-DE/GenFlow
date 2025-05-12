// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import BiotechIcon from '@mui/icons-material/Biotech';
import { useTranslate } from 'react-admin';

import { PagePlaceholder } from '@/common';

type TestSessionPlaceholderProps = object;

const TestSessionPlaceholder: FC<TestSessionPlaceholderProps> = () => {
    const translate = useTranslate();

    return (
        <PagePlaceholder
            icon={<BiotechIcon />}
            sx={{
                height: '80%',
            }}
        >
            <Box>
                <Typography variant='h4' gutterBottom>
                    {translate('message.prompt.start_test_title')}
                </Typography>
                <Typography variant='subtitle1' gutterBottom>
                    {translate('message.prompt.start_test_content')}
                </Typography>
            </Box>
        </PagePlaceholder>
    );
};

export default TestSessionPlaceholder;
