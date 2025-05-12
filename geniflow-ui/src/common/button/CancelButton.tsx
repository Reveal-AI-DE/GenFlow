// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';
import { Button, ButtonProps } from 'react-admin';

type CancelButtonProps = ButtonProps;

const CancelButton: FC<CancelButtonProps> = ({
    onClick,
    ...rest
}) => (
    <Button
        label='ra.action.cancel'
        onClick={onClick}
        startIcon={<ErrorOutlineIcon />}
        {...rest}
    />
);

export default CancelButton;
