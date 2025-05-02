// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import IconButton from '@mui/material/IconButton';
import StarOutlineIcon from '@mui/icons-material/StarOutline';
import GradeIcon from '@mui/icons-material/Grade';
import { styled } from '@mui/material/styles';
import {
    useRecordContext, useDataProvider, useNotify,
    useResourceContext, useRefresh, useTranslate,
} from 'react-admin';

import { Prompt } from '@/types';
import { WithTooltip } from '@/common/layout';

export const StyledGradeIcon = styled(GradeIcon, {
    name: 'GFPinButton',
    slot: 'icon',
})(() => ({
    color: '#ffeb00',
}));

interface PinButtonProps {
    disabled?: boolean;
};

const PinButton: FC<PinButtonProps> = ({
    disabled,
}) => {
    const record = useRecordContext<Prompt>();
    const resource = useResourceContext();
    const dataProvider = useDataProvider();
    const refresh = useRefresh();
    const translate = useTranslate();
    const notify = useNotify();

    if (!record || !resource) {
        return null;
    }

    const Pin = async (): Promise<void> => {
        await dataProvider.update(
            resource, {
                id: record.id,
                data: {
                    is_pinned: !record.is_pinned,
                },
                previousData: record,
            }
        ).then(() => {
            refresh();
        }).catch(() => notify(
            'ra.notification.http_error',
            {
                type: 'error',
            }));
    };

    return (
        <WithTooltip
            title={record.is_pinned ? translate('action.unpin') : translate('action.pin')}
            trigger={(
                <span>
                    <IconButton
                        onClick={Pin}
                        disabled={disabled}
                    >
                        {
                            record.is_pinned ? (
                                <StyledGradeIcon />
                            ) : (
                                <StarOutlineIcon />
                            )
                        }
                    </IconButton>
                </span>
            )}
        />
    );
};

export default PinButton;
