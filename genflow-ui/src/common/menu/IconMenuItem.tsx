// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React,
{
    forwardRef,
    RefObject,
    ReactNode
} from 'react';
import MenuItem,
{
    MenuItemProps as MuiMenuItemProps
} from '@mui/material/MenuItem';
import { styled } from '@mui/material/styles';
import ListItemIcon from '@mui/material/ListItemIcon';

const LeftIconContainer = styled(ListItemIcon, {
    name: 'GFIconMenuItem',
    slot: 'left-icon',
})(() => ({
    minWidth: 5,
}));

const RightIconContainer = styled(ListItemIcon, {
    name: 'GFIconMenuItem',
    slot: 'right-icon',
})(() => ({
    minWidth: 5,
    flexDirection: 'row-reverse'
}));

export interface IconMenuItemProps extends Omit<MuiMenuItemProps, 'ref'> {
    className?: string;
    label?: string;
    leftIcon?: ReactNode;
    onClick?: (event: any) => void;
    ref?: RefObject<HTMLLIElement>;
    rightIcon?: ReactNode;
};

const IconMenuItem = forwardRef<HTMLLIElement, IconMenuItemProps>((
    {
        className, label, leftIcon, rightIcon, ...props
    },
    ref
) => (
    <MenuItem
        ref={ref}
        className={className}
        {...props}
    >
        <LeftIconContainer>
            {leftIcon}
        </LeftIconContainer>
        {label}
        <RightIconContainer>
            {rightIcon}
        </RightIconContainer>
    </MenuItem>
));

export default IconMenuItem;
