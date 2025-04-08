// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import Box from '@mui/material/Box';
import Link from '@mui/material/Link';
import LaunchIcon from '@mui/icons-material/Launch';
import Typography from '@mui/material/Typography';
import { useRecordContext, useLocale } from 'react-admin';

import { AIProviderConfiguration } from '@/types';

type ProviderHelpProps = object;

const ProviderHelp: FC<ProviderHelpProps> = () => {
    const record = useRecordContext<AIProviderConfiguration>();
    const locale = useLocale();
    if (!record || !record.help) return null;

    return (
        <Box flexGrow={1}>
            {
                record.help.url ? (
                    <Link
                        href={record.help.url[locale] ?? record.help.url.en_US}
                        target='_blank'
                        rel='noreferrer'
                        variant='caption'
                        underline='none'
                    >
                        <span>
                            <span style={{marginRight: '2px'}}>
                                {record.help.title[locale] ?? record.help.title.en_US}
                            </span>
                            <LaunchIcon fontSize='inherit' />
                        </span>
                    </Link>
                ) : (
                    <Typography variant='body2' component='span'>{record.help.title[locale] ?? record.help.title.en_US}</Typography>
                )
            }
        </Box>
    );
};

export default ProviderHelp;
