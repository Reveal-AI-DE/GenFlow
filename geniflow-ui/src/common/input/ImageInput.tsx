// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC, useState } from 'react';
import { DropzoneProps } from 'react-dropzone';
import 'react-advanced-cropper/dist/style.css';

import { useFormContext } from 'react-hook-form';
import {
    ImageInput as RAImageInput,
    ImageInputProps as RAImageInputProps,
    ImageField, useNotify,
} from 'react-admin';

import { TransformedFile } from '@/types';
import { CropDialog } from '@/common';

const ImageInput: FC<RAImageInputProps> = ({
    options,
    ...props
}) => {
    const [open, setOpen] = useState<boolean>(false);
    const [file, setFile] = useState<File | null>(null);
    const { setValue } = useFormContext();
    const notify = useNotify();

    const handleClose = (): void => setOpen(false);

    const onDropAccepted: DropzoneProps['onDropAccepted'] = (files: File[]): void => {
        setFile(files[0]);
        setOpen(true);
    };

    const onDropRejected: DropzoneProps['onDropRejected'] = (): void => {
        notify('message.image_not_supported', { type: 'warning'});
    };

    const onCropFinished = (transformedFile: TransformedFile): void => {
        setValue(props.source, transformedFile);
    };

    return (
        <>
            <RAImageInput
                {...props}
                options={{
                    ...options,
                    accept: {
                        'image/*': ['.png', '.jpg']
                    },
                    onDropAccepted,
                    onDropRejected,
                }}
                maxSize={1024 * 1024} // 1MB
            >
                <ImageField source='src' />
            </RAImageInput>
            <CropDialog
                open={open}
                file={file}
                onCropFinished={onCropFinished}
                onClose={handleClose}
            />
        </>
    )
}

export default ImageInput;
