// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React from 'react';
import Tooltip from '@mui/material/Tooltip';
import Typography from '@mui/material/Typography';
import {
    FunctionField,
    RaRecord,
} from 'react-admin';

import { truncateText } from '@/utils';

type TruncatedTextFieldProps = {
    source: string;
    length?: number;
};

const TruncatedTextField = <T extends RaRecord>({
    source,
    length = 20,
}: TruncatedTextFieldProps): JSX.Element => (
        <FunctionField
            source={source}
            render={(record: T) => (
                <Tooltip title={record[source]}>
                    <Typography variant='subtitle2' gutterBottom>
                        {truncateText(record[source], length)}
                    </Typography>
                </Tooltip>
            )}
        />
    );

export default TruncatedTextField;
