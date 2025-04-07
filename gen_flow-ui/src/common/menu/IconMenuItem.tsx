// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

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

export const LeftIconContainer = styled(ListItemIcon, {
    name: 'GFIconMenuItem',
    slot: 'left-icon',
})(() => ({
    minWidth: 5,
}));

export const RightIconContainer = styled(ListItemIcon, {
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
    onClick?: (event: React.MouseEvent<HTMLElement>) => void;
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
