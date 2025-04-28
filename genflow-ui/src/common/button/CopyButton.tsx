// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC, useState } from 'react';
import IconButton from '@mui/material/IconButton';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import { useTranslate } from 'react-admin';

import{ WithTooltip } from '@/common';

interface CopyButtonProps {
    value: any;
};

const CopyButton: FC<CopyButtonProps> = ({
    value,
}) => {
    const translate = useTranslate()
    const [showCheckmark, setShowCheckmark] = useState(false);

    const handleCopy = (): void => {
        if (navigator.clipboard) {
            navigator.clipboard.writeText(value);
        } else {
            const textArea = document.createElement('textarea');
            textArea.value = value;
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
        }
        setShowCheckmark(true);
        setTimeout(() => {
            setShowCheckmark(false);
        }, 1000);
    };

    return (
        <WithTooltip
            title={translate('action.copy')}
            trigger={(
                <span>
                    <IconButton
                        aria-label={translate('action.copy')}
                        onClick={showCheckmark ? undefined:handleCopy}
                        color='primary'
                        size='small'
                    >
                        {
                            showCheckmark ? (
                                <CheckCircleOutlineIcon fontSize='small' />
                            ) : (
                                <ContentCopyIcon fontSize='small' />
                            )
                        }
                    </IconButton>
                </span>
            )}
            arrow
        />
    );
};

export default CopyButton;
