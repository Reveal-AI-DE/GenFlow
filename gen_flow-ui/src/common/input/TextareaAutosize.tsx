// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import { TextareaAutosize as BaseTextareaAutosize } from '@mui/material';
import { styled } from '@mui/material/styles';
import Input, { InputProps } from '@mui/material/Input';
import OutlinedInput from '@mui/material/OutlinedInput';
import FilledInput from '@mui/material/FilledInput';
import FormControl, { FormControlProps } from '@mui/material/FormControl';

const StyledTextareaAutosize = styled(BaseTextareaAutosize, {
    name: 'GFTextInput',
    slot: 'textarea',
})(() => ({
    // boxSizing: 'border-box',
    width: '100%',
    padding: '12px',
    resize: 'none',
    border: 'none',
    backgroundColor: 'transparent',
    '&:focus': {
        outline: 0,
    },
    '&:focus-visible': {
        outline: 0,
    },
    '&:hover': {
        outline: 0,
    },
}));

interface TextareaAutosizeProps {
    formControlProps?: FormControlProps;
    inputProps?: InputProps;
    variant?: 'standard' | 'outlined' | 'filled';
};

const TextareaAutosize: FC<TextareaAutosizeProps> = ({
    formControlProps, inputProps, variant
}) => {
    let input;
    switch(variant) {
        case 'standard':
            input = (
                <Input
                    inputComponent={StyledTextareaAutosize}
                    {...inputProps}
                />
            )
            break;
        case 'filled':
            input = (
                <FilledInput
                    inputComponent={StyledTextareaAutosize}
                    {...inputProps}
                />
            )
            break;
        default:
            input = (
                <OutlinedInput
                    inputComponent={StyledTextareaAutosize}
                    {...inputProps}
                />
            )
    }
    return (
        <FormControl
            {...formControlProps}
        >
            {input}
        </FormControl>
    );
};

export default TextareaAutosize;
