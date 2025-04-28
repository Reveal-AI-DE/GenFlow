// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, {
    FC, useContext, useCallback,
    createElement, SyntheticEvent,
} from 'react';
import IconButton from '@mui/material/IconButton';
import {
    useRecordContext, Form, useTranslate,
    AutocompleteInputProps,
} from 'react-admin';

import { Session, SessionType, PromptStatus } from '@/types';
import { SessionContext, SessionContextInterface } from '@/context';
import { WithTooltip } from '@/common';
import { PromptResourceProps } from '@/prompt';
import { PromptSelectInput } from '@/prompt/form';

interface PromptSelectionButtonProps {
    onClick?: (e: SyntheticEvent<HTMLElement>) => void;
};

export const PromptSelectionButton: FC<PromptSelectionButtonProps> = ({
    onClick,
}) => {
    const session = useRecordContext<Session>();
    if (!session || session.session_type !== SessionType.LLM) return null;

    const translate = useTranslate();
    const {
        setPromptSelection,
    } = useContext<SessionContextInterface>(SessionContext);

    const handleClick = useCallback((e: SyntheticEvent<HTMLElement>) => {
        setPromptSelection((prev) => !prev);
        onClick?.(e);
    }, []);

    return (
        <WithTooltip
            title={translate('action.use_prompt')}
            trigger={(
                <span>
                    <IconButton
                        edge='start'
                        aria-label={translate('action.use_prompt')}
                        disabled={!session}
                        onClick={handleClick}
                        size='small'
                    >
                        {
                            PromptResourceProps.icon ? createElement(PromptResourceProps.icon, { fontSize: 'small'}) : false
                        }
                    </IconButton>
                </span>
            )}
            arrow
        />
    );
};

type PromptSelectionProps = object;

const PromptSelection: FC<PromptSelectionProps> = () => {
    const session = useRecordContext<Session>();
    if (!session || session.session_type !== SessionType.LLM) return null;

    const {
        promptSelection,
        setUserInput,
    } = useContext<SessionContextInterface>(SessionContext);

    if (!promptSelection) return null;

    const onPromptChange: AutocompleteInputProps['onChange'] = (
        value,
        record
    ) => {
        if (!record) {
            return;
        }
        setUserInput(record.pre_prompt);
    };

    return (
        <Form>
            <PromptSelectInput
                source='prompt'
                filter={{ status: PromptStatus.PUBLISHED }}
                sort={{ field: 'group__name', order: 'ASC' }}
                onChange={onPromptChange}
            />
        </Form>
    );
};

export default PromptSelection;
