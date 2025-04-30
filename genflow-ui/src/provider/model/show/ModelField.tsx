// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC, Fragment } from 'react';
import Tooltip from '@mui/material/Tooltip';
import Chip from '@mui/material/Chip';
import { styled } from '@mui/material/styles';
import { useLocale, useTranslate, useRecordContext } from 'react-admin';

import { PropertyKey, ModelEntity } from '@/types';
import { formatBytes } from '@/utils';

const StyledChip = styled(Chip, {
    name: 'GFModelField',
    slot: 'Chip',
})(() => ({
    borderRadius: 0,
    margin: '0 3px',
    fontSize: '0.6rem',
    '& .MuiChip-labelSmall': {
        padding: '0 2px',
    }
}));

interface ModelPropertyProps {
    property: PropertyKey;
    value: any;
}

const ModelPropertyItem: FC<ModelPropertyProps> = ({
    property,
    value,
}) => {
    let label = '';
    switch (property) {
        case PropertyKey.CONTEXT_SIZE:
            label = formatBytes(value);
            break;
        default:
            label = value.toUpperCase();
    };

    return (
        <Tooltip key={property} title={property}>
            <StyledChip
                label={label}
                size='small'
                sx={{ fontSize: '11px' }}
            />
        </Tooltip>
    )
};

export enum ModelFieldSlot {
    NAME = 'name',
    TYPE = 'type',
    PROPERTIES = 'properties',
};

export interface ModelFieldProps {
    slots?: ModelFieldSlot[];
    properties?: PropertyKey[];
}

const ModelField: FC<ModelFieldProps> = ({
    slots=[ModelFieldSlot.NAME, ModelFieldSlot.TYPE, ModelFieldSlot.PROPERTIES],
    properties=[PropertyKey.MODE, PropertyKey.CONTEXT_SIZE],
}) => {
    const record = useRecordContext<ModelEntity>();
    if (!record) {
        return null;
    }

    const locale = useLocale();
    const translate = useTranslate();

    const renderSlot = (slot: ModelFieldSlot): JSX.Element | null => {
        switch (slot) {
            case ModelFieldSlot.NAME:
                return (
                    <span>
                        {record.label[locale] ?? record.label.en_US}
                    </span>
                );
            case ModelFieldSlot.TYPE:
                return (
                    <Tooltip
                        title={translate('resources.models.fields.type')}
                    >
                        <StyledChip
                            label={record.type.toUpperCase()}
                            size='small'
                        />
                    </Tooltip>
                );
            case ModelFieldSlot.PROPERTIES:
                return (
                    <>
                        {
                            Object.keys(record.properties).map((key: string) => {
                                if (properties && !properties.includes(key as PropertyKey)) {
                                    return null;
                                }
                                return (
                                    <ModelPropertyItem
                                        key={key}
                                        property={key as PropertyKey}
                                        value={record.properties[key as PropertyKey]}
                                    />
                                );
                            })
                        }
                    </>
                );
            default:
                return null;
        }
    };

    return (
        <span>
            {
                slots.map((slot: ModelFieldSlot) => (
                    <Fragment key={slot}>
                        {renderSlot(slot)}
                    </Fragment>
                ))
            }
        </span>
    )
};

export default ModelField;
