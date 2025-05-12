// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC, useState } from 'react';
import IconButton from '@mui/material/IconButton';
import SettingsOverscanIcon from '@mui/icons-material/SettingsOverscan';
import { TextInput, TextInputProps, useTranslate } from 'react-admin';

import { Dialog, WithTooltip } from '@/common/layout';

type ExpandableTextInputProps = Omit<TextInputProps, 'value'>;

const ExpandableTextInput: FC<ExpandableTextInputProps> = ({
    onChange,
    ...rest
}) => {
    const [open, setOpen] = useState(false);
    const translate = useTranslate();

    const onClick = (): void => {
        setOpen(true);
    };

    const onClose = (reason: 'backdropClick' | 'escapeKeyDown'): void => {
        if (reason === 'backdropClick') {
            return;
        }
        setOpen(false);
    };

    return (
        <>
            <TextInput
                {...rest}
                slotProps={{
                    input: {
                        endAdornment: (
                            <WithTooltip
                                title={translate('ra.action.expand')}
                                trigger={(
                                    <span>
                                        <IconButton
                                            edge='start'
                                            aria-label={translate('ra.action.expand')}
                                            onClick={onClick}
                                            size='small'
                                        >
                                            <SettingsOverscanIcon
                                                fontSize='small'
                                            />
                                        </IconButton>
                                    </span>
                                )}
                                arrow
                            />
                        ),
                    },
                }}
                multiline
                rows={2}
            />

            <Dialog
                onClose={(event, reason) => onClose(reason)}
                open={open}
                title='Edit Text'
                maxWidth='lg'
                fullWidth
                dialogContent={(
                    <div>
                        <TextInput
                            {...rest}
                            multiline
                            minRows={25}
                            autoFocus
                            fullWidth
                        />
                    </div>
                )}
            />
        </>
    );
};

export default ExpandableTextInput;
