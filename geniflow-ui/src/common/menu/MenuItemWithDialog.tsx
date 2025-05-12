// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, {
    FC,
    useState,
    ReactNode,
} from 'react';
import {
    useTranslate
} from 'react-admin';

import IconMenuItem,
{
    IconMenuItemProps
} from '@/common/menu/IconMenuItem';
import {
    Dialog,
    DialogProps
} from '@/common/layout';

interface MenuItemWithDialogProps extends Omit<IconMenuItemProps, 'LeftIcon' | 'label' | 'rightIcon'> {
    LeftIcon: ReactNode;
    label: string;
    dialog: Omit<DialogProps, 'open' | 'onClose'> & {
        disableBackdropClick?: boolean;
    };
};

const MenuItemWithDialog: FC<MenuItemWithDialogProps> = ({
    LeftIcon,
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
            <IconMenuItem
                onClick={() => onClick()}
                label={translate(label)}
                leftIcon={LeftIcon}
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

export default MenuItemWithDialog;
