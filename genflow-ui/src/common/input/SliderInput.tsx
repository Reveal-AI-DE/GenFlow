// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import clsx from 'clsx';
import FormControl , { FormControlProps } from '@mui/material/FormControl';
import Stack from '@mui/material/Stack';
import Slider, { SliderProps } from '@mui/material/Slider';
import Chip from '@mui/material/Chip';
import { styled } from '@mui/material/styles';
import {
    CommonInputProps, useInput, sanitizeInputRestProps, InputHelperText, FieldTitle
} from 'react-admin';
import { Typography } from '@mui/material';

const ValueContainer = styled(Chip, {
    name: 'GFSliderInput',
    slot: 'value',
})(({ theme }) => ({
    marginLeft: theme.spacing(1),
    padding: theme.spacing(0, 1),
}));

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
    InputProps,
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

    const {
        startAdornment,
        endAdornment,
    } = InputProps;

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
                label={(
                    <Typography
                        variant='body1'
                        component='span'
                        color='text.secondary'
                        className='RaLabeled-label'
                    >
                        {label}
                        <ValueContainer
                            label={sliderValue}
                            size='small'
                            variant='outlined'
                            color='primary'
                        />
                    </Typography>
                )}
                source={source}
                resource={resource}
                isRequired={isRequired}
            />
            <Stack
                spacing={2}
                direction='row'
                sx={{
                    alignItems: 'center',
                    mb: 1
                }}
            >
                {startAdornment}
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
                />
                {endAdornment}
            </Stack>
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
        InputProps?: any;
    };

export default SliderInput;
