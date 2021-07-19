import { writable } from "svelte/store";


export const baseURL = "http://127.0.0.1:5001";



export const uid = writable("");

export var username = "";

export function setUsername(value) {
    username = value;
    console.log(username);
}

export var offset = 0;

export function setOffset(value) {
    offset = value;
}

export const message = writable("");

export const comments = writable({});
