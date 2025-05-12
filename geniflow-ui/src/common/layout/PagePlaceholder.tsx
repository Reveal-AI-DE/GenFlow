// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC, ReactNode } from 'react';
import Box, { BoxProps } from '@mui/material/Box';
import { styled } from '@mui/material/styles';

const Root = styled(Box, {
    name: 'GFPagePlaceholder',
    slot: 'root',
})(() => ({
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100%',
    '& svg': {
        width: '9em',
        height: '9em',
    }
}));

type PagePlaceholderProps = {
    children?: ReactNode;
    icon?: ReactNode;
    sx?: BoxProps['sx'];
};

const PagePlaceholder: FC<PagePlaceholderProps> = ({
    icon,
    children,
    sx
}) => (
    <Root sx={sx}>
        {icon}
        {children}
    </Root>
)

export default PagePlaceholder;
