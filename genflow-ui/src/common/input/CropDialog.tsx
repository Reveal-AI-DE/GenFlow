// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC, useRef } from 'react';
import {
    FixedCropperRef, FixedCropper,
    CircleStencil, ImageRestriction
} from 'react-advanced-cropper';
import { Button, useTranslate } from 'react-admin';

import { TransformedFile } from '@/types';
import { Dialog, CancelButton } from '@/common';

interface CropDialogProps {
    open: boolean;
    file: File | null;
    onCropFinished: (transformedFile: TransformedFile) => void;
    onClose: () => void;
};

const CropDialog: FC<CropDialogProps> = ({
    open,
    file,
    onCropFinished,
    onClose,
}) => {
    const cropperRef = useRef<FixedCropperRef>(null);
    const translate = useTranslate();

    const transformFile = (fileObj: File): TransformedFile => {
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
                        onCropFinished(transformFile(
                            new File([blob],
                                file.name,
                                {
                                    type: file.type,
                                    lastModified: file.lastModified,
                                }
                            )));
                    }
                });
            onClose();
        }
    };

    return (
        <Dialog
            open={open}
            onClose={onClose}
            title={translate('label.crop')}
            maxWidth='md'
            sx={{
                '& .cropper': {
                    maxHeight: 'calc(100vh - 200px)',
                },
            }}
            dialogContent={(
                <FixedCropper
                    ref={cropperRef}
                    src={file ? URL.createObjectURL(file) : file}
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
                            onClose();
                        }}
                    />
                    <Button
                        label={translate('action.crop')}
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
    );
};

export default CropDialog;
