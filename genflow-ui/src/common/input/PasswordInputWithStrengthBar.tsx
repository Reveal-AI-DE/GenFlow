// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC, useState } from 'react';
import zxcvbn from 'zxcvbn';
import {
    PasswordInput, PasswordInputProps, LinearProgress,
    LinearProgressProps, ValidationErrorMessage
} from 'react-admin';

export const validatePassword = (value: string, username: string, email: string):
    ValidationErrorMessage
    | null
    | undefined
    | Promise<ValidationErrorMessage | null | undefined> => {
    if (!value) {
        return 'ra.validation.required';
    }
    // Rule 1: At least 8 characters
    if (value.length < 8) {
        return { message: 'validation.password.min', args: { number: 8 } };
    }
    // Rule 2: Not entirely numeric
    if (/^\d+$/.test(value)) {
        return 'validation.password.numeric';
    }
    // Rule 3: Not too similar to personal information
    if (username && value.toLowerCase().includes(username.toLowerCase())) {
        return 'validation.password.personal';
    }
    if (email && value.toLowerCase().includes(email.toLowerCase())) {
        return 'validation.password.personal';
    }
    return undefined;
};

export const matchPassword = (value: string, password: string):
    ValidationErrorMessage
    | null
    | undefined
    | Promise<ValidationErrorMessage | null | undefined> => {
    if (value.length !== password.length || value !== password) {
        return 'The two passwords must match';
    }
    return undefined;
};

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
