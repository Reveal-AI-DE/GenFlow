// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, {
    FC,
    useState,
} from 'react';
import { useTranslate, Button, ButtonProps } from 'react-admin';

import { Dialog, DialogProps } from '../layout';

interface ButtonWithDialogProps extends ButtonProps {
    dialog: Omit<DialogProps, 'open' | 'onClose'> & {
        disableBackdropClick?: boolean;
    };
};

const ButtonWithDialog: FC<ButtonWithDialogProps> = ({
    startIcon,
    label,
    dialog,
    ...props
}) => {
    const translate = useTranslate();
    const [open, setOpen] = useState<boolean>(false);

    const {
        title,
        dialogContent,
        dialogAction,
        ContentProps,
        ActionsProps,
        disableBackdropClick,
        ...rest
    } = dialog;

    const onClick = (): void => {
        setOpen(true);
    };

    const onClose = (reason: 'backdropClick' | 'escapeKeyDown'): void => {
        if (disableBackdropClick && reason === 'backdropClick') {
            return;
        }
        setOpen(false);
    };

    return (
        <>
            <Button
                onClick={onClick}
                label={label ? translate(label) : ''}
                startIcon={startIcon}
                {...props}
            />
            <Dialog
                onClose={(event, reason) => onClose(reason)}
                open={open}
                title={title}
                dialogContent={dialogContent}
                dialogAction={dialogAction}
                ContentProps={ContentProps}
                ActionsProps={ActionsProps}
                {...rest}
            />
        </>
    )
};

export default ButtonWithDialog;
