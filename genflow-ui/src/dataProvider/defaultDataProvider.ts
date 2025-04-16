// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import queryString from 'query-string';

import {
    Identifier, PaginationPayload, SortPayload, FilterPayload, DataProvider,
} from 'react-admin';

import { MetaParams } from '@/types';
import { ResourceURL } from '@/utils';
import { fetchJsonWithAuthToken } from '../authProvider';

const getPaginationQuery = (pagination: PaginationPayload): object => ({
    page: pagination.page,
    page_size: pagination.perPage,
});

const getFilterQuery = (filter: FilterPayload): object => {
    const { q: search, ...otherSearchParams } = filter;
    return {
        ...otherSearchParams,
        search,
    };
};

export const getOrderingQuery = (sort: SortPayload): object => {
    const { field, order } = sort;
    return {
        ordering: `${order === 'ASC' ? '' : '-'}${field}`,
    };
};

export const baseURL = process.env.REACT_APP_BACKEND_API_BASE_URL;

const getOneJson = (resource: string, id: Identifier): Promise<any> => (
    fetchJsonWithAuthToken(
        ResourceURL(`/${resource}/${id}`, baseURL),
    ).then((response: Response) => response.json)
);

export default <DataProvider>{
    getList: async (resource, params) => {
        const query: {
            page?: number;
            page_size?: number | string;
            ordering?: string;
            search?: string;
        } = {
            ...getFilterQuery(params.filter ? params.filter : {}),
            ...getPaginationQuery(params.pagination ? params.pagination : { page: 1, perPage: 10 }),
            ...getOrderingQuery(params.sort ? params.sort : { field: 'id', order: 'ASC' }),
        };
        if (query.page_size === -1) {
            query.page_size = 'all';
        }

        const url = ResourceURL(`/${resource}?${queryString.stringify(query, { arrayFormat: 'comma' })}`, baseURL);
        const { json } = await fetchJsonWithAuthToken(url);
        return {
            data: json.results,
            total: json.count,
        };
    },

    getOne: async (resource, params) => {
        const data = await getOneJson(resource, params.id);
        return {
            data,
        };
    },

    getMany: (resource, params) => (
        Promise.all(
            params.ids.map((id) => getOneJson(resource, id)),
        ).then((data) => (
            {
                data,
            }
        ))
    ),

    getManyReference: async (resource, params) => {
        const query = {
            ...getFilterQuery(params.filter),
            ...getPaginationQuery(params.pagination),
            ...getOrderingQuery(params.sort),
            [params.target]: params.id,
        };
        const url = ResourceURL(`/${resource}?${queryString.stringify(query, { arrayFormat: 'comma' })}`, baseURL);
        const { json } = await fetchJsonWithAuthToken(url);
        return {
            data: json.results,
            total: json.count,
        };
    },

    update: async (resource, params) => {
        let url = ResourceURL(`/${resource}/${params.id}`, baseURL)
        if (params.meta && params.meta.queryParams) {
            const { queryParams } = params.meta as MetaParams;
            if (queryParams) {
                url = `${url}?${queryString.stringify(queryParams, { arrayFormat: 'comma' })}`;
            }
        }
        const { json } = await fetchJsonWithAuthToken(url, {
            method: 'PATCH',
            body: JSON.stringify(params.data),
        });
        return { data: json };
    },

    updateMany: (resource, params) => Promise.all(
        params.ids.map((id) => fetchJsonWithAuthToken(ResourceURL(`/${resource}/${id}`, baseURL), {
            method: 'PATCH',
            body: JSON.stringify(params.data),
        })),
    ).then((responses) => ({ data: responses.map(({ json }) => json.id) })),

    create: async (resource, params) => {
        let url = ResourceURL(`/${resource}`, baseURL);
        if (params.meta && params.meta.queryParams) {
            const { queryParams } = params.meta as MetaParams;
            if (queryParams) {
                url = `${url}?${queryString.stringify(queryParams, { arrayFormat: 'comma' })}`;
            }
        }
        const { json } = await fetchJsonWithAuthToken(url, {
            method: 'POST',
            body: JSON.stringify(params.data),
        });
        return {
            data: { ...json },
        };
    },

    delete: (resource, params) => fetchJsonWithAuthToken(ResourceURL(`/${resource}/${params.id}`, baseURL), {
        method: 'DELETE',
    }).then((json) => ({ data: json })),

    deleteMany: (resource, params) => Promise.all(
        params.ids.map((id) => (
            fetchJsonWithAuthToken(ResourceURL(`/${resource}/${id}`, baseURL), {
                method: 'DELETE',
            }))),
    ).then(() => ({ data: [] })),
};
