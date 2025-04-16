// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC, useState, useRef } from 'react';
import { DropzoneProps } from 'react-dropzone';
import {
    FixedCropperRef, FixedCropper,
    CircleStencil, ImageRestriction
} from 'react-advanced-cropper';
import 'react-advanced-cropper/dist/style.css';

import { useFormContext } from 'react-hook-form';
import {
    ImageInput as RAImageInput,
    ImageInputProps as RAImageInputProps,
    Button, ImageField,
} from 'react-admin';

import { Dialog, CancelButton } from '@/common';

const ImageInput: FC<RAImageInputProps> = ({
    options,
    ...props
}) => {
    const cropperRef = useRef<FixedCropperRef>(null);
    const [open, setOpen] = useState<boolean>(false);
    const [file, setFile] = useState<File | null>(null);
    const { setValue } = useFormContext();

    const handleClose = (): void => setOpen(false);

    const onDropAccepted: DropzoneProps['onDropAccepted'] = (files: File[]): void => {
        setFile(files[0]);
        setOpen(true);
    };

    const transformFile = (fileObj: File): any => {
        const preview = URL.createObjectURL(fileObj);
        const transformedFile = {
            rawFile: fileObj,
            src: preview,
            title: fileObj.name,
        };

        return transformedFile;
    }

    const onCrop = (): void => {
        if (file && cropperRef.current) {
            cropperRef.current
                .getCanvas()?.toBlob((blob) => {
                    if (blob) {
                        setValue(props.source, transformFile(new File([blob], file.name)));
                    }
                });
            handleClose();
        }
    };

    return (
        <>
            <RAImageInput
                {...props}
                options={{
                    ...options,
                    onDropAccepted,
                }}
            >
                <ImageField source='src' />
            </RAImageInput>
            <Dialog
                open={open}
                onClose={handleClose}
                title='Crop Image'
                maxWidth='md'
                sx={{
                    '& .cropper': {
                        maxHeight: 'calc(100vh - 200px)',
                    },
                }}
                dialogContent={(
                    <FixedCropper
                        ref={cropperRef}
                        src={file ? URL.createObjectURL(file) : ''}
                        className='cropper'
                        stencilComponent={CircleStencil}
                        stencilSize={{
                            width: 400,
                            height: 400
                        }}
                        stencilProps={{
                            handlers: false,
                            lines: false,
                            movable: false,
                            resizable: false
                        }}
                        imageRestriction={ImageRestriction.stencil}
                    />
                )}
                dialogAction={() => (
                    <>
                        <CancelButton
                            size='medium'
                            variant='outlined'
                            color='warning'
                            onClick={() => {
                                handleClose();
                            }}
                        />
                        <Button
                            label='done'
                            size='medium'
                            variant='outlined'
                            onClick={() => {
                                onCrop();
                            }}
                        />
                    </>
                )}
                fullWidth
            />
        </>
    )
}

export default ImageInput;
