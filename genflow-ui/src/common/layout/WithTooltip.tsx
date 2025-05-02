// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC, ReactElement } from 'react';
import Tooltip, { TooltipProps } from '@mui/material/Tooltip';

interface WithTooltipProps extends Omit<TooltipProps, 'children'> {
    trigger: ReactElement<unknown, any>;
};

const WithTooltip: FC<WithTooltipProps> = ({
    trigger,
    ...tooltipProps
}) => {
    const {
        title,
        placement,
        arrow,
        ...rest
    } = tooltipProps;
    return (
        <Tooltip
            title={title}
            placement={placement || 'top'}
            arrow
            {...rest}
        >
            {trigger}
        </Tooltip>
    );
};

export default WithTooltip;
