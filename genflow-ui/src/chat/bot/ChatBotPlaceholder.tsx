// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import SettingsInputCompositeIcon from '@mui/icons-material/SettingsInputComposite';
import { useTranslate } from 'react-admin';

import { PagePlaceholder } from '@/common';

type ChatBotPlaceholderProps = object;

const ChatBotPlaceholder: FC<ChatBotPlaceholderProps> = () => {
    const translate = useTranslate();

    return (
        <PagePlaceholder
            icon={<SettingsInputCompositeIcon />}
        >
            <Box>
                <Typography variant='h3' gutterBottom>
                    {translate('message.chat.bot.title')}
                </Typography>
                <Typography variant='subtitle1' gutterBottom>
                    {translate('message.chat.bot.description')}
                </Typography>
            </Box>
        </PagePlaceholder>
    );
};

export default ChatBotPlaceholder;
