// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC, useContext } from 'react';
import InfoIcon from '@mui/icons-material/Info';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import { useTranslate, useLocale } from 'react-admin';

import { GlobalContext, GlobalContextInterface } from '@/context';
import { MenuItemWithDialog } from '@/common';

const AboutMenuItem: FC = () => {
    const translate = useTranslate();
    const locale = useLocale();
    const { aboutSystem } = useContext<GlobalContextInterface>(GlobalContext);

    if (!aboutSystem) return null;

    return (
        <MenuItemWithDialog
            id='about-menu-item'
            LeftIcon={<InfoIcon />}
            label='label.about'
            dialog={{
                id: 'about-dialog',
                maxWidth: 'sm',
                fullWidth: true,
                'aria-labelledby': translate('label.about'),
                title: (
                    <>
                        {aboutSystem.name[locale] ?? aboutSystem.name.en_US}
                        <Typography variant='caption' display='block'>
                            {translate('label.version', { version: aboutSystem.version })}
                        </Typography>
                    </>
                ),
                disableBackdropClick: true,
                ContentProps: {
                    id: 'about-dialog-content',
                    dividers: true,
                },
                dialogContent: (
                    <>
                        <Typography variant='subtitle2'>
                            {aboutSystem.description[locale] ?? aboutSystem.description.en_US}
                        </Typography>
                        <br />
                        <Divider />
                        <Typography variant='overline' display='block' sx={{ textAlign: 'right' }}>
                            {aboutSystem.license[locale] ?? aboutSystem.license.en_US}
                        </Typography>
                    </>
                ),
            }}
            divider
        />
    );
};

export default AboutMenuItem;
