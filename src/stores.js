import { writable } from "svelte/store";


export const baseURL = "http://127.0.0.1:5001";

export const videoId = writable("");

export const uid = writable("");

export const username = writable("");

export function setUsername(value) {
    username = value;
}

export function setOffset(value) {
    offset = value;
}

export const message = writable("");

export const comments = writable({});

export var lastCommentUpdateTime = "";
export function setLastCommentUpdateTime(value) {
    lastCommentUpdateTime = value;
}

export const Status = {
    Initial: 'Initial',
    Loading: 'Loading',
    Success: 'Success',
    Failed: 'Failed',
    MissingUsername: 'MissingUsername',
    CommentsEnabled: 'CommentsEnabled',
    NotLoggedIn: 'NotLoggedIn'
}

export const status = writable(Status.Initial);

