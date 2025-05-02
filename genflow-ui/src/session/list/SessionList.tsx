// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC, useState } from 'react';
import {
    Datagrid, List, TextField,
    DateField, Identifier, RowClickFunction,
} from 'react-admin';

import { SessionShowButton, SessionShowDialog } from '@/session/show';

type SessionListProps = object;

const SessionList : FC<SessionListProps> = () => {
    const [selectedSessionId, setSelectedSessionId] = useState<Identifier | undefined>();
    const [open, setOpen] = useState<boolean>(false);

    const rowClick: RowClickFunction = (id) => {
        setSelectedSessionId(id);
        setOpen(true);
        return false;
    };

    const onClose = (reason: 'backdropClick' | 'escapeKeyDown'): void => {
        if (reason === 'backdropClick') {
            return;
        }
        setOpen(false);
    };

    return (
        <>
            <List
                sort={{
                    field: 'created_date',
                    order: 'DESC'
                }}
            >
                <Datagrid
                    rowClick={rowClick}
                >
                    <TextField source='name' />
                    <TextField source='session_type' />
                    <TextField source='owner.username' />
                    <DateField source='created_date' showTime />
                    <SessionShowButton />
                </Datagrid>
            </List>
            {
                selectedSessionId && (
                    <SessionShowDialog
                        id={selectedSessionId}
                        open={open}
                        onClose={onClose}
                    />
                )
            }
        </>
    );
};

export default SessionList;
