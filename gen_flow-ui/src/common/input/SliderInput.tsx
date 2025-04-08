// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import clsx from 'clsx';
import FormControl , { FormControlProps } from '@mui/material/FormControl';
import Slider, { SliderProps } from '@mui/material/Slider';
import {
    CommonInputProps, useInput, sanitizeInputRestProps, InputHelperText, FieldTitle
} from 'react-admin';

const SliderInput: FC<SliderInputProps> = ({
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
    min,
    max,
    step = undefined,
    validate,
    variant,
    readOnly,
    disabled,
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

    const [sliderValue, setSliderValue] = React.useState(field.value);

    const hasFocus = React.useRef(false);

    // update the input text when the record changes
    React.useEffect(() => {
        if (!hasFocus.current) {
            setSliderValue(sliderValue);
        }
    }, [field.value]);

    const handleChange = (event: Event, value: number | number[]): void => {
        if (onChange) {
            onChange(event);
        }
        setSliderValue(value);
        field.onChange(value);
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
        setSliderValue(field.value);
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
                label={`${label} ${sliderValue}`}
                source={source}
                resource={resource}
                isRequired={isRequired}
            />
            <Slider
                id={id}
                {...fieldWithoutRef}
                ref={ref}
                name={field.name}
                min={min}
                max={max}
                step={step}
                value={sliderValue}
                onChange={handleChange}
                onFocus={handleFocus}
                onBlur={handleBlur}
                aria-labelledby='slider-label'
                size='small'
                valueLabelDisplay='auto'
                sx={{ width: '90%' }}
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

type SliderInputProps = CommonInputProps &
    Omit<SliderProps, 'defaultValue'> &
    FormControlProps & {
        options?: SliderProps;
    };

export default SliderInput;
