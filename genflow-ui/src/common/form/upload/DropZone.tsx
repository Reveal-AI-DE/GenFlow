// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC, ReactNode } from 'react';
import Box from '@mui/material/Box';
import { useDropzone, DropzoneOptions } from 'react-dropzone';
import { useTranslate } from 'react-admin';
import { useUploadyContext } from '@rpldy/uploady';
import { styled } from '@mui/material/styles';

const StyledBox = styled(Box, {
    name: 'GFDropZone',
    slot: 'root',
})(({ theme }) => ({
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    padding: theme.spacing(2),
    border: '2px dashed #bdbdbd',
    borderRadius: '2px',
    backgroundColor: '#fafafa',
    color: '#bdbdbd',
    outline: 'none',
    transition: 'border .24s ease-in-out',
}));

export interface DropZoneProps {
    accept?: DropzoneOptions['accept'];
    maxSize?: DropzoneOptions['maxSize'];
    minSize?: DropzoneOptions['minSize'];
    multiple?: DropzoneOptions['multiple'];
    options?: DropzoneOptions;
    placeholder?: ReactNode;
    labelMultiple?: string;
    labelSingle?: string;
};

const DropZone: FC<DropZoneProps> = ({
    accept,
    maxSize,
    minSize,
    multiple = false,
    placeholder,
    options = {},
    labelMultiple = 'ra.input.file.upload_several',
    labelSingle = 'ra.input.file.upload_single',
}) => {
    const translate = useTranslate();
    const { onDrop: onDropProp } = options;
    const { upload } = useUploadyContext();

    const onDrop: DropzoneOptions['onDrop'] = (newFiles, rejectedFiles, event) => {
        if (multiple) {
            upload(newFiles);
        } else {
            upload(newFiles[0]);
        }

        if (onDropProp) {
            onDropProp(newFiles, rejectedFiles, event);
        }
    };

    const { getRootProps, getInputProps } = useDropzone({
        accept,
        maxSize,
        minSize,
        multiple,
        ...options,
        onDrop
    });

    return (
        <StyledBox {...getRootProps()}>
            <input
                {...getInputProps()}
            />
            {
                placeholder && placeholder
            }
            {
                (!placeholder && multiple) ? (
                    <p>{translate(labelMultiple)}</p>
                ) : (
                    <p>{translate(labelSingle)}</p>
                )
            }
        </StyledBox>
    );
};

export default DropZone
