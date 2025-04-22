// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import ChatIcon from '@mui/icons-material/Chat';
import { useTranslate } from 'react-admin';

import { PagePlaceholder } from '@/common';

type NewSessionPlaceholderProps = object;

const NewSessionPlaceholder: FC<NewSessionPlaceholderProps> = () => {
    const translate = useTranslate();

    return (
        <PagePlaceholder
            icon={<ChatIcon />}
            sx={{
                height: '80%',
            }}
        >
            <Box>
                <Typography variant='h3' gutterBottom>
                    {translate('message.chat.new.title')}
                </Typography>
                <Typography variant='subtitle1' gutterBottom>
                    {translate('message.chat.new.description')}
                </Typography>
            </Box>
        </PagePlaceholder>
    );
};

export default NewSessionPlaceholder;
