// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import Card from '@mui/material/Card';
import CardHeader from '@mui/material/CardHeader';
import CardContent from '@mui/material/CardContent';
import Stack from '@mui/material/Stack';
import Divider from '@mui/material/Divider';
import { PieChart } from '@mui/x-charts/PieChart';
import { BarChart } from '@mui/x-charts/BarChart';
import {
    useRecordContext, NumberField,
    Labeled, FunctionField, useTranslate,
} from 'react-admin';
import { styled } from '@mui/material/styles';

import { Session } from '@/types';
import { processDailyUsage } from '@/utils';

const StyledCard = styled(Card, {
    name: 'GFSessionUsageCard',
    slot: 'root',
})(() => ({
    display: 'flex',
    flexDirection: 'column',
    height: '100%',
}));

type SessionUsageCardProps = object;

const SessionUsageCard: FC<SessionUsageCardProps> = () => {
    const session = useRecordContext<Session>();
    const translate = useTranslate();

    if (!session || !session.usage) {
        return null;
    }

    return (
        <StyledCard>
            <CardHeader
                subheader={translate('resources.sessions.fields.usage.title')}
            />
            <CardContent>
                <Labeled source='usage.total_messages'>
                    <NumberField source='usage.total_messages' />
                </Labeled>
                <Stack
                    direction='row'
                    divider={<Divider orientation='vertical' flexItem />}
                    spacing={2}
                >
                    <Stack>
                        <Labeled source='usage.total_tokens'>
                            <FunctionField
                                source='usage.total_tokens'
                                render={(record) => record.usage.total_input_tokens + record.usage.total_output_tokens}
                            />
                        </Labeled>
                        <PieChart
                            series={[
                                {
                                    data: [
                                        {
                                            value: session.usage.total_input_tokens,
                                            label: translate('resources.sessions.fields.usage.total_input_tokens')
                                        },
                                        {
                                            value: session.usage.total_output_tokens,
                                            label: translate('resources.sessions.fields.usage.total_output_tokens')
                                        },
                                    ],
                                    highlightScope: { fade: 'global', highlight: 'item' },
                                    faded: { innerRadius: 30, additionalRadius: -30, color: 'gray' },
                                    valueFormatter: (value) => `${value.value} tokens`,
                                },
                            ]}
                            width={200}
                            height={100}
                        />
                    </Stack>
                    <Stack>
                        <Labeled source='usage.total_price'>
                            <NumberField
                                source='usage.total_price'
                                options={{
                                    style: 'currency',
                                    currency: session.usage.currency,
                                    maximumFractionDigits: 4,
                                }}
                            />
                        </Labeled>
                        <PieChart
                            series={[
                                {
                                    data: [
                                        {
                                            value: session.usage.total_input_price,
                                            label: translate('resources.sessions.fields.usage.total_input_price')
                                        },
                                        {
                                            value: session.usage.total_output_price,
                                            label: translate('resources.sessions.fields.usage.total_output_price')
                                        },
                                    ],
                                    highlightScope: { fade: 'global', highlight: 'item' },
                                    faded: { innerRadius: 30, additionalRadius: -30, color: 'gray' },
                                    valueFormatter: (value) => `${value.value.toFixed(4)} ${session.usage?.currency}`,
                                },
                            ]}
                            width={200}
                            height={100}
                        />
                    </Stack>
                </Stack>
                <Divider sx={{ m: 1 }} />
                <Labeled source='usage.per_day'>
                    <BarChart
                        dataset={processDailyUsage(session.usage.per_day)}
                        xAxis={[{ scaleType: 'band', dataKey: 'day' }]}
                        series={[{
                            dataKey: 'total_price',
                            valueFormatter: (value) => `${value?.toFixed(4)} ${session.usage?.currency}`,
                        }]}
                        width={400}
                        height={250}
                    />
                </Labeled>
            </CardContent>
        </StyledCard>
    );
};

export default SessionUsageCard;
