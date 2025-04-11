// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import Box from '@mui/material/Box';
import Link from '@mui/material/Link';
import LaunchIcon from '@mui/icons-material/Launch';
import Typography from '@mui/material/Typography';
import { useLocale } from 'react-admin';

import { HelpEntity } from '@/types';

interface ProviderHelpProps {
    help?: HelpEntity;
};

const ProviderHelp: FC<ProviderHelpProps> = ({
    help,
}) => {
    const locale = useLocale();
    if (!help) return null;

    return (
        <Box flexGrow={1}>
            {
                help.url ? (
                    <Link
                        href={help.url[locale] ?? help.url.en_US}
                        target='_blank'
                        rel='noreferrer'
                        variant='caption'
                        underline='none'
                    >
                        <span>
                            <span style={{marginRight: '2px'}}>
                                {help.title[locale] ?? help.title.en_US}
                            </span>
                            <LaunchIcon fontSize='inherit' />
                        </span>
                    </Link>
                ) : (
                    <Typography variant='body2' component='span'>{help.title[locale] ?? help.title.en_US}</Typography>
                )
            }
        </Box>
    );
};

export default ProviderHelp;
