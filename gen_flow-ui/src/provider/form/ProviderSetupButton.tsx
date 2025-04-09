// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import {
    CreateBase, EditBase, Form, useNotify,
    useTranslate, useLocale, useRecordContext,
} from 'react-admin';

import { AIProviderConfiguration, Provider } from '@/types';
import { ButtonWithDialog } from '@/common';

import ProviderSetupForm from '@/provider/form/ProviderSetupForm';
import ProviderHelp from '@/provider/form/ProviderHelp';
import ProviderSetupActions from '@/provider/form/ProviderSetupActions';

type ProviderSetupButtonProps = object;

const ProviderSetupButton: FC<ProviderSetupButtonProps> = () => {
    const translate = useTranslate();
    const locale = useLocale();
    const notify = useNotify();
    const aiProviderConfiguration = useRecordContext<AIProviderConfiguration>();

    if (!aiProviderConfiguration) {
        return null;
    }

    let ProviderSetupRoot: any = CreateBase;
    // edit mode
    if (aiProviderConfiguration.user_configuration?.active) {
        ProviderSetupRoot = EditBase;
    }

    const transform = (data: Provider): Provider => ({
        ...data,
        provider_name: aiProviderConfiguration.id as string,
    });

    const populateProps = (activeProvider: boolean | undefined): object => (
        activeProvider ? {
            id: aiProviderConfiguration.user_configuration?.provider as string,
            mutationMode: 'pessimistic',
            queryOptions: {
                onError: () => {
                    notify('ra.notification.item_doesnt_exist', {
                        type: 'error',
                    });
                },
            }
        } : {
            transform
        }
    );

    return (
        <ProviderSetupRoot<Provider>
            resource='providers'
            redirect={false}
            {...populateProps(aiProviderConfiguration.user_configuration?.active)}
        >
            <Form>
                <ButtonWithDialog
                    label='action.setup'
                    sx={{
                        width: '100%',
                    }}
                    dialog={{
                        title: translate('action.setup_name', {
                            name: aiProviderConfiguration.label[locale] ?? aiProviderConfiguration.label.en_US
                        }),
                        maxWidth: 'sm',
                        fullWidth: true,
                        disableBackdropClick: true,
                        ContentProps: {
                            dividers: true,
                        },
                        dialogContent: (
                            <ProviderSetupForm
                                credentialForm={aiProviderConfiguration.credential_form || []}
                            />
                        ),
                        dialogAction: (onClose) => (
                            <>
                                <ProviderHelp help={aiProviderConfiguration.help} />
                                <ProviderSetupActions
                                    onClose={() => onClose && onClose({}, 'escapeKeyDown')}
                                />
                            </>
                        )
                    }}
                />
            </Form>
        </ProviderSetupRoot>
    );
};

export default ProviderSetupButton;
