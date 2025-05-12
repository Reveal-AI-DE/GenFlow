// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, {
    FC, useCallback, ReactNode, useEffect,
    useRef, SyntheticEvent, useState,
} from 'react';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import RemoveIcon from '@mui/icons-material/Remove';
import EditIcon from '@mui/icons-material/Edit';
import IconButton from '@mui/material/IconButton';
import {
    useTranslate,useGetIdentity, HttpError,
    useRefresh, useNotify,
} from 'react-admin';
import Uploady, {
    useUploadyContext, UploadOptions, useItemFinishListener,
    useBatchAddListener, Batch, useRequestPreSend, BatchItem,
    useItemErrorListener,
} from '@rpldy/uploady';

import { TransformedFile } from '@/types';
import { WithTooltip, CropDialog } from '@/common';
import { createUploadyDestination } from '@/utils';
import { userDataProvider } from '@/user';

interface UploadAvatarButtonControllerProps {
    icon: ReactNode;
};

const UploadAvatarButtonController: FC<UploadAvatarButtonControllerProps> = ({
    icon,
}) => {
    const [open, setOpen] = useState<boolean>(false);
    const [file, setFile] = useState<File | null>(null);
    const [ready, setReady] = useState<boolean>(false);
    const translate = useTranslate();
    const refresh = useRefresh();
    const notify = useNotify();

    const { showFileUpload, processPending } = useUploadyContext();
    // using ref so onButtonClick can stay memoized
    const uploadOptionsRef = useRef<UploadOptions>();
    uploadOptionsRef.current = {
        autoUpload: false,
        clearPendingOnAdd: true,
    };

    const handleUpload = useCallback((e: SyntheticEvent<HTMLElement>) => {
        e.stopPropagation();
        showFileUpload(uploadOptionsRef.current);
    }, [showFileUpload, uploadOptionsRef]);

    useBatchAddListener((batch: Batch) => {
        setFile(batch.items[0].file as File);
        setOpen(true);
    });

    const onCropFinished = (transformedFile: TransformedFile): void => {
        setFile(transformedFile.rawFile);
        setReady(true);
    };

    useRequestPreSend(({ items }) => ({
        items: file ? [
            {
                ...items[0],
                file,
            }
        ] : items,
    }));

    useItemFinishListener(() => {
        localStorage.removeItem('RaStoreGeniFlow.identity');
        refresh();
    });

    useItemErrorListener((it: BatchItem) => {
        const { data } = it.uploadResponse;
        notify(
            data.message || 'ra.notification.http_error',
            {
                type: 'error',
            }
        );
    });

    useEffect(() => {
        if (ready) {
            processPending({
                autoUpload: true,
                clearPendingOnAdd: true,
            });
            setReady(false);
        }
    }, [ready, processPending]);

    const handleClose = (): void => setOpen(false);

    return (
        <>
            <WithTooltip
                title={translate('action.upload')}
                trigger={(
                    <span>
                        <IconButton
                            edge='start'
                            aria-label={translate('action.upload')}
                            size='medium'
                            color='primary'
                            onClick={handleUpload}
                        >
                            {icon}
                        </IconButton>
                    </span>
                )}
            />
            <CropDialog
                open={open}
                file={file}
                onCropFinished={onCropFinished}
                onClose={handleClose}
            />
        </>
    );
};

type UploadAvatarButtonProps = object;

const UploadAvatarButton: FC<UploadAvatarButtonProps> = () => {
    const { data: currentUser } = useGetIdentity();
    const translate = useTranslate();
    const refresh = useRefresh();
    const notify = useNotify();

    if (!currentUser) {
        return null;
    }

    const destination = createUploadyDestination('users', currentUser.id, 'upload_avatar');

    const icon = currentUser.avatar ? (
        <EditIcon />
    ) : (
        <AddCircleOutlineIcon />
    );

    const handleRemove = (e: SyntheticEvent<HTMLElement>): void => {
        e.stopPropagation();
        userDataProvider.remove_avatar('users', { id: currentUser.id })
            .then(() => {
                localStorage.removeItem('RaStoreGeniFlow.identity');
                refresh();
            })
            .catch((error: HttpError) => {
                notify(
                    error.message || 'ra.notification.http_error',
                    {
                        type: 'error',
                    }
                );
            });
    };

    return (
        <Uploady
            multiple={false}
            autoUpload={false}
            clearPendingOnAdd
            accept='image/png'
            destination={destination || undefined}
        >
            <UploadAvatarButtonController
                icon={icon}
            />
            {
                currentUser.avatar && (
                    <WithTooltip
                        title={translate('ra.action.remove')}
                        trigger={(
                            <span>
                                <IconButton
                                    edge='start'
                                    aria-label={translate('ra.action.remove')}
                                    size='medium'
                                    color='error'
                                    onClick={handleRemove}
                                >
                                    <RemoveIcon />
                                </IconButton>
                            </span>
                        )}
                    />
                )
            }
        </Uploady>
    )
};

export default UploadAvatarButton;
