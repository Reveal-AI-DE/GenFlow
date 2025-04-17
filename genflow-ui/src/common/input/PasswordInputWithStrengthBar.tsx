// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC, useState } from 'react';
import zxcvbn from 'zxcvbn';
import {
    PasswordInput, PasswordInputProps, LinearProgress, LinearProgressProps,
} from 'react-admin';

interface PasswordInputWithStrengthBarProps extends PasswordInputProps {
    linearProgressClasses?: LinearProgressProps['classes'];
};

const PasswordInputWithStrengthBar: FC<PasswordInputWithStrengthBarProps> = ({
    linearProgressClasses,
    onChange,
    slotProps,
    ...rest
}) => {
    const [passwordStrength, setPasswordStrength] = useState(0);

    const handlePasswordChange = (value: string): void => {
        const result = zxcvbn(value); // Score ranges from 0 (weak) to 4 (strong)
        setPasswordStrength(result.score);
        if (onChange) {
            onChange(value);
        }
    };

    const setLinearProgressColor = (value: number): 'error' | 'warning' | 'success' => {
        if (value < 2) {
            return 'error';
        }
        if (value < 4) {
            return 'warning';
        }
        return 'success';
    };

    return (
        <>
            <PasswordInput
                onChange={(e: any) => handlePasswordChange(e.target.value)}
                slotProps={{
                    ...slotProps,
                    htmlInput: { autoComplete: 'current-password' }
                }}
                {...rest}
            />
            <LinearProgress
                variant='determinate'
                value={(passwordStrength / 4) * 100}
                classes={linearProgressClasses}
                color={setLinearProgressColor(passwordStrength)}
            />
        </>
    )
};

export default PasswordInputWithStrengthBar;
