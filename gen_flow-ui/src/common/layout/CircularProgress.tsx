// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import Box from '@mui/material/Box';
import {
    CircularProgress as MuiCircularProgress,
    CircularProgressProps as MuiCircularProgressProps,
} from '@mui/material';
import Typography from '@mui/material/Typography';
import { styled } from '@mui/material/styles';

const Root = styled(Box, {
    name: 'GFCircularProgress',
    slot: 'root',
})(() => ({
    position: 'relative',
    display: 'inline-flex',
}));

const LabelContainer = styled(Box, {
    name: 'GFCircularProgress',
    slot: 'label',
})(() => ({
    top: 0,
    left: 0,
    bottom: 0,
    right: 0,
    position: 'absolute',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
}));

interface CircularProgressProps extends MuiCircularProgressProps {
    value: number;
    withLabel?: boolean;
};

const CircularProgress: FC<CircularProgressProps> = ({
    value,
    withLabel=true,
}) => (
    <Root>
        <MuiCircularProgress
            variant='determinate'
            value={value}
        />
        {
            withLabel && (
                <LabelContainer>
                    <Typography
                        variant='caption'
                        component='div'
                        sx={{ color: 'text.secondary' }}
                    >
                        {`${Math.round(value)}%`}
                    </Typography>
                </LabelContainer>
            )
        }
    </Root>
)

export default CircularProgress;
