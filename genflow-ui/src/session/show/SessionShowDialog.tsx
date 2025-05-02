// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import Grid from '@mui/material/Grid';
import { ShowBase, useTranslate, Identifier } from 'react-admin';

import { Dialog, DialogProps } from '@/common';
import SessionCard from '@/session/show/SessionCard';
import SessionUsageCard from '@/session/show/SessionUsageCard';
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
                        >
                            <SessionUsageCard />
                        </Grid>
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
