// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC, useState, useRef } from 'react';
import clsx from 'clsx';
import FormControl , { FormControlProps } from '@mui/material/FormControl';
import {
    CommonInputProps, useInput, sanitizeInputRestProps,
    InputHelperText, FieldTitle
} from 'react-admin';
import {
    MuiColorInput, MuiColorInputProps,
    matchIsValidColor,
} from 'mui-color-input'

const ColorInput: FC<ColorInputProps> = ({
    className,
    defaultValue = null,
    helperText,
    label,
    margin,
    onChange,
    onBlur,
    onFocus,
    resource,
    source,
    validate,
    variant,
    readOnly,
    disabled,
    format,
    ...rest
}) => {
    const {
        field,
        fieldState: { error, invalid },
        id,
        isRequired,
    } = useInput({
        defaultValue,
        onBlur,
        resource,
        source,
        validate,
        disabled,
        readOnly,
        ...rest,
    });

    const { onBlur: onBlurFromField } = field;

    const [colorValue, setColorValue] = useState(field.value);

    const hasFocus = useRef(false);

    // update the input text when the record changes
    React.useEffect(() => {
        if (!hasFocus.current) {
            setColorValue(colorValue);
        }
    }, [field.value]);

    const handleChange = (value: string): void => {
        if (matchIsValidColor(value)) {
            if (onChange) {
                onChange();
            }
            setColorValue(value);
            field.onChange(value);
        }
    };

    const handleFocus = (event: React.FocusEvent<HTMLInputElement>): void => {
        if (onFocus) {
            onFocus(event);
        }
        hasFocus.current = true;
    };

    const handleBlur = (): void => {
        if (onBlurFromField) {
            onBlurFromField();
        }
        hasFocus.current = false;
        setColorValue(field.value);
    };

    const renderHelperText = helperText !== false || invalid;
    const { ref, ...fieldWithoutRef } = field;

    return (
        <FormControl
            className={clsx('ra-input', `ra-input-${source}`, className)}
            variant={variant}
            error={invalid}
            disabled={disabled || readOnly}
            margin={margin}
            {...sanitizeInputRestProps(rest)}
        >
            <FieldTitle
                label={label}
                source={source}
                resource={resource}
                isRequired={isRequired}
            />
            <MuiColorInput
                id={id}
                {...fieldWithoutRef}
                ref={ref}
                name={field.name}
                value={colorValue}
                onChange={handleChange}
                onFocus={handleFocus}
                onBlur={handleBlur}
                aria-labelledby='color-label'
                size='small'
                format={format}
            />
            {
                renderHelperText ? (
                    <InputHelperText
                        error={error?.message}
                        helperText={helperText}
                    />
                ) : null
            }
        </FormControl>
    );
};

type ColorInputProps = Omit<CommonInputProps, 'format'> &
    Omit<MuiColorInputProps, 'defaultValue' | 'value'> &
    FormControlProps & {
    };

export default ColorInput;
