// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import {
    Identifier, RaRecord, GetListParams,
    DeleteParams, DeleteManyParams,
} from 'react-admin';

export interface FileEntity extends RaRecord {
    path: string;
};

export interface GetFilesMeta {
    resource: string;
    recordId: Identifier;
}

export interface GetFilesParams extends GetListParams {
    meta: GetFilesMeta;
};

export interface DeleteFileMeta {
    resource: string;
    fileId: string;
};

export interface DeleteFileParams extends DeleteParams {
    meta: DeleteFileMeta;
};

export interface DeleteFilesMeta {
    resource: string;
    recordId: Identifier;
};

export interface DeleteFilesParams extends DeleteManyParams {
    meta: DeleteFilesMeta;
};

export interface TransformedFile {
    rawFile: File;
    src: string;
    title: string;
};
