// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import Grid from '@mui/material/Grid2';
import { ShowBase, useTranslate, Identifier } from 'react-admin';

import { Dialog, DialogProps } from '@/common';
import SessionCard from '@/session/show/SessionCard';
import SessionShowButton from '@/session/show/SessionShowButton';

type SessionShowDialogProps = {
    id: Identifier;
    open: DialogProps['open'];
    onClose: DialogProps['onClose'];
};

const SessionShowDialog: FC<SessionShowDialogProps> = ({
    id,
    open,
    onClose,
}) => {
    const translate = useTranslate();

    return (
        <ShowBase
            resource='sessions'
            id={id}
        >
            <Dialog
                onClose={(event, reason) => onClose && onClose(event, reason)}
                open={open}
                title={translate('label.session_info')}
                maxWidth='lg'
                disableEscapeKeyDown
                dialogContent={(
                    <Grid
                        container
                        spacing={2}
                    >
                        <Grid
                            size={{
                                xs: 12,
                                sm: 12,
                                md: 12,
                                lg: 6
                            }}
                        >
                            <SessionCard />
                        </Grid>
                        <Grid
                            size={{
                                xs: 12,
                                sm: 12,
                                md: 12,
                                lg: 6
                            }}
                        />
                    </Grid>
                )}
                dialogAction={() => (
                    <SessionShowButton
                        label='label.view'
                    />
                )}
            />
        </ShowBase>
    );
}

export default SessionShowDialog;
