// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import { SaveButton } from 'react-admin';
import { useFormContext } from 'react-hook-form';

import { CancelButton } from '@/common';

interface GroupFormActionsProps {
    onClose: () => void;
};

const GroupFormActions: FC<GroupFormActionsProps> = ({
    onClose
}) => {
    const { reset } = useFormContext();

    return (
        <>
            <CancelButton
                onClick={() => {
                    reset();
                    onClose();
                }}
            />
            <SaveButton
                type='button'
            />
        </>
    );
};

export default GroupFormActions;
