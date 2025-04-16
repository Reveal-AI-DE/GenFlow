// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, {
    FC, useState, useRef, useEffect,
    KeyboardEvent
} from 'react';
import EditIcon from '@mui/icons-material/Edit';
import IconButton from '@mui/material/IconButton';
import InputAdornment from '@mui/material/InputAdornment';
import CheckIcon from '@mui/icons-material/Check';
import CloseIcon from '@mui/icons-material/Close';
import {
    Form, TextInput, useRecordContext,
    required, EditBase, useRefresh,
} from 'react-admin';

import { Session } from '@/types';

type SessionNameProps = object;

const SessionName: FC<SessionNameProps> = () => {
    const session = useRecordContext<Session>();
    const [edit, setEdit] = useState<boolean>(false);
    const inputRef = useRef<HTMLInputElement>(null);
    const refresh = useRefresh();

    useEffect(() => {
        if (edit && inputRef.current) {
            inputRef.current.focus();
        }
    }, [edit]);

    useEffect(() => {
        // Function to handle clicks outside the input
        const handleClickOutside = (event: MouseEvent): void => {
            if (inputRef.current && !inputRef.current.contains(event.target as Node)) {
                setEdit(false);
            }
        };

        // Add event listener to handle clicks outside the input
        if (edit) {
            document.addEventListener('mousedown', handleClickOutside);
        } else {
            document.removeEventListener('mousedown', handleClickOutside);
        }

        // Cleanup event listener on component unmount
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, [edit]);

    if (!session) {
        return null;
    }

    const handleKeyPress = (event: KeyboardEvent<HTMLInputElement>): void => {
        if (event.key === 'Escape') {
            event.preventDefault();
            setEdit(false);
        }
    };

    return edit ? (
        <EditBase
            resource='sessions'
            id={session.id}
            mutationMode='pessimistic'
            transform={
                (data) => ({
                    name: data.name
                })
            }
            mutationOptions={{
                onSuccess: () => {
                    setEdit(false);
                    refresh();
                },
            }}
        >
            <Form>
                <TextInput
                    source='name'
                    variant='outlined'
                    onKeyDown={handleKeyPress}
                    validate={required()}
                    slotProps={{
                        input: {
                            ref: inputRef,
                            endAdornment: (
                                <InputAdornment position='end'>
                                    <IconButton
                                        onClick={() => setEdit(false)}
                                        color='error'
                                        size='small'
                                    >
                                        <CloseIcon />
                                    </IconButton>
                                    <IconButton
                                        type='submit'
                                        color='primary'
                                        size='small'
                                    >
                                        <CheckIcon />
                                    </IconButton>
                                </InputAdornment>
                            )
                        },
                    }}
                />
            </Form>
        </EditBase>
    ) : (
        <>
            {session.name}
            <IconButton
                onClick={() => setEdit(true)}
                size='small'
                color='primary'
            >
                <EditIcon />
            </IconButton>
        </>
    );
};

export default SessionName;
