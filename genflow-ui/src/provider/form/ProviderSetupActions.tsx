// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import {
    useRecordContext, SaveButton,
    DeleteWithConfirmButton, useNotify, useRefresh,
} from 'react-admin';
import { useFormContext } from 'react-hook-form';

import { Provider } from '@/types';
import { CancelButton } from '@/common';

type ProviderSetupActionsProps = {
    onClose: () => void;
};

const ProviderSetupActions: FC<ProviderSetupActionsProps> = ({
    onClose,
}) => {
    const record = useRecordContext<Provider>();
    const { reset } = useFormContext();
    const notify = useNotify();
    const refresh = useRefresh();

    const renderDisableButton = (provider: Provider): JSX.Element | null => {
        if (provider.is_enabled) {
            return (
                <DeleteWithConfirmButton
                    mutationOptions={{
                        onSuccess: () => {
                            reset();
                            refresh();
                            onClose();
                        },
                        onError: (error) => {
                            notify((error as Error).toString(), { type: 'error' });
                        }
                    }}
                    confirmTitle='message.delete_dialog.disable_title'
                    confirmContent='message.delete_dialog.disable_content'
                    translateOptions={{ resource: 'provider' }}
                    redirect={false}
                />
            );
        }
        return null;
    };

    return (
        <>
            {
                record && renderDisableButton(record)
            }
            <CancelButton
                onClick={() => {
                    reset();
                    onClose();
                }}
            />
            <SaveButton
                type='button'
                mutationOptions={{
                    onSuccess: () => {
                        reset();
                        onClose();
                    },
                    onError: (error) => {
                        notify((error as Error).toString(), { type: 'error' });
                        reset();
                    }
                }}
            />
        </>
    );
};

export default ProviderSetupActions;
