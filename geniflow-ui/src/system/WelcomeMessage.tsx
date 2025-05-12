// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC, useContext } from 'react';
import Typography from '@mui/material/Typography';
import { useTranslate, useLocale, Button } from 'react-admin';

import { GlobalContext, GlobalContextInterface } from '@/context';
import { Dialog } from '@/common';

interface WelcomeMessageProps {
    open: boolean;
    onClose: () => void;
};

const WelcomeMessage: FC<WelcomeMessageProps> = ({
    open,
    onClose,
}) => {
    const translate = useTranslate();
    const locale = useLocale();
    const { aboutSystem } = useContext<GlobalContextInterface>(GlobalContext);

    if (!aboutSystem) return null;

    const handleClose = (reason: 'backdropClick' | 'escapeKeyDown'): void => {
        if (reason === 'backdropClick') {
            return;
        }
        onClose();
    };

    return (
        <Dialog
            open={open}
            id='welcome-dialog'
            aria-labelledby={translate('label.welcome')}
            onClose={(event, reason) => handleClose(reason)}
            maxWidth='md'
            fullWidth
            title={(
                <>
                    {aboutSystem.name[locale] ?? aboutSystem.name.en_US}
                    <Typography variant='caption' display='block'>
                        {translate('label.version', { version: aboutSystem.version })}
                    </Typography>
                </>
            )}
            ContentProps={{
                id: 'welcome-dialog-content',
                dividers: true,
            }}
            dialogContent={(
                <>
                    <Typography
                        variant='subtitle2'
                        dangerouslySetInnerHTML={{
                            __html: aboutSystem.welcome[locale] ?? aboutSystem.welcome.en_US,
                        }}
                    />
                    <br />
                    <Typography
                        variant='overline'
                        display='block'
                        sx={{ textAlign: 'right'}}
                        dangerouslySetInnerHTML={{
                            __html: aboutSystem.license[locale] ?? aboutSystem.license.en_US,
                        }}
                    />
                </>
            )}
            dialogAction={() => (
                <>
                    <Button
                        label='ra.action.close'
                        onClick={() => onClose()}
                    />
                    <Button
                        label='action.not_show_again'
                        onClick={() => {
                            localStorage.setItem('showWelcome', 'false');
                            onClose();
                        }}
                        variant='contained'
                        color='secondary'
                    />
                </>
            )}
        />
    );
};

export default WelcomeMessage;
