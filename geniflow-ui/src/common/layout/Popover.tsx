// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, {
    FC, useState, MouseEvent, ReactNode
} from 'react';
import {
    Popover as MuiPopover,
    PopoverOrigin,
}from '@mui/material';
import { Button, ButtonProps } from 'react-admin';
import SpeedDialAction, { SpeedDialActionProps } from '@mui/material/SpeedDialAction';

interface PopoverProps {
    component: 'button' | 'fab';
    children: ReactNode;
    componentProps?: ButtonProps | SpeedDialActionProps;
    anchorOrigin?: PopoverOrigin;
    transformOrigin?: PopoverOrigin;
}

const Popover: FC<PopoverProps> = ({
    component, children, componentProps, anchorOrigin, transformOrigin,
}) => {
    const [anchorEl, setAnchorEl] = useState<HTMLButtonElement | HTMLDivElement | null>(null);

    const handleClose = (): void => {
        setAnchorEl(null);
    };

    const open = Boolean(anchorEl);
    const id = open ? 'popover' : undefined;

    return (
        <>
            {
                component === 'button' ? (
                    <Button
                        aria-describedby={id}
                        onClick={(event: MouseEvent<HTMLButtonElement>) => setAnchorEl(event.currentTarget)}
                        {...componentProps as ButtonProps}
                    />
                ) : (
                    <SpeedDialAction
                        aria-describedby={id}
                        onClick={(event: MouseEvent<HTMLDivElement>) => setAnchorEl(event.currentTarget)}
                        {...componentProps as SpeedDialActionProps}
                    />
                )
            }
            <MuiPopover
                id={id}
                open={open}
                anchorEl={anchorEl}
                onClose={handleClose}
                anchorOrigin={anchorOrigin}
                transformOrigin={transformOrigin}
                sx={{ overflow: 'auto' }}
            >
                {children}
            </MuiPopover>
        </>
    );
};

export default Popover;
