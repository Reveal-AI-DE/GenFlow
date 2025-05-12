// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import { styled } from '@mui/material/styles';
import CircularProgress from '@mui/material/CircularProgress';
import Button, { ButtonProps } from '@mui/material/Button';

const StyledCircularProgress = styled(CircularProgress, {
    name: 'GFButtonWithLoadingIndicatorProps',
    slot: 'loading',
})(({ theme }) => ({
    marginRight: theme.spacing(1),
}));

interface ButtonWithLoadingIndicatorProps extends ButtonProps {
    loading?: boolean;
    icon?: React.ReactNode;
};

const ButtonWithLoadingIndicator: FC<ButtonWithLoadingIndicatorProps> = ({
    loading = false,
    children,
    icon,
    ...rest
}) => (
    <Button
        disabled={loading}
        {...rest}
    >
        {
            loading ? (
                <StyledCircularProgress
                    size={14}
                    thickness={3}
                    color='inherit'
                />
            ) : (
                icon
            )
        }
        {children}
    </Button>
);

export default ButtonWithLoadingIndicator;
